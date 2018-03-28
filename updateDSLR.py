import os
os.chdir("D:\\PyCharm Projects\\SingleProject")

import dslr
import updateIMERGData
import maxdslr
import time
import logging
import datetime
from datetime import date


LOG_FILENAME = os.path.join("D:\\PyCharm Projects\\SingleProject\\log", 'dslr_log_'+time.strftime("%Y%m%d")+'.log')
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
datelog = time.strftime('%c')
imerg_nc4_folder = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\IMERG\\daily\\NC4'
tiffolder = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\IMERG\\daily\\tif'
rainfalfolder = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\IMERG\\daily\\rainday_1'
dslrfolder = "D:\\IDN_GIS\\01_Data\\01_Global\\VampireData\\global_dslr_1mm"
country = 'idn'

start_checking = date(2017,11,1)
date_end = date.today() - datetime.timedelta(days=2)

updateIMERGData.checking_imerg_data(imerg_nc4_folder,tiffolder)
logging.debug(datelog+" : Finish updating IMERG data----------------------------")
dslr.rainydays(tiffolder, 1, rainfalfolder)
logging.debug(datelog+" : Finish updating Rainy data----------------------------")
while start_checking <= date_end:
    dslrfilename = 'dslr_{0:0=2d}mm_threshold_{1}.tif'.format(1, start_checking.strftime('%Y%m%d'))
    logging.debug(datelog+" : start processing DSLR--------------- ")
    if not os.path.exists(os.path.join(dslrfolder,dslrfilename)):
        print("processing "+str(start_checking))
        dslrdate = start_checking.strftime('%Y%m%d')
        dslr.calculatedslr(dslrdate, 1, 90, rainfalfolder, dslrfolder)
    else:
        print(str(start_checking)+ " is available")
    start_checking = start_checking + datetime.timedelta(days=1)
logging.debug(datelog+" : Finish updating DSLR data----------------------------")
dslr.subsetdslr(country, 1)
calmonth = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
calyear = ['2014', '2015', '2016', '2017']
for i in calmonth:
    for j in calyear:
        maxdslr.max_monthly_dslr('idn',i,j, 1)

