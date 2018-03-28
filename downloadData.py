import VampireDefaults
import ftputil
import os
import re
import datetime
import gzip
import time
import logging

LOG_FILENAME = os.path.join("D:\\PyCharm Projects\\SingleProject\\log", 'vampire_download_log_'+time.strftime("%Y%m%d")+'.log')
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
datelog = time.strftime('%c')

def downloadCHIRPSData(interval, output_dir, tiffolder):
    interval = interval
    output_dir = output_dir
    start_date = None
    end_date = None
    dates = None
    overwrite = False

    vampire = VampireDefaults.VampireDefaults()
    _ftp_dir = vampire.get('CHIRPS', 'ftp_dir_{0}'.format(interval.lower()))
    files_list = []
    all_files = []
    if not os.path.exists(output_dir):
        # output directory does not exist, create it first
        os.makedirs(output_dir)
    with ftputil.FTPHost(vampire.get('CHIRPS', 'ftp_address'),
                         vampire.get('CHIRPS', 'ftp_user'),
                         vampire.get('CHIRPS', 'ftp_password')) as ftp_host:
        ftp_host.chdir(_ftp_dir)
        if interval.lower() == 'daily':
            # daily files are in directory by year so create new list of files
            # loop through years in dates and get from the correct directory
            _years = []
            _ftp_years = ftp_host.listdir(ftp_host.curdir)
            if start_date is not None:
                if end_date is not None:
                    # have both start and end dates, create list of years
                    for i in range(start_date.year, start_date.year + (end_date.year - start_date.year)):
                        _years.append(start_date.year + i)
                else:
                    # have start date but no end date. Find last year available and download all until then
                    for fd in _ftp_years:
                        if int(fd) >= start_date.year:
                            _years.append(int(fd))
            else:
                # no start date
                if end_date is not None:
                    # have end date but no start date. Find all years until end_date
                    for fd in _ftp_years:
                        if int(fd) <= end_date.year:
                            _years.append(int(fd))
                else:
                    # no start or end date.
                    if dates:
                        # have list of dates
                        for d in dates:
                            _years.append(int(d.split('-')[0]))
            _years = set(_years)
            for y in _years:
                ftp_host.chdir(ftp_host.path.join(_ftp_dir, str(y)))
                _files = ftp_host.listdir(ftp_host.curdir)
                if _files is not None:
                    for f in _files:
                        _f_abs = ftp_host.path.join(ftp_host.getcwd(), f)
                        all_files.append(_f_abs)
        else:
            all_files = ftp_host.listdir(ftp_host.curdir)
            #print(all_files)
        regex = re.compile(vampire.get('CHIRPS', 'global_{0}_pattern'.format(interval)))
        for f in all_files:
            download = False
            result = regex.match(os.path.basename(f))
            f_date = None
            if result is not None:
                if interval.lower() == 'monthly' or interval.lower() == 'dekad' or interval.lower() == 'daily':
                    f_year = result.group('year')
                    f_month = result.group('month')
                    f_day = 1
                    if interval.lower() == 'daily':
                        f_day = result.group('day')
                    f_date = datetime.datetime(int(f_year), int(f_month), int(f_day))
                elif interval.lower() == 'seasonal':
                    f_year = result.group('year')
                    f_month = result.group('season')[0:2]
                    f_date = datetime.datetime(int(f_year), int(f_month), 1)
                else:
                    raise ValueError, "Interval not recognised."
                if dates:
                    if '{0}-{1}'.format(f_year, f_month) in dates:
                        download = True
                elif (start_date is None) and (end_date is None):
                    download = True
                elif start_date is None:
                    # have end_date, check date is before
                    if f_date is not None:
                        if f_date <= end_date:
                            download = True
                elif end_date is None:
                    # have start_date, check date is after
                    if f_date is not None:
                        if f_date >= start_date:
                            download = True
                else:
                    # have both start and end date
                    if f_date is not None:
                        if f_date >= start_date and f_date <= end_date:
                            download = True
                if download:
                    if int(f_year) > 1980:
                        #print(f)
                        #print(f_year)
                        #print(f_month)

                        if ftp_host.path.isfile(f):
                            local_f = os.path.join(output_dir, os.path.basename(f))
                            tifdata = os.path.join(tiffolder, os.path.basename(f))
                            if not os.path.isfile(local_f) or overwrite:
                                logging.debug(datelog+": downloading data "+local_f)
                                ftp_host.download(f, local_f)  # remote, local
                                files_list.append(os.path.basename(f))
                                with gzip.open(local_f, 'rb') as _in_file:
                                    s = _in_file.read()
                                _path_to_store = os.path.splitext(tifdata)[0] #f[:-3]
                                print(_path_to_store)
                                if not os.path.isfile(_path_to_store) or overwrite:
                                    with open(_path_to_store, 'wb') as _out_file:
                                        _out_file.write(s)
                            else:
                                logging.debug(datelog+": "+f+" is available")

        logging.debug(datelog+": Download CHIRPS Data finished..")
        logging.debug(datelog+": Continue checking on rainfall anomaly and standard precipitattion index data..")
