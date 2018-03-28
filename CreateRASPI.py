import os
os.chdir("D:\\PyCharm Projects\\SingleProject")

import VampireDefaults
import arcpy
from arcpy.sa import *
import re
import time
import logging

LOG_FILENAME = os.path.join("D:\\PyCharm Projects\\SingleProject\\log", 'vampire_log_'+time.strftime("%Y%m%d")+'.log')
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
datelog = time.strftime('%c')
vp = VampireDefaults.VampireDefaults()
base_product_name = vp.get('CHIRPS','base_data_name')
logging.debug(datelog+": Updating rainfall anomaly and Standard Precipitation Index starts.....")

def monthlyRASPI():
    average_pattern = vp.get('CHIRPS_Longterm_Average','global_lta_monthly_pattern')
    std_pattern = vp.get('CHIRPS_Longterm_Standard_Deviation','global_ltsd_monthly_pattern')
    monthly_pattern = vp.get('CHIRPS', 'global_monthly_pattern')
    AVGdir = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Monthly\\NewStatistics\\avg'
    STDdir = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Monthly\\NewStatistics\\std'
    Monthlydir = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Monthly\\TifData'
    ResultDir = 'D:\\IDN_GIS\\01_Data\\01_Global\\VampireData\\global_rainfall_anomaly_1_month'
    ResultDirSPI = 'D:\\IDN_GIS\\01_Data\\01_Global\\VampireData\\global_spi_1_month'
    AVGregex = re.compile(average_pattern)
    STDregex = re.compile(std_pattern)
    Moregex = re.compile(monthly_pattern)
    for Mfilename in os.listdir(Monthlydir):
        if Mfilename.endswith(".tif"):
            Moresult = Moregex.match(Mfilename)
            Mmonth = Moresult.group('month')
            for Afilename in os.listdir(AVGdir):
                if Afilename.endswith(".tif"):
                    if AVGregex.match(Afilename):
                        AVGresult = AVGregex.match(Afilename)
                        Amonth = AVGresult.group('month')
                        if Amonth == Mmonth:
                            #print(Mfilename+" match with "+Afilename)
                            AVGFile = os.path.join(AVGdir, Afilename)
                            MoFile = os.path.join(Monthlydir, Mfilename)
                            month = Amonth
                            year = Moresult.group('year')
                            ext = ".tif"
                            newfilename = '{0}.{1}.{2}.ratio_anom{3}'.format(base_product_name, year, month, ext)
                            if arcpy.Exists(os.path.join(ResultDir, newfilename)):
                                logging.debug(datelog+": file " + newfilename + " is already exist")
                            else:
                                newRaster = Int(100 * Raster(MoFile) / Raster(AVGFile))
                                newRaster.save(os.path.join(ResultDir, newfilename))
                                logging.debug(datelog+":file " + newfilename + " is created")

                            for Sfilename in os.listdir(STDdir):
                                if Sfilename.endswith(".tif"):
                                    if STDregex.match(Sfilename):
                                        STDresult = STDregex.match(Sfilename)
                                        Smonth = STDresult.group('month')
                                        if Smonth == Mmonth:
                                            #print(Mfilename + " match with " + Afilename +" match with " +Sfilename)
                                            AVGFile = os.path.join(AVGdir, Afilename)
                                            MoFile = os.path.join(Monthlydir, Mfilename)
                                            SPIFile = os.path.join(STDdir, Sfilename)
                                            month = Amonth
                                            year = Moresult.group('year')
                                            ext = ".tif"
                                            spifilename = '{0}.{1}.{2}.spi{3}'.format(base_product_name, year, month, ext)
                                            if arcpy.Exists(os.path.join(ResultDirSPI, spifilename)):
                                                logging.debug(datelog+": file " + newfilename + " is already exist")
                                            else:
                                                SPIRaster = (Raster(MoFile) - Raster(AVGFile)) / Raster(SPIFile)
                                                SPIRaster.save(os.path.join(ResultDirSPI, spifilename))
                                                logging.debug(datelog+": file " + newfilename + " is created")
                                        continue
                                else:
                                    continue

                        continue
                else:
                    continue
            continue
        else:
            continue

#============================================Dekad ============================================#

