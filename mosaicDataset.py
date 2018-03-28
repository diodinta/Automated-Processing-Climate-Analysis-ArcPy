import arcpy
import logging
import os
import sys
import time
import VampireDefaults
import ast
import re
import xml.dom.minidom as DOM
from datetime import date

vp = VampireDefaults.VampireDefaults()

def addRastertoMDS(MDS, folder):
    arcpy.AddRastersToMosaicDataset_management(MDS, "Raster Dataset",folder,
                                               "UPDATE_CELL_SIZES", "UPDATE_BOUNDARY", "NO_OVERVIEWS", "", "0", "1500",
                                               "", "", "SUBFOLDERS", "OVERWRITE_DUPLICATES", "NO_PYRAMIDS", "NO_STATISTICS",
                                               "NO_THUMBNAILS", "", "NO_FORCE_SPATIAL_REFERENCE")
def update_mosaic_statistics (mosaic_dataset):
    logging.debug('updating mosaic statistics')
    arcpy.SetMosaicDatasetProperties_management(
        mosaic_dataset,use_time="ENABLED", start_time_field="start_date", end_time_field="end_date",)
    arcpy.management.CalculateStatistics(mosaic_dataset)
    arcpy.management.BuildPyramidsandStatistics(mosaic_dataset, 'INCLUDE_SUBDIRECTORIES', 'BUILD_PYRAMIDS', 'CALCULATE_STATISTICS')
    arcpy.RefreshCatalog(mosaic_dataset)

def eomday(year, month):
    days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    d = days_per_month[month - 1]
    if month == 2 and (year % 4 == 0 and year % 100 != 0 or year % 400 == 0):
        d = 29
    return d

def getYearMonth(name, product):
    if product == 'rainfall_anomaly_1_month':
        print("analomay")
        productPattern = vp.get('CHIRPS_Rainfall_Anomaly', 'ra_regional_monthly_pattern')
        print("product pattern : "+productPattern)
        regex = re.compile(productPattern)
        result = regex.match(name)
        f_year = result.group('year')
        f_month = result.group('month')
        lastday = eomday(int(f_year), int(f_month))
        dateStart = date(int(f_year),int(f_month),1)
        dateEnd = date(int(f_year),int(f_month),int(lastday))
        return(dateStart, dateEnd)
    elif product == 'spi_1_month':
        print("spi 1 month")
        productPattern = vp.get('CHIRPS_SPI', 'spi_regional_monthly_pattern')
        print("product pattern : "+productPattern)
        regex = re.compile(productPattern)
        result = regex.match(name)
        f_year = result.group('year')
        f_month = result.group('month')
        lastday = eomday(int(f_year), int(f_month))
        dateStart = date(int(f_year),int(f_month),1)
        dateEnd = date(int(f_year),int(f_month),int(lastday))
        return(dateStart, dateEnd)
    elif product == 'rainfall_anomaly_3_month':
        print("3 monthly rainfall anomaly")
        productPattern = vp.get('CHIRPS_Rainfall_Anomaly', 'ra_regional_seasonal_pattern')
        print("product pattern : "+productPattern)
        regex = re.compile(productPattern)
        result = regex.match(name)
        print(result)
        f_year = result.group('year')
        print(f_year)
        f_season = result.group('season')
        print(f_season, f_season[0:2])
        if int(f_season[4:6]) < int(f_season[0:2]):
            print(int(f_season[4:6]), " lebih kecil dari ", int(f_season[0:2]))
            f_year_end = int(f_year)+1
        else:
            print(int(f_season[4:6]), " lebih besar dari ", int(f_season[0:2]))
            f_year_end = int(f_year)
        lastday = eomday(int(f_year_end), int(f_season[4:6]))
        dateStart = date(int(f_year),int(f_season[0:2]),1)
        dateEnd = date(int(f_year_end),int(f_season[4:6]),int(lastday))
        print("resturn ", dateStart, dateEnd)
        return(dateStart, dateEnd)
    elif product == 'spi_3_month':
        print("3 monthly spi")
        productPattern = vp.get('CHIRPS_SPI', 'spi_regional_seasonal_pattern')
        print("product pattern : "+productPattern)
        regex = re.compile(productPattern)
        result = regex.match(name)
        print(result)
        f_year = result.group('year')
        print(f_year)
        f_season = result.group('season')
        print(f_season, f_season[0:2])
        if int(f_season[4:6]) < int(f_season[0:2]):
            print(int(f_season[4:6]), " lebih kecil dari ", int(f_season[0:2]))
            f_year_end = int(f_year)+1
        else:
            print(int(f_season[4:6]), " lebih besar dari ", int(f_season[0:2]))
            f_year_end = int(f_year)
        lastday = eomday(int(f_year_end), int(f_season[4:6]))
        dateStart = date(int(f_year),int(f_season[0:2]),1)
        dateEnd = date(int(f_year_end),int(f_season[4:6]),int(lastday))
        print("resturn ", dateStart, dateEnd)
        return(dateStart, dateEnd)
    elif product == 'rainfall_anomaly_dekad':
        print("Dekad rainfall anomaly")
        productPattern = vp.get('CHIRPS_Rainfall_Anomaly', 'ra_regional_dekad_pattern')
        regex = re.compile(productPattern)
        result = regex.match(name)
        f_year = result.group('year')
        f_month = result.group('month')
        f_dekad = result.group('dekad')
        if f_dekad == '1':
            dateStart = date(int(f_year),int(f_month),1)
            dateEnd = date(int(f_year),int(f_month),10)
        elif f_dekad == '2':
            dateStart = date(int(f_year),int(f_month),11)
            dateEnd = date(int(f_year),int(f_month),20)
        elif f_dekad == '3':
            lastday = eomday(int(f_year), int(f_month))
            dateStart = date(int(f_year),int(f_month),21)
            dateEnd = date(int(f_year),int(f_month),lastday)
        return(dateStart, dateEnd)
    elif product == 'spi_dekad':
        print("Dekad SPI")
        productPattern = vp.get('CHIRPS_SPI', 'spi_regional_dekad_pattern')
        regex = re.compile(productPattern)
        result = regex.match(name)
        f_year = result.group('year')
        f_month = result.group('month')
        f_dekad = result.group('dekad')
        if f_dekad == '1':
            dateStart = date(int(f_year),int(f_month),1)
            dateEnd = date(int(f_year),int(f_month),10)
        elif f_dekad == '2':
            dateStart = date(int(f_year),int(f_month),11)
            dateEnd = date(int(f_year),int(f_month),20)
        elif f_dekad == '3':
            lastday = eomday(int(f_year), int(f_month))
            dateStart = date(int(f_year),int(f_month),21)
            dateEnd = date(int(f_year),int(f_month),lastday)
        return(dateStart, dateEnd)
    elif product == 'vhi_crop_1_month':
        print("vhi 1 month")
        productPattern = vp.get('MODIS_VHI', 'vhi_crop_pattern')
        print("product pattern : "+productPattern)
        regex = re.compile(productPattern)
        result = regex.match(name)
        f_year = result.group('year')
        f_month = result.group('month')
        lastday = eomday(int(f_year), int(f_month))
        dateStart = date(int(f_year),int(f_month),1)
        dateEnd = date(int(f_year),int(f_month),int(lastday))
        return(dateStart, dateEnd)
    elif product == 'idn_vhi_monthly2':
        print("vhi 1 month")
        productPattern = vp.get('MODIS_VHI', 'vhi_pattern')
        print("product pattern : "+productPattern)
        regex = re.compile(productPattern)
        result = regex.match(name)
        f_year = result.group('year')
        f_month = result.group('month')
        lastday = eomday(int(f_year), int(f_month))
        dateStart = date(int(f_year),int(f_month),1)
        dateEnd = date(int(f_year),int(f_month),int(lastday))
        return(dateStart, dateEnd)
    elif product == 'DSLR_01mm' or product == 'DSLR_05mm':
        #print("DSLR")
        productPattern = vp.get('DSLR', 'DSLR_output_pattern')
        #print("product pattern : "+productPattern)
        regex = re.compile(productPattern)
        result = regex.match(name)
        f_year = result.group('year')
        f_month = result.group('month')
        f_day = result.group('day')
        lastday = eomday(int(f_year), int(f_month))
        dateStart = date(int(f_year),int(f_month),int(f_day))
        dateEnd = date(int(f_year),int(f_month),int(f_day))
        return(dateStart, dateEnd)
    else:
        return(None, None)


def addDateField(mds):
    in_table = mds
    field_name = ["start_date", "end_date"]
    field_type = "DATE"
    for i in field_name:
        if arcpy.ListFields(mds, i):
            print "Field exists"
        else:
            arcpy.AddField_management(in_table, i, field_type)

def updateDateField(mds,productX):
    fields = ['Name', 'start_date', 'end_date']
    print("produknya : "+productX)
    with arcpy.da.UpdateCursor(mds, fields) as cursor:
        print(cursor)
        for row in cursor:
            if row[1] == None or row[2] == None:
                fileName = str(row[0])+".tif"
                print("filename: "+fileName)
                startD, endD = getYearMonth(fileName, productX)
                print("tes ", startD, endD)
                if startD == None:
                    print("cant find match naming template")
                else:
                    print(startD, endD)
                    print("tes")
                    row[1] = startD
                    row[2] = endD
            elif row[1] is not None:
                print("Start Date is not none")
                print(row[0])
            cursor.updateRow(row)
    del cursor