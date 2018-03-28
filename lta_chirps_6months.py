import os
import arcpy

six_month_data = ['010203040506', '020304050607', '030405060708', '040506070809', '050607080910', '060708091011',
                  '070809101112', '080910111201', '091011120102', '101112010203', '111201020304', '120102030405']

data_folder = "D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\6-monthly\\tifdata\\forlta"
lta_folder = "D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\CHIRPS\\6-monthly\\statistics"

dictionary = {}
for i in six_month_data:
    content = []
    for file_sixmonth in os.listdir(data_folder):
        if file_sixmonth.endswith(".tif") or file_sixmonth.endswith(".tiff"):
            parse_string = file_sixmonth.split('.')
            Dmonthseq = parse_string[3]
            if Dmonthseq == i:
                content.append(os.path.join(data_folder, file_sixmonth))
    dictionary[i] = content


for index in dictionary:
    listoffile = dictionary[index]
    print(listoffile)
    ext = ".tif"
    newfilename_sixmonth_std = 'chirps-v2.0.1981-2015.{0}.monthly.35yrs.std{1}'.format(index, ext)
    newfilename_sixmonth_avg = 'chirps-v2.0.1981-2015.{0}.monthly.35yrs.avg{1}'.format(index, ext)

    if arcpy.Exists(os.path.join(lta_folder, newfilename_sixmonth_std)):
        print(newfilename_sixmonth_std + " exists")
    else:
        arcpy.CheckOutExtension("spatial")
        outCellStatistics = arcpy.sa.CellStatistics(listoffile, "STD", "DATA")
        outCellStatistics.save(os.path.join(lta_folder, newfilename_sixmonth_std))
        arcpy.CheckInExtension("spatial")

    if arcpy.Exists(os.path.join(lta_folder, newfilename_sixmonth_avg)):
        print(newfilename_sixmonth_avg + " exists")
    else:
        arcpy.CheckOutExtension("spatial")
        outCellStatistics_avg = arcpy.sa.CellStatistics(listoffile, "MEAN", "DATA")
        outCellStatistics_avg.save(os.path.join(lta_folder, newfilename_sixmonth_avg))
        arcpy.CheckInExtension("spatial")