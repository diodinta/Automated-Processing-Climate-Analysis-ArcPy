import os
import VampireDefaults
import re
from arcpy.sa import *
import arcpy

vp = VampireDefaults.VampireDefaults()
dir = ['01','02','03','04', '05', '06', '07', '08', '09', '10', '11', '12']
dirseasonal = ['010203','020304','030405','040506', '050607', '060708', '070809', '080910', '091011', '101112', '111201', '120102']
dekad = ['1','2','3']

#====================== change following data before running the script ==========================#
datadir = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Seasonal\\TifData'
stddir = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Seasonal\\NewStatististics'
dekad_pattern = vp.get('CHIRPS', 'global_seasonal_pattern') # global_monthly_pattern, global_seasonal_pattern, global_dekad_pattern


Moregex_dekad = re.compile(dekad_pattern)


#===================================create list file of DEKAD============================#
def dekadLT():
    dictionary = {}
    for i in dir:
        for j in dekad:
            index = i+j
            content = []
            for file_dekad in os.listdir(datadir):
                if file_dekad.endswith(".tif") or file_dekad.endswith(".tiff"):
                    Moresult_dekad = Moregex_dekad.match(file_dekad)
                    Dmonth = Moresult_dekad.group('month')
                    Ddekad = Moresult_dekad.group('dekad')
                    if Ddekad == j and Dmonth == i:
                        content.append(os.path.join(datadir, file_dekad))
            dictionary[index] = content

#=========================Create STD DEKAD file=================================#

    for k in dir:
        for l in dekad:
            index = k + l
            listoffile = dictionary[index]
            ext = ".tif"
            newfilename_dekad = 'chirps-v2.0.1981-2016.{0}.{1}.dekad.36yrs.std{2}'.format(k, l, ext)
            newfilename_dekad_avg = 'chirps-v2.0.1981-2016.{0}.{1}.dekad.36yrs.avg{2}'.format(k, l, ext)
            print(newfilename_dekad)

            if arcpy.Exists(os.path.join(stddir, newfilename_dekad)):
                print(newfilename_dekad + " exists")
            else:
                arcpy.CheckOutExtension("spatial")
                outCellStatistics = CellStatistics(listoffile, "STD", "DATA")
                outCellStatistics.save(os.path.join(stddir, newfilename_dekad))
                arcpy.CheckInExtension("spatial")

            if arcpy.Exists(os.path.join(stddir, newfilename_dekad_avg)):
                print(newfilename_dekad_avg + " exists")
            else:
                arcpy.CheckOutExtension("spatial")
                outCellStatistics_avg = CellStatistics(listoffile, "MEAN", "DATA")
                outCellStatistics_avg.save(os.path.join(stddir, newfilename_dekad_avg))
                arcpy.CheckInExtension("spatial")

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
        newfilename_dekad = 'chirps-v2.0.1981-2016.{0}.monthly.36yrs.std{1}'.format(k, ext)
        newfilename_dekad_avg = 'chirps-v2.0.1981-2016.{0}.monthly.36yrs.avg{1}'.format(k, ext)
        print(newfilename_dekad)

        if arcpy.Exists(os.path.join(stddir, newfilename_dekad)):
            print(newfilename_dekad + " exists")
        else:
            arcpy.CheckOutExtension("spatial")
            outCellStatistics = CellStatistics(listoffile, "STD", "DATA")
            outCellStatistics.save(os.path.join(stddir, newfilename_dekad))
            arcpy.CheckInExtension("spatial")

        if arcpy.Exists(os.path.join(stddir, newfilename_dekad_avg)):
            print(newfilename_dekad_avg + " exists")
        else:
            arcpy.CheckOutExtension("spatial")
            outCellStatistics_avg = CellStatistics(listoffile, "MEAN", "DATA")
            outCellStatistics_avg.save(os.path.join(stddir, newfilename_dekad_avg))
            arcpy.CheckInExtension("spatial")

def seasonal():
    dictionary = {}
    for i in dirseasonal:
        index = i
        content = []
        for file_dekad in os.listdir(datadir):
            if file_dekad.endswith(".tif") or file_dekad.endswith(".tiff"):
                print(file_dekad)
                Moresult_dekad = Moregex_dekad.match(file_dekad)
                Dmonth = Moresult_dekad.group('season')
                if Dmonth == i:
                    content.append(os.path.join(datadir, file_dekad))
        dictionary[index] = content
    print(dictionary)

    # =========================Create STD DEKAD file=================================#
    for k in dirseasonal:
        index = k
        listoffile = dictionary[index]
        print(listoffile)
        ext = ".tif"
        newfilename_dekad = 'chirps-v2.0.1981-2016.{0}.seasonal.36yrs.std{1}'.format(k, ext)
        newfilename_dekad_avg = 'chirps-v2.0.1981-2016.{0}.seasonal.36yrs.avg{1}'.format(k, ext)
        print(newfilename_dekad)

        if arcpy.Exists(os.path.join(stddir, newfilename_dekad)):
            print(newfilename_dekad + " exists")
        else:
            arcpy.CheckOutExtension("spatial")
            outCellStatistics = CellStatistics(listoffile, "STD", "DATA")
            outCellStatistics.save(os.path.join(stddir, newfilename_dekad))
            arcpy.CheckInExtension("spatial")

        if arcpy.Exists(os.path.join(stddir, newfilename_dekad_avg)):
            print(newfilename_dekad_avg + " exists")
        else:
            arcpy.CheckOutExtension("spatial")
            outCellStatistics_avg = CellStatistics(listoffile, "MEAN", "DATA")
            outCellStatistics_avg.save(os.path.join(stddir, newfilename_dekad_avg))
            arcpy.CheckInExtension("spatial")

seasonal()

