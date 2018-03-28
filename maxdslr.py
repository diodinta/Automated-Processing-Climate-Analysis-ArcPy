import os
import mosaicDataset
import arcpy
from arcpy.sa import *
from datetime import date
import time
import logging

LOG_FILENAME = os.path.join("D:\\PyCharm Projects\\SingleProject\\log", 'dslr_log_'+time.strftime("%Y%m%d")+'.log')
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
datelog = time.strftime('%c')

def max_monthly_dslr(country, month, year, threshold):
    countryfolder = "D:\\IDN_GIS\\01_Data\\03_Regional\\"+country+"\\DSLR_"+str(threshold).zfill(2)+"mm"
    max_country_folder = "D:\\IDN_GIS\\01_Data\\03_Regional\\"+country+"\\DSLR_"+str(threshold).zfill(2)+"mm_monthly_max"
    result_filename = '{0}_cli_dslr_{1}mm_threshold_{2}.{3}.max.tif'.format(country, str(threshold).zfill(2), year, month)
    if not os.path.exists(os.path.join(max_country_folder,result_filename)):
        logging.debug(datelog+" : max dslr "+result_filename+ " is not available. Processing.....")
        file_list = []
        for dslrfile in os.listdir(countryfolder):
            if dslrfile.endswith(".tif") or dslrfile.endswith(".tiff"):
                datestring = dslrfile.split("_")
                filemonth = datestring[5][4:6]
                fileyear = datestring[5][0:4]
                #print(filemonth, fileyear)
                if month == filemonth and year == fileyear:
                    file_list.append(os.path.join(countryfolder, dslrfile))
        lastday = mosaicDataset.eomday(int(year), int(month))
        firstdate = date(int(year), int(month), 1)
        lastdate = date(int(year), int(month), lastday)
        day_count_delta = lastdate - firstdate
        day_count = day_count_delta.days + 1
        if day_count == len(file_list):
            logging.debug(datelog+" : the data required to calculate max dslr are available. Calculating max DSLR....")
            arcpy.CheckOutExtension("Spatial")
            #print(result_filename)
            outCellStatistics = CellStatistics(file_list, "MAXIMUM", "DATA")
            outCellStatistics.save(os.path.join(max_country_folder, result_filename))
            arcpy.CheckInExtension("spatial")
        else:
            logging.debug(datelog+" : incomplete data to calculate max dslr for month = " +month+" and year = "+year)
            logging.debug(datelog+" : data available = "+str(len(file_list))+ " while the required data is "+str(day_count))
    else:
        logging.debug(datelog+" : max dslr for month = " +month+" and year = "+year+ " is available")

# calmonth = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
# calyear = ['2014', '2015', '2016', '2017']
# for i in calmonth:
#     for j in calyear:
#         max_monthly_dslr('idn',i,j, 1)