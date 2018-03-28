import os
os.chdir("D:\\PyCharm Projects\\SingleProject")

import arcpy
from arcpy.sa import *
import CreateRASPI
import downloadData
import VampireDefaults
import ast
import mosaicDataset
import logging
import time

def updateDataCHIRPS(interval, output_dir, tif_data):
    downloadData.downloadCHIRPSData(interval, output_dir, tif_data)
    arcpy.CheckOutExtension("spatial")
    CreateRASPI.dekadRASPI()
    CreateRASPI.seasonalRASPI()
    CreateRASPI.monthlyRASPI()
    arcpy.CheckInExtension("spatial")

def subsetByCountry(country):
    #LOG_FILENAME1 = os.path.join("D:\\PyCharm Projects\\SingleProject\\log", 'vampire_log_'+country+'_'+time.strftime("%Y%m%d")+'.log')
    #logging.basicConfig(filename=LOG_FILENAME1,level=logging.DEBUG)
    datelog = time.strftime('%c')
    vp = VampireDefaults.VampireDefaults()
    subsetFile = vp.get('CHIRPS_subset', country)
    geodatabase = vp.get('geodatabase', 'config')
    config = ast.literal_eval(geodatabase)
    file_path = config['gdbpath']
    directory = file_path+'\\'+country
    folderglobal = 'D:\\IDN_GIS\\01_Data\\01_Global\\VampireData'
    folder = 'D:\\IDN_GIS\\01_Data\\03_Regional\\'+country
    products = ['rainfall_anomaly_1_month', 'rainfall_anomaly_3_month', 'rainfall_anomaly_dekad', 'spi_1_month', 'spi_3_month', 'spi_dekad']
    for product in products:
        productFolder = folder+"\\"+product
        countryData = []
        globalproductfolder = folderglobal+'\\'+'global_'+product
        globaldata = []
        gdbname = directory+'\\'+product+'.gdb'
        MDS = gdbname + '\\' + product
        for gdata in os.listdir(globalproductfolder):
            if gdata.endswith(".tif") or gdata.endswith(".tiff"):
                NameConverting = country +'_cli_' +gdata
                globaldata.append(NameConverting)
        for data in os.listdir(productFolder):
            if data.endswith(".tif") or data.endswith(".tiff"):
                countryData.append(data)
        for i in globaldata:
            if i not in countryData:
                globalname1 = i.split("_")
                globalname1.remove(country)
                globalname1.remove('cli')
                globalname = "_".join(globalname1)
                gdataloc = os.path.join(globalproductfolder, globalname)
                arcpy.CheckOutExtension("spatial")
                extractbymask = ExtractByMask(gdataloc, subsetFile)
                extractbymask.save(os.path.join(productFolder, i))
                #logging.debug(datelog+" :updating " + product, globalname, gdbname, MDS)
                mosaicDataset.addRastertoMDS(MDS, productFolder)
                #mosaicDataset.addDateField(MDS)
                mosaicDataset.updateDateField(MDS, product)
                arcpy.CheckInExtension("spatial")
            else:
                logging.debug(datelog+" : "+i+" is available")
                print("data available")
        print("updating date")




updateDataCHIRPS('monthly', 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Monthly\\GZData','D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Monthly\\TifData' )
updateDataCHIRPS('dekad', 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Dekad\\GZData','D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Dekad\\TifData' )
updateDataCHIRPS('seasonal', 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Seasonal\\GZData','D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Seasonal\\TifData' )

subsetByCountry('idn')