def dekadRASPI():
    average_pattern_dekad = vp.get('CHIRPS_Longterm_Average','global_lta_dekad_pattern')
    std_pattern_dekad = vp.get('CHIRPS_Longterm_Standard_Deviation','global_ltsd_dekad_pattern')
    dekad_pattern = vp.get('CHIRPS', 'global_dekad_pattern')
    AVGdir_dekad = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Dekad\\NewStatistics\\avg'
    STDdir_dekad = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Dekad\\NewStatistics\\std'
    dekaddir = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Dekad\\TifData'
    ResultDir_dekad = 'D:\\IDN_GIS\\01_Data\\01_Global\\VampireData\\global_rainfall_anomaly_dekad'
    ResultDirSPI_dekad = 'D:\\IDN_GIS\\01_Data\\01_Global\\VampireData\\global_spi_dekad'
    AVGregex_dekad = re.compile(average_pattern_dekad)
    STDregex_dekad = re.compile(std_pattern_dekad)
    Moregex_dekad = re.compile(dekad_pattern)

    for Dfilename in os.listdir(dekaddir):
        if Dfilename.endswith(".tif") or Dfilename.endswith(".tiff"):
            #print(Dfilename)
            Moresult_dekad = Moregex_dekad.match(Dfilename)
            Dmonth = Moresult_dekad.group('month')
            Ddekad = Moresult_dekad.group('dekad')
            for ADfilename in os.listdir(AVGdir_dekad):
                if ADfilename.endswith(".tif"):
                    if AVGregex_dekad.match(ADfilename):
                        AVGresult_dekad = AVGregex_dekad.match(ADfilename)
                        SDmonth = AVGresult_dekad.group('month')
                        SDdekad = AVGresult_dekad.group('dekad')
                        if SDmonth == Dmonth and SDdekad == Ddekad:
                            #print(Dfilename+" match with "+ADfilename)
                            AVGFile_dekad = os.path.join(AVGdir_dekad, ADfilename)
                            MoFile_dekad = os.path.join(dekaddir, Dfilename)
                            month = SDmonth
                            year = Moresult_dekad.group('year')
                            ext = ".tif"
                            newfilename_dekad = '{0}.{1}.{2}.{3}.ratio_anom{4}'.format(base_product_name, year, month, Ddekad, ext)
                            #print(newfilename_dekad)
                            if arcpy.Exists(os.path.join(ResultDir_dekad, newfilename_dekad)):
                                 logging.debug(datelog+": file " + newfilename_dekad + " is already exist")
                            else:
                                newRaster_dekad = Int(100 * Raster(MoFile_dekad) / Raster(AVGFile_dekad))
                                newRaster_dekad.save(os.path.join(ResultDir_dekad, newfilename_dekad))
                                logging.debug(datelog+": file " + newfilename_dekad + " is created")

                            for SDfilename in os.listdir(STDdir_dekad):
                                if SDfilename.endswith(".tif"):
                                    if STDregex_dekad.match(SDfilename):
                                        STDresult_dekad = STDregex_dekad.match(SDfilename)
                                        SSmonth = STDresult_dekad.group('month')
                                        SSDdekad = STDresult_dekad.group('dekad')
                                        if SDmonth == SSmonth and SDdekad == SSDdekad:
                                            #print(Dfilename + " match with " + ADfilename +" match with " +SDfilename)
                                            SPIFile_dekad = os.path.join(STDdir_dekad, SDfilename)
                                            year = Moresult_dekad.group('year')
                                            ext = ".tif"
                                            spifilename_dekad = '{0}.{1}.{2}.{3}.spi{4}'.format(base_product_name, year, month, SSDdekad, ext)
                                            SPIRaster_dekad = (Raster(MoFile_dekad) - Raster(AVGFile_dekad))/Raster(SPIFile_dekad)
                                            if arcpy.Exists(os.path.join(ResultDirSPI_dekad, spifilename_dekad)):
                                                logging.debug(datelog+": file " + spifilename_dekad + " is already exist")
                                            else:
                                                SPIRaster_dekad.save(os.path.join(ResultDirSPI_dekad, spifilename_dekad))
                                                logging.debug(datelog+": file " + spifilename_dekad + " is created")
                                        continue
                                else:
                                    continue

                        continue
                else:
                    continue
            continue
        else:
            continue

# #==========================================Seasonal============================================#
def seasonalRASPI():
    average_pattern_seasonal = vp.get('CHIRPS_Longterm_Average','global_lta_seasonal_pattern')
    std_pattern_seasonal = vp.get('CHIRPS_Longterm_Standard_Deviation','global_ltsd_seasonal_pattern')
    seasonal_pattern = vp.get('CHIRPS', 'global_seasonal_pattern')
    AVGdir_seasonal = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Seasonal\\NewStatististics\\avg'
    STDdir_seasonal = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Seasonal\\NewStatististics\\std'
    seasonaldir = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Seasonal\\TifData'
    ResultDir_seasonal = 'D:\\IDN_GIS\\01_Data\\01_Global\\VampireData\\global_rainfall_anomaly_3_month'
    ResultDirSPI_seasonal = 'D:\\IDN_GIS\\01_Data\\01_Global\\VampireData\\global_spi_3_month'
    AVGregex_seasonal = re.compile(average_pattern_seasonal)
    STDregex_seasonal = re.compile(std_pattern_seasonal)
    Moregex_seasonal = re.compile(seasonal_pattern)

    for SEfilename in os.listdir(seasonaldir):
        if SEfilename.endswith(".tif") or SEfilename.endswith(".tiff"):
            Moresult_seasonal = Moregex_seasonal.match(SEfilename)
            SEmonth = Moresult_seasonal.group('season')
            for SESfilename in os.listdir(AVGdir_seasonal):
                if SESfilename.endswith(".tif") or SESfilename.endswith(".tiff"):
                    if AVGregex_seasonal.match(SESfilename):
                        AVGresult_seasonal = AVGregex_seasonal.match(SESfilename)
                        SESmonth = AVGresult_seasonal.group('season')
                        if SEmonth == SESmonth:
                            #print(SEfilename+" match with "+SESfilename)
                            AVGFile_seasonal = os.path.join(AVGdir_seasonal, SESfilename)
                            MoFile_seasonal = os.path.join(seasonaldir, SEfilename)
                            SEyear = Moresult_seasonal.group('year')
                            ext = ".tif"
                            newfilename_seasonal = '{0}.{1}.{2}.ratio_anom{3}'.format(base_product_name, SEyear, SEmonth, ext)
                            if arcpy.Exists(os.path.join(ResultDir_seasonal, newfilename_seasonal)):
                                 logging.debug(datelog+": file " + newfilename_seasonal + " is already exist")
                            else:
                                newRaster_seasonal = Int(100 * Raster(MoFile_seasonal) / Raster(AVGFile_seasonal))
                                newRaster_seasonal.save(os.path.join(ResultDir_seasonal, newfilename_seasonal))
                                logging.debug(datelog+": file " + newfilename_seasonal + " is created")

                            for STDSEfilename in os.listdir(STDdir_seasonal):
                                if STDSEfilename.endswith(".tif"):
                                    if STDregex_seasonal.match(STDSEfilename):
                                        STDresult_seasonal = STDregex_seasonal.match(STDSEfilename)
                                        STDSEmonth = STDresult_seasonal.group('season')
                                        if STDSEmonth == SEmonth:
                                            #print(SEfilename + " match with " + SESfilename +" match with " +STDSEfilename)
                                            SPIFile_seasonal = os.path.join(STDdir_seasonal, STDSEfilename)
                                            ext = ".tif"
                                            spifilename_seasonal = '{0}.{1}.{2}.spi{3}'.format(base_product_name, SEyear, SEmonth, ext)
                                            if arcpy.Exists(os.path.join(ResultDirSPI_seasonal, spifilename_seasonal)):
                                                logging.debug(datelog+": file " + spifilename_seasonal + " is already exist")
                                            else:
                                                SPIRaster_seasonal = (Raster(MoFile_seasonal) - Raster(
                                                    AVGFile_seasonal)) / Raster(SPIFile_seasonal)
                                                SPIRaster_seasonal.save(os.path.join(ResultDirSPI_seasonal, spifilename_seasonal))
                                                logging.debug(datelog+": file " + spifilename_seasonal + " is created")
                                        continue
                                else:
                                    continue

                        continue
                else:
                    continue
            continue
        else:
            continue

