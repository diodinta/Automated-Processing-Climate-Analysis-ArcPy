import calendar
import os
import arcpy
from arcpy.sa import *

def JulianDate_to_MMDDYYY(y,jd):
    month = 1
    day = 0
    while jd - calendar.monthrange(y,month)[1] > 0 and month <= 12:
        jd = jd - calendar.monthrange(y,month)[1]
        month = month + 1
    return month,jd,y

def kelvintocelcius(folder, outputfolder):
    for filename in os.listdir(folder):
        if filename.endswith(".tif") or filename.endswith(".tiff"):
            fileKelvin = os.path.join(folder,filename)
            celciusfile = (Raster(fileKelvin)*0.02) - 273.15
            celciusfile.save(os.path.join(outputfolder, filename))

def LSTAverage(day,night,result):
    for filename in os.listdir(day):
        if filename.endswith(".tif") or filename.endswith(".tiff"):
            split = filename.split('.')
            daydate = split[1]
            print(daydate)
            for Nfilename in os.listdir(night):
                if Nfilename.endswith(".tif") or Nfilename.endswith(".tiff"):
                    Nsplit = Nfilename.split('.')
                    year = int(Nsplit[1][1:5])
                    date = int(Nsplit[1][5:8])
                    print(year, day)
                    month, jd, y = JulianDate_to_MMDDYYY(year, date)
                    twodigitmonth = str(month).zfill(2)
                    twodigitday = str(jd).zfill(2)
                    print(twodigitmonth,twodigitday)
                    nightdate = Nsplit[1]
                    if daydate == nightdate:
                        print("day file  "+filename+" match with "+Nfilename)
                        arcpy.CheckOutExtension("spatial")
                        ext = ".tif"
                        newfilename = 'idn_cli_MOD11C3.{0}.{1}.{2}.avg{3}'.format(y, twodigitmonth, twodigitday, ext)
                        print(newfilename)
                        Calculation =  CellStatistics([Raster(os.path.join(day,filename)),Raster(os.path.join(night,Nfilename))], "MEAN", "DATA")
                        Calculation.save(os.path.join(result, newfilename))
                        print("Average file "+newfilename+" created")
                        arcpy.CheckInExtension("spatial")
                    continue
                else:
                    continue
        else:
            continue

def mod13a3Process(folder, index, outputFolder, product):
    for filename in os.listdir(folder):
        if filename.endswith(".hdf"):
            print("processing "+filename)
            arcpy.env.workspace = outputFolder
            arcpy.CheckOutExtension("spatial")
            inputRaster = os.path.join(folder,filename)
            outputEVI = '{0}.{1}.tif'.format(filename, product)
            if arcpy.Exists(os.path.join(outputFolder, outputEVI)):
                print(outputEVI + " exists")
            else:
                EVIfile = arcpy.ExtractSubDataset_management(inputRaster,outputEVI,index)
            arcpy.CheckInExtension("spatial")
        else:
            continue

def combineMODData(folder, outputFolder, subset):
    processedDate = []
    for filename in os.listdir(folder):
        print(filename)
        if filename.endswith(".tif") or filename.endswith(".tiff"):
            split = filename.split('.')
            filedate = split[1]
            year = int(split[1][1:5])
            date = int(split[1][5:8])
            month, jd, y = JulianDate_to_MMDDYYY(year, date)
            twodigitmonth = str(month).zfill(2)
            twodigitday = str(jd).zfill(2)
            if filedate not in processedDate:
                processedDate.append(filedate)
                combinedData=[]
                combinedData.append(os.path.join(folder, filename))
                for SFilename in os.listdir(folder):
                    if SFilename.endswith(".tif") or SFilename.endswith(".tiff"):
                        if os.path.join(SFilename) not in combinedData:
                            split1 = SFilename.split('.')
                            Sfiledate = split1[1]
                            if Sfiledate == filedate:
                                combinedData.append(os.path.join(folder, SFilename))
                            else:
                                continue
                print(combinedData)
                sumofdata = len(combinedData)
                stringcombined = combinedData[0]
                x = 1
                while x > 0 and x < sumofdata:
                    stringcombined = stringcombined + ";" +combinedData[x]
                    x = x+1
                print(stringcombined)
                sr = arcpy.SpatialReference(4326)
                arcpy.env.workspace = folder
                newfilename = 'phy_MOD13A3.{0}.{1}.{2}_006.1_km_monthly_EVI.tif'.format(year, twodigitmonth, twodigitday )
                idnfilename = 'idn_phy_MOD13A3.{0}.{1}.{2}_006.1_km_monthly_EVI.tif'.format(year, twodigitmonth,
                                                                                        twodigitday)
                julianname = '{0}.{1}.006.250m_16_days_NDVI.tif'.format(split[0], filedate)
                arcpy.CheckOutExtension("spatial")
                arcpy.MosaicToNewRaster_management(input_rasters= combinedData, output_location = outputFolder, raster_dataset_name_with_extension=newfilename, coordinate_system_for_the_raster= sr, pixel_type='16_BIT_SIGNED', number_of_bands='1' )
                arcpy.DefineProjection_management(os.path.join(outputFolder,newfilename), sr)
                outExtractByMask = ExtractByMask(os.path.join(outputFolder,newfilename), subset)

                # ---- Uncomment code when result filename is in julian date---- #
                # if arcpy.Exists(os.path.join(outputFolder, julianname)):
                #     print(julianname + " exists")
                # else:
                #     outExtractByMask.save(os.path.join(outputFolder, julianname))

                if arcpy.Exists(os.path.join(outputFolder, idnfilename)):
                    print(idnfilename + " exists")
                else:
                    outExtractByMask.save(os.path.join(outputFolder, idnfilename))

                arcpy.CheckInExtension("spatial")

def lst_processing(mod11c3_file):
    lst_day_name = '{0}.day.tif'.format(mod11c3_file)
    lst_day = arcpy.ExtractSubDataset_management(mod11c3_file,outputEVI,0)
    lst_night = 2


# hdf_folder = 'D:\\IDN_GIS\\01_Data\\02_IDN\\Rasters\\Physical\\Vegetation\\MOD13A3.006\\HDF'
# tif_folder = 'D:\\IDN_GIS\\01_Data\\02_IDN\\Rasters\\Physical\\Vegetation\\MOD13A3.006\\TIF'
# idn_evi_folder = 'D:\\IDN_GIS\\01_Data\\02_IDN\\Rasters\\Physical\\Vegetation\\MOD13A3.006\\IDN.EVI'
# idn_subset_shp = 'D:\\IDN_GIS\\01_Data\\02_IDN\\ShapeFiles\\Boundaries\\Subset\\MODIS\\idn_bnd_subset_modis_250m_grid_diss_a.shp'
#
# mod13a3Process(hdf_folder, 1, tif_folder, 'EVI')
# combineMODData(tif_folder, idn_evi_folder, idn_subset_shp)
