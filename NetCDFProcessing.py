import arcpy
import os

def createRaster(folder, netcdffile, tiffolder):
    arcpy.env.workspace = tiffolder
    filename = os.path.join(folder, netcdffile)
    newfilename = netcdffile+".tif"
    tiffile = os.path.join(tiffolder, newfilename)
    if not os.path.exists(os.path.join(tiffolder, newfilename)):
        arcpy.MakeNetCDFRasterLayer_md(in_netCDF_file=filename,variable="precipitationCal",x_dimension="lon",y_dimension="lat",out_raster_layer=newfilename,band_dimension="",dimension_values="",value_selection_method="BY_VALUE")
        arcpy.CopyRaster_management(newfilename, tiffile, "", "", "", "NONE", "NONE", "")
        if not os.path.exists(tiffile):
            print("Failed to create " + newfilename)
        if os.path.exists(tiffile):
            print(newfilename + " is successfully created")
    else:
        print(newfilename + " already exists")



# folder = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\IMERG\\daily\\NC4'
# tiffolder = 'D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\IMERG\\daily\\tif'
# for i in os.listdir(folder):
#     if i.endswith(".nc4"):
#         print(i)
#         createRaster(folder, i, tiffolder)