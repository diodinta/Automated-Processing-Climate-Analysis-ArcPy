import os
import arcpy
from arcpy import env

tif_folder = "D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\Monthly\\TifData"
arcpy.env.workspace = tif_folder
output_folder = "D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\6-monthly\\tifdata"
month_calculate = 6
for file_monthly in os.listdir(tif_folder):
    if file_monthly.endswith(".tif"):
        ext = ".tif"
        parse_string = file_monthly.split('.')
        Dmonth = int(parse_string[3])
        DYear = int(parse_string[2])
        array_process = []
        array_process.append(file_monthly)
        i = 1
        DmonthSeq = parse_string[3]
        while i < month_calculate:
            next_month = Dmonth+i
            if next_month > Dmonth and next_month <= 12:
                file_process = 'chirps-v2.0.{0}.{1}{2}'.format(str(DYear), str(next_month).zfill(2), ext)
            else:
                next_month = next_month - 12
                file_process = 'chirps-v2.0.{0}.{1}{2}'.format(str(DYear+1), str(next_month).zfill(2), ext)
            i = i + 1
            DmonthSeq = DmonthSeq + str(next_month).zfill(2)
            array_process.append(file_process)
    print(array_process)
    filename_6month = 'chirps-v2.0.{0}.{1}.tif'.format(DYear, DmonthSeq)
    if not os.path.exists(os.path.join(output_folder, filename_6month)):
        print("processing "+filename_6month+" ....")
        raster_0 = array_process[0]
        raster_1 = array_process[1]
        raster_2 = array_process[2]
        raster_3 = array_process[3]
        raster_4 = array_process[4]
        raster_5 = array_process[5]
        arcpy.CheckOutExtension("spatial")
        outCellStatistics = arcpy.sa.Raster(raster_0)+arcpy.sa.Raster(raster_1)+arcpy.sa.Raster(raster_2)+\
                            arcpy.sa.Raster(raster_3)+arcpy.sa.Raster(raster_4)+arcpy.sa.Raster(raster_5)
        outCellStatistics.save(os.path.join(output_folder, filename_6month))
        arcpy.CheckInExtension("spatial")
        print(filename_6month)
    else:
        print(filename_6month+ " exist")








