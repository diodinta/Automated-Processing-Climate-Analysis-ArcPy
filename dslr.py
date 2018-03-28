import os
os.chdir("D:\\PyCharm Projects\\SingleProject")

import datetime
import arcpy
from arcpy.sa import *
from datetime import date
import VampireDefaults
import mosaicDataset
import time
import logging

LOG_FILENAME = os.path.join("D:\\PyCharm Projects\\SingleProject\\log", 'dslr_log_'+time.strftime("%Y%m%d")+'.log')
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
datelog = time.strftime('%c')

def rainydays(tiffolder, threshold, rainydayFolder):
    print("start processing rainy data........ ")
    sr = arcpy.SpatialReference(4326)
    tifdata = []
    rainydata = []
    for tdata in os.listdir(tiffolder):
        if tdata.endswith(".tif") or tdata.endswith(".tiff"):
            parseString = tdata.split('.')
            parse = parseString[4]
            tifdate = parse[0:8]
            tifdata.append(tifdate)
    for rdata in os.listdir(rainydayFolder):
        if rdata.endswith(".tif") or rdata.endswith(".tiff"):
            parseStringtdata = rdata.split('.')
            rainydate = parseStringtdata[1]
            rainydata.append(rainydate)
    for i in tifdata:
        print("checking rainday data for date " +i)
        if i not in rainydata:
            print("rainday data for date " +i+ " has not been calculated")
            print("calculating rainday for date " +i)
            tifname = '3B-DAY-L.MS.MRG.3IMERG.{0}-S000000-E235959.V05.nc4.tif'.format(i)
            rainyfilename = 'raindays.{0}.threshold_{1}mm.tif'.format(i,threshold)
            tiffile = os.path.join(tiffolder, tifname)
            arcpy.CheckOutExtension("spatial")
            outCon = Con(Raster(tiffile) > int(threshold),1,0)
            outCon.save(os.path.join(rainydayFolder, rainyfilename))
            arcpy.DefineProjection_management(os.path.join(rainydayFolder, rainyfilename),sr)
            print("file "+rainyfilename+" is created")
            arcpy.CheckInExtension("spatial")
    print("processing rainy days for threshold "+str(threshold)+" is  completed--------")


# tiffolder = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\IMERG\\daily\\tif'
# rainfalfolder = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\IMERG\\daily\\rainday_1'
# rainydays(tiffolder, 1, rainfalfolder)

def calculatedslr(dslrdate, threshold, num_of_days, raindayfolder, dslrfolder):
    dslrfilename = 'dslr_{0:0=2d}mm_threshold_{1}.tif'.format(threshold, dslrdate)
    print("start processing DSLR--------------- ")
    if not os.path.exists(os.path.join(dslrfolder,dslrfilename)):
        arcpy.CheckOutExtension("spatial")
        print("DSLR file for date " +dslrdate+ " has not been calculated")
        print("calculating DSLR file for date "+dslrdate)
        dslrdateformatted = date(int(dslrdate[0:4]), int(dslrdate[4:6]), int(dslrdate[6:8]))
        NumDaysRain = int(num_of_days)+1
        index = []
        rangedata = 0
        for rainyfilename in os.listdir(raindayfolder):
            if rainyfilename.endswith(".tif") or rainyfilename.endswith(".tiff"):
                arcpy.CalculateStatistics_management(os.path.join(raindayfolder,rainyfilename))
                get_min_value = arcpy.GetRasterProperties_management(os.path.join(raindayfolder,rainyfilename), "MINIMUM")
                get_max_value = arcpy.GetRasterProperties_management(os.path.join(raindayfolder,rainyfilename), "MAXIMUM")
                max_value = int(get_max_value.getOutput(0))
                min_value = int(get_min_value.getOutput(0))
                if min_value == 0 and max_value == 1:
                    parseStringRain = rainyfilename.split('.')
                    parseRain = parseStringRain[1]
                    yearRain = int(parseRain[0:4])
                    monthRain = int(parseRain[4:6])
                    dayRain = int(parseRain[6:8])
                    filedateRain = date(yearRain, monthRain, dayRain)
                    if filedateRain < dslrdateformatted:
                        rangedata = rangedata+1; # to check if the data is in range
                        if filedateRain > dslrdateformatted - datetime.timedelta(days=num_of_days+1): #to limit the data calculation
                            index.append(os.path.join(raindayfolder, rainyfilename))
                else:
                    print(rainyfilename + " is not a proper rainyday data. max value must be 1 and min value must be 0.")

        if len(index)>=num_of_days:
            print("rainday data "+str(len(index))+" before DSLR date are complete. calculating DSLR....")
            indexReverse = sorted(index, reverse=True)
            #print(indexReverse)
            outHighestPosition = HighestPosition(indexReverse)
            #outHighestPosition.save(os.path.join(dslrfolder, 'temp.tif'))
            minusOne = outHighestPosition - 1
            minusOne.save(os.path.join(dslrfolder, dslrfilename))
            print("file DaysSinceLastRain.tif is created. Process completed")
        else:
            print("the sum of the data " +str(len(index))+ " is less than the num of days = "+str(num_of_days))
        arcpy.CheckInExtension("spatial")
    else:
        print("DSLR file for date " +dslrdate+ " exists")


def subsetdslr(countrycode, threshold):
    vp = VampireDefaults.VampireDefaults()
    subsetFile = vp.get('IMERG_subset', countrycode)
    logging.debug(datelog+" : start subset data for country "+countrycode+ " on " +str(threshold)+ " threshold--------")
    globalfolder = "D:\\IDN_GIS\\01_Data\\01_Global\\VampireData\\global_dslr_"+str(threshold)+"mm"
    countryfolder = "D:\\IDN_GIS\\01_Data\\03_Regional\\"+countrycode+"\\DSLR_"+str(threshold).zfill(2)+"mm"
    MDS = "D:\\IDN_GIS\\05_Analysis\\04_Geodatabases\\idn\\DSLR_"+str(threshold).zfill(2)+"mm.gdb\\DSLR_"+str(threshold).zfill(2)+"mm"
    global_data = []
    country_data = []
    for globaldata in os.listdir(globalfolder):
        if globaldata.endswith(".tif") or globaldata.endswith(".tiff"):
            prefixname = countrycode+"_cli_"+globaldata
            global_data.append(prefixname)
    for countrydata in os.listdir(countryfolder):
        if countrydata.endswith(".tif") or countrydata.endswith(".tiff"):
            country_data.append(countrydata)
    #print(globaldata)
    #print(country_data)
    for i in global_data:
        if i not in country_data:
            print(datelog+" : file DSLR "+i+ " for country "+countrycode+ " is not available")
            logging.debug(datelog+" : Cropping DSLR data.......")
            globalname1 = i.split("_")
            globalname1.remove(countrycode)
            globalname1.remove('cli')
            globalname = "_".join(globalname1)
            globaldataloc = os.path.join(globalfolder,globalname)
            arcpy.CheckOutExtension("spatial")
            extractbymask = ExtractByMask(globaldataloc, subsetFile)
            extractbymask.save(os.path.join(countryfolder, i))
            logging.debug(datelog+" : Cropping DSLR data finished. File "+i+ "is created.......")
            arcpy.CheckInExtension("spatial")
    mosaicDataset.addRastertoMDS(MDS, countryfolder)
    mosaicDataset.addDateField(MDS)
    mosaicDataset.updateDateField(MDS, "DSLR_"+str(threshold).zfill(2)+"mm")



