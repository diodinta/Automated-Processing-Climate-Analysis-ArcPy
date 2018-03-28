import os
import urllib2
import datetime
from cookielib import CookieJar
from datetime import date
import time
import logging
import NetCDFProcessing

LOG_FILENAME = os.path.join("D:\\PyCharm Projects\\SingleProject\\log", 'dslr_log_'+time.strftime("%Y%m%d")+'.log')
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
datelog = time.strftime('%c')
os.chdir("D:\\PyCharm Projects\\SingleProject")


def download_imerg(doyear, domonth, dodate, imerg_nc4_folder):
    logging.debug(datelog+" : starts downloading imerg data for "+doyear+domonth+dodate)
    username = 'diodinta'
    password = 'Semangat2015'
    url = 'http://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGDL.05/'+doyear+'/'+domonth+'/3B-DAY-L.MS.MRG.3IMERG.'+doyear+domonth+dodate+'-S000000-E235959.V05.nc4'
    file_name = url.split('/')[-1]
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, "https://urs.earthdata.nasa.gov", username, password)
    cookie_jar = CookieJar()
    opener = urllib2.build_opener(
        urllib2.HTTPBasicAuthHandler(password_manager),
        # urllib2.HTTPHandler(debuglevel=1),    # Uncomment these two lines to see
        # urllib2.HTTPSHandler(debuglevel=1),   # details of the requests/responses
        urllib2.HTTPCookieProcessor(cookie_jar))
    urllib2.install_opener(opener)
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request)
        body = response.read()
        file_ = open(os.path.join(imerg_nc4_folder,file_name), 'wb')
        file_.write(body)
        file_.close()
        logging.debug(datelog+" : Your file, "+ file_name+ " has downloaded to "+ imerg_nc4_folder)
    except urllib2.HTTPError as e:
        if e.code == 404:
            print("file not found")
            result = 'false'
        else:
            print("another error")
    #return result

    # Print out the result (not a good idea with binary data!)



def checking_imerg_data(imerg_nc4_folder, tiffolder):
    logging.debug(datelog+" : Starts checking IMERG data")
    index_nc4_data = []
    todaydate = date.today() - datetime.timedelta(days=2)
    print(todaydate)
    for i in os.listdir(imerg_nc4_folder):
        if i.endswith(".nc4"):
            parseString = i.split('.')
            parse = parseString[4]
            nc4_date = parse[0:8]
            index_nc4_data.append(nc4_date)
    #------check if the data is complete since last day------#
    index_sorted = sorted(index_nc4_data, reverse=False)
    last_data = index_sorted[-1]
    logging.debug(datelog+" : last data available is on date "+last_data)
    last_data_date = date(int(last_data[0:4]),int(last_data[4:6]), int(last_data[6:8]))
    calculate_num_day_data = last_data_date - date(2014,03,12)
    deltaday = calculate_num_day_data.days + 1
    if deltaday == len(index_sorted):
        logging.debug(datelog+" : data before last data is complete. Checking missing data since today "+str(todaydate)+".....")
        if last_data_date < todaydate:
            logging.debug(datelog+" : Processing data missing since "+str(last_data_date))
            while last_data_date < todaydate:
                last_data_date = last_data_date + datetime.timedelta(days=1)
                print("downloading "+str(last_data_date))
                result = download_imerg(str(last_data_date.year),str(last_data_date.month).zfill(2),str(last_data_date.day).zfill(2), imerg_nc4_folder)
                nc4_file = '3B-DAY-L.MS.MRG.3IMERG.'+str(last_data_date.year)+str(last_data_date.month).zfill(2)+str(last_data_date.day).zfill(2)+'-S000000-E235959.V05.nc4'
                if result == 'false':
                    print(datelog+" : file does not exist: "+nc4_file)
                else:
                    NetCDFProcessing.createRaster(imerg_nc4_folder, nc4_file, tiffolder)
                    print(datelog+" : tiffile from "+nc4_file+ " is created")
        else:
            logging.debug(datelog+" : No data missing since "+str(last_data_date))
    else:
        logging.debug(datelog+" : it is weird. there is data missing before "+str(last_data_date)+".....")
        logging.debug(datelog+" : you want me to check ?")
        logging.debug(datelog+" : it is a lot of work tho' ")
