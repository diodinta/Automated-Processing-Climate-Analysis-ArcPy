import sys
import re
import arcpy
import ALFlib
import urllib2
from datetime import date
import tempfile
import os
from cookielib import CookieJar
import time
import logging

LOG_FILENAME = os.path.join("D:\\PyCharm Projects\\SingleProject\\log", 'vhi_log_'+time.strftime("%Y%m%d")+'.log')
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
datelog = time.strftime('%c')

def DownloadRoutine(tile, year, momonth, outputfolder):
    """Downloads files"""
    username = 'diodinta'
    password = 'Semangat2015'
    scratch = tempfile.mkdtemp()
    f = date(int(year), int(momonth), 1)
    DOY = str(f.timetuple().tm_yday).rjust(3, '0')
    hdf_pattern = re.compile('MOD13A3.A'+year+DOY+'.'+ tile +'.006.*.hdf$', re.IGNORECASE)
    source = "http://e4ftl01.cr.usgs.gov/" + "MOLT/MOD13A3.006/" + year + "." + momonth + ".01/"
    webFile = os.path.join(scratch, "earthdata.html")

    matched_file = ''
    files = []
    match_array = []
    try:
        if ALFlib.getDownload(source, webFile):
            page = open(webFile).read()
            files = []
            for url in page.split('<a href="'):
                link = url.split('">', 1)[0]
                if link.endswith('hdf'):
                    files.append(link.split("/")[-1])
    except urllib2.HTTPError:
        arcpy.AddMessage("\n[ERROR] No data for that date\n")
        sys.exit()
    for f in files:
        if re.match(hdf_pattern,f):
            matched_file = f
            match_array.append(matched_file)
            break
    if matched_file == '':
            print("\n[ERROR] No data for that tile\n")

    print("Found: " + matched_file)

    username = 'diodinta'
    password = 'Semangat2015'
    for f in match_array:
        url = os.path.join(source, f)
        print(url)
        file_name = url.split('/')[-1]

        # The user credentials that will be used to authenticate access to the data
        # Create a password manager to deal with the 401 reponse that is returned from
        # Earthdata Login

        password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(None, "https://urs.earthdata.nasa.gov", username, password)

        # Create a cookie jar for storing cookies. This is used to store and return
        # the session cookie given to use by the data server (otherwise it will just
        # keep sending us back to Earthdata Login to authenticate).  Ideally, we
        # should use a file based cookie jar to preserve cookies between runs. This
        # will make it much more efficient.

        cookie_jar = CookieJar()

        # Install all the handlers.

        opener = urllib2.build_opener(
            urllib2.HTTPBasicAuthHandler(password_manager),
            # urllib2.HTTPHandler(debuglevel=1),    # Uncomment these two lines to see
            # urllib2.HTTPSHandler(debuglevel=1),   # details of the requests/responses
            urllib2.HTTPCookieProcessor(cookie_jar))
        urllib2.install_opener(opener)

        # Create and submit the request. There are a wide range of exceptions that
        # can be thrown here, including HTTPError and URLError. These should be
        # caught and handled.

        request = urllib2.Request(url)
        response = urllib2.urlopen(request)

        # Print out the result (not a good idea with binary data!)

        body = response.read()
        file_ = open(os.path.join(outputfolder,file_name), 'wb')
        file_.write(body)
        file_.close()

        logging.debug(datelog+" : Your file, ", file_name, " has downloaded to ", os.path.join(outputfolder,file_name))

def checking_last_data(vhi_folder):
    for i in os.listdir(vhi_folder):
        print(i)