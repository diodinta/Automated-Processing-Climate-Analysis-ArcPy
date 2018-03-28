import os
import arcpy
from arcpy.sa import *

def ra_six_monthly(dyear, monthseq, tif_folder, stat_folder, result_folder):
    for stat_file in os.listdir(stat_folder):
        if stat_file.endswith(".tif"):
            parse_string = stat_file.split('.')
            stat_month = parse_string[3]
            stat_type = parse_string[6]
            if stat_month == monthseq and stat_type == 'avg':
                stat_file_process = os.path.join(stat_folder, stat_file)
            if stat_month == monthseq and stat_type == 'std':
                std_file_process = os.path.join(stat_folder, stat_file)
    print("avg file found : " +stat_file_process)
    print("std file found : " +std_file_process)
    for tif_file in os.listdir(tif_folder):
        if tif_file.endswith(".tif"):
            parse_string_tif = tif_file.split('.')
            tif_month = parse_string_tif[3]
            tif_year = parse_string_tif[2]
            if tif_month == monthseq and tif_year == dyear:
                tif_file_process = os.path.join(tif_folder, tif_file)
                print("tif file found : "+tif_file_process)
    arcpy.CheckOutExtension("spatial")
    ra_filename = 'chirps-v2.0.{0}.{1}.ratio_anom.tif'.format(dyear, monthseq)
    if not os.path.exists(os.path.join(result_folder, ra_filename)):
        print("Processing Rainfall anomaly : "+ra_filename)
        ra_calc = Int(100 * Raster(tif_file_process) / Raster(stat_file_process))
        ra_calc.save(os.path.join(result_folder, ra_filename))
        print("Processing Rainfall anomaly : "+ra_filename+ " finished")
    spi_filename = 'chirps-v2.0.{0}.{1}.spi.tif'.format(dyear, monthseq)
    if not os.path.exists(os.path.join(spi_result_folder, spi_filename)):
        print("Processing SPI : "+spi_filename)
        spi_calc = (Raster(tif_file_process) - Raster(stat_file_process)) / Raster(std_file_process)
        spi_calc.save(os.path.join(spi_result_folder, spi_filename))
        print("Processing SPI : "+spi_filename+ " finished")
    arcpy.CheckInExtension("spatial")

six_month_data = ['010203040506', '020304050607', '030405060708', '040506070809', '050607080910', '060708091011',
                  '070809101112', '080910111201', '091011120102', '101112010203', '111201020304', '120102030405']
stat_folder = "D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\6-monthly\\statistics"
tif_folder = "D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\6-monthly\\tifdata"
result_folder = "D:\\IDN_GIS\\01_Data\\01_Global\\VampireData\\global_rainfall_anomaly_6_month"
spi_result_folder = "D:\\IDN_GIS\\01_Data\\01_Global\\VampireData\\global_spi_6_month"

year_calc = 2016
while year_calc > 1980:
    for i in six_month_data:
        print("processing data "+str(year_calc)+" and "+i)
        ra_six_monthly(str(year_calc), i, tif_folder, stat_folder, result_folder)
    year_calc = year_calc + 1