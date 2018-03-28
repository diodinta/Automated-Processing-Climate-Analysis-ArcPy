import os
import VampireDefaults
import re
from arcpy.sa import *
import arcpy

vp = VampireDefaults.VampireDefaults()
dir = ['01','02','03','04', '05', '06', '07', '08', '09', '10', '11', '12']
datadir = 'D:\\IDN_GIS\\01_Data\\02_IDN\\Rasters\\Climate\\Temperature\\MODIS\\MOD11C3.006\\LST_AVG_YEAR_MONTH_WGS84'
stddir = 'D:\\IDN_GIS\\01_Data\\02_IDN\\Rasters\\Climate\\Temperature\\MODIS\\MOD11C3.006\\Satistics_By_Month'
monthly_pattern = vp.get('MODIS_LST', 'lst_average_pattern') # global_monthly_pattern, global_seasonal_pattern, global_dekad_pattern

Moregex_dekad = re.compile(monthly_pattern)

def monthly():
    dictionary = {}
    for i in dir:
        index = i
        content = []
        for file_dekad in os.listdir(datadir):
            if file_dekad.endswith(".tif") or file_dekad.endswith(".tiff"):
                Moresult_dekad = Moregex_dekad.match(file_dekad)
                Dmonth = Moresult_dekad.group('month')
                if Dmonth == i:
                    content.append(os.path.join(datadir, file_dekad))
        dictionary[index] = content

    # =========================Create STD DEKAD file=================================#
    for k in dir:
        index = k
        listoffile = dictionary[index]
        ext = ".tif"
        newfilename_month_min = 'MOD11C3.2000-2015.{0}.min{1}'.format(k, ext)
        newfilename_month_max = 'MOD11C3.2000-2015.{0}.max{1}'.format(k, ext)
        newfilename_month_avg = 'MOD11C3.2000-2015.{0}.avg{1}'.format(k, ext)

        if arcpy.Exists(os.path.join(stddir, newfilename_month_min)):
            print(newfilename_month_min + " exists")
        else:
            arcpy.CheckOutExtension("spatial")
            outCellStatistics = CellStatistics(listoffile, "MINIMUM", "DATA")
            outCellStatistics.save(os.path.join(stddir, newfilename_month_min))
            print(newfilename_month_min + " is created")
            arcpy.CheckInExtension("spatial")

        if arcpy.Exists(os.path.join(stddir, newfilename_month_max)):
            print(newfilename_month_max + " exists")
        else:
            arcpy.CheckOutExtension("spatial")
            outCellStatistics_avg = CellStatistics(listoffile, "MAXIMUM", "DATA")
            outCellStatistics_avg.save(os.path.join(stddir, newfilename_month_max))
            print(newfilename_month_max + " is created")
            arcpy.CheckInExtension("spatial")

        if arcpy.Exists(os.path.join(stddir, newfilename_month_avg)):
            print(newfilename_month_avg + " exists")
        else:
            arcpy.CheckOutExtension("spatial")
            outCellStatistics_avg = CellStatistics(listoffile, "MEAN", "DATA")
            outCellStatistics_avg.save(os.path.join(stddir, newfilename_month_avg))
            print(newfilename_month_avg + " is created")
            arcpy.CheckInExtension("spatial")

monthly()