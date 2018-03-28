import os
os.chdir("D:\\PyCharm Projects\\SingleProject")

import arcpy
from arcpy.sa import *
import VampireDefaults
import mosaicDataset
import logging
import time
import ast

def update_mosaic_vhi_crop(country):
    datelog = time.strftime('%c')
    vp = VampireDefaults.VampireDefaults()
    geodatabase = vp.get('geodatabase', 'config')
    config = ast.literal_eval(geodatabase)
    file_path = config['gdbpath']
    directory = file_path+'\\'+country
    folder = 'D:\\IDN_GIS\\01_Data\\03_Regional\\'+country
    products = ['vhi_crop_1_month']
    for product in products:
        productFolder = folder+"\\"+product
        countryData = []
        gdbname = directory+'\\'+product+'.gdb'
        MDS = gdbname + '\\' + product
        mosaicDataset.addRastertoMDS(MDS, productFolder)
        #mosaicDataset.addDateField(MDS)
        mosaicDataset.updateDateField(MDS, product)
        arcpy.CheckInExtension("spatial")
        print("updating date")