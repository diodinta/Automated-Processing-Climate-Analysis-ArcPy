import time
import optparse
import os
import traceback
import sys
import arcpy
import datetime
from datetime import date
from arcpy.sa import *

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

def rainydays(tiffolder, threshold, rainydayFolder):
    print("start processing rainy data........ ")
    sr = arcpy.SpatialReference(4326)
    tifdata = []
    rainydata = []
    for tdata in os.listdir(tiffolder):
        if tdata.endswith(".tif") or tdata.endswith(".tiff"):
            parseString = tdata.split('.')
            parse = parseString[4]
            tifdate = parse[0:8]
            tifdata.append(tifdate)
    for rdata in os.listdir(rainydayFolder):
        if rdata.endswith(".tif") or rdata.endswith(".tiff"):
            parseStringtdata = rdata.split('.')
            rainydate = parseStringtdata[1]
            rainydata.append(rainydate)
    for i in tifdata:
        print("checking rainday data for date " +i)
        if i not in rainydata:
            print("rainday data for date " +i+ " has not been calculated")
            print("calculating rainday for date " +i)
            tifname = 'idn_DAY-L.MS.MRG.3IMERG.{0}-S000000-E235959.tif'.format(i)
            rainyfilename = 'raindays.{0}.threshold_{1}mm.tif'.format(i,threshold)
            tiffile = os.path.join(tiffolder, tifname)
            arcpy.CheckOutExtension("spatial")
            outCon = Con(Raster(tiffile) > int(threshold),1,0)
            outCon.save(os.path.join(rainydayFolder, rainyfilename))
            arcpy.DefineProjection_management(os.path.join(rainydayFolder, rainyfilename),sr)
            print("file "+rainyfilename+" is created")
            arcpy.CheckInExtension("spatial")
    print("processing rainy days for threshold "+str(threshold)+" is  completed--------")

def calculatedslr(dslrdate, threshold, num_of_days, raindayfolder, dslrfolder):
    dslrfilename = 'dslr_{0:0=2d}mm_threshold_{1}.tif'.format(threshold, dslrdate)
    #print("start processing DSLR--------------- ")
    if not os.path.exists(os.path.join(dslrfolder,dslrfilename)):
        arcpy.CheckOutExtension("spatial")
        print("DSLR file for date " +dslrdate+ " has not been calculated")
        print("calculating DSLR file for date "+dslrdate)
        dslrdateformatted = date(int(dslrdate[0:4]), int(dslrdate[4:6]), int(dslrdate[6:8]))
        NumDaysRain = int(num_of_days)+1
        index = []
        rangedata = 0
        for rainyfilename in os.listdir(raindayfolder):
            if rainyfilename.endswith(".tif") or rainyfilename.endswith(".tiff"):
                arcpy.CalculateStatistics_management(os.path.join(raindayfolder,rainyfilename))
                get_min_value = arcpy.GetRasterProperties_management(os.path.join(raindayfolder,rainyfilename), "MINIMUM")
                get_max_value = arcpy.GetRasterProperties_management(os.path.join(raindayfolder,rainyfilename), "MAXIMUM")
                max_value = int(get_max_value.getOutput(0))
                min_value = int(get_min_value.getOutput(0))
                if min_value == 0 and max_value == 1:
                    parseStringRain = rainyfilename.split('.')
                    parseRain = parseStringRain[1]
                    yearRain = int(parseRain[0:4])
                    monthRain = int(parseRain[4:6])
                    dayRain = int(parseRain[6:8])
                    filedateRain = date(yearRain, monthRain, dayRain)
                    if filedateRain < dslrdateformatted:
                        rangedata = rangedata+1; # to check if the data is in range
                        if filedateRain > dslrdateformatted - datetime.timedelta(days=num_of_days+1): #to limit the data calculation
                            index.append(os.path.join(raindayfolder, rainyfilename))
                else:
                    print(rainyfilename + " is not a proper rainyday data. max value must be 1 and min value must be 0.")

        if len(index)>=num_of_days:
            print("rainday data "+str(len(index))+" before DSLR date are complete. calculating DSLR....")
            indexReverse = sorted(index, reverse=True)
            #print(indexReverse)
            outHighestPosition = HighestPosition(indexReverse)
            #outHighestPosition.save(os.path.join(dslrfolder, 'temp.tif'))
            minusOne = outHighestPosition - 1
            minusOne.save(os.path.join(dslrfolder, dslrfilename))
            print("file DaysSinceLastRain.tif is created. Process completed")
        else:
            print("the sum of the data " +str(len(index))+ " is less than the num of days = "+str(num_of_days))
        arcpy.CheckInExtension("spatial")
    else:
        print("DSLR file for date " +dslrdate+ " exists")

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], version='$Id$')
        parser.add_option ('-f', '--folder', dest='nc4_folder', action='store', help='NC4 folder')
        parser.add_option ('-o', '--output_folder', dest='output_folder', action='store', help='generate config')
        parser.add_option('-s', '--start_date', dest='start_date', action='store', help='Start Date in YYYYMMDD format')
        parser.add_option('-e', '--end_date', dest='end_date', action='store', help='End Date in YYYYMMDD format')
        parser.add_option('-t', '--threshold', dest='threshold', action='store', help='threshold in mm')
        parser.add_option('-n', '--num_of_days', dest='num_of_days', action='store', help='number of days to calculate DSLR')
        (options, args) = parser.parse_args()
        # ------- default parameter -------- #
        start_date = ''
        end_date = ''
        threshold = 1
        num_of_days = 90
        #------- end of default parameter -------#

        if options.nc4_folder:
            nc4_folder = options.nc4_folder
        if options.output_folder:
            output_folder = options.output_folder
        if options.start_date:
            start_date = options.start_date
        if options.end_date:
            end_date = options.end_date
        if options.threshold:
            threshold = options.threshold
        if options.num_of_days:
            num_of_days = options.num_of_days
        print("-------------------- Days Since Last Rain Calculation---------------------")
        print("----------------- Developed by DD Dafrista - WFP Indonesia----------------")
        print("")
        print 'Input folder=', nc4_folder
        print 'Output folder=', output_folder
        print 'Start Date=', start_date
        print 'End Date=', end_date
        print 'threshold=', threshold
        print 'Num of days=', num_of_days

        if start_date == '' or end_date == '':
            print("Start date or end date is empty. calculating all possible dslr from input folder...")
            print("checking input folder .... ")
            if not os.path.exists(nc4_folder) or not os.path.exists(output_folder):
                print("input folder or output folder is in wrong format or does not exist")
                sys.exit(0)
            else:
                print("input folder and output folder are found. Looking for NetCDF file in input folder")
                IndexData = []
                IndexDate = []
                for nc4_file in os.listdir(nc4_folder):
                    if nc4_file.endswith(".nc4"):
                        parseStringRain = nc4_file.split('.')
                        parseRain = parseStringRain[4]
                        yearRain = int(parseRain[0:4])
                        monthRain = int(parseRain[4:6])
                        dayRain = int(parseRain[6:8])
                        filedateRain = date(yearRain, monthRain, dayRain)
                        IndexDate.append(filedateRain)
                        IndexData.append(nc4_file)
                indexDateSorted = sorted(IndexDate, reverse=True)
                indexDataSorted = sorted(IndexData, reverse=True)
                data_numdays = indexDateSorted[0] - indexDateSorted[len(indexDateSorted)-1]
                date_numdays = len(indexDateSorted)
                if data_numdays.days+1 == date_numdays and date_numdays > 90:
                    print("data is in order from " +str(indexDateSorted[0])+ " to "+ str(indexDateSorted[len(indexDateSorted)-1]))
                    print("start processing...........................")
                    print("creating folder to store raster precipitation data...")
                    parent_dir = os.path.abspath(os.path.join(nc4_folder, os.pardir))
                    result_folder = parent_dir+ "\\result"
                    if not os.path.exists(result_folder):
                        os.mkdir(result_folder)
                    tiffolder = parent_dir+ "\\result\\imerg_precipitation"
                    if not os.path.exists(tiffolder):
                        os.mkdir(tiffolder)
                    for i in indexDataSorted:
                        createRaster(nc4_folder, i, tiffolder)
                    print("creating raster precipitation data are done")
                print("creating folder to store indonesia precipitation data...")
                idn_precipitation = result_folder + "\\idn_precipitation"
                subset_file = parent_dir + "\\indonesia_GPM\\idn_bnd_subset_imerg_01_deg_grid_diss_a.shp"
                if not os.path.exists(idn_precipitation):
                    os.mkdir(idn_precipitation)
                print("start processing the subset data")
                for tif_file in os.listdir(tiffolder):
                    if tif_file.endswith(".tif"):
                        dateparse = tif_file.split('.')
                        datefile = dateparse[4]
                        new_name = 'idn_day-L.MS.MRG.3IMERG.{0}.tif'.format(datefile)
                        arcpy.CheckOutExtension("spatial")
                        if not os.path.exists(os.path.join(idn_precipitation, new_name)):
                            extractbymask = ExtractByMask(os.path.join(tiffolder, tif_file), subset_file)
                            extractbymask.save(os.path.join(idn_precipitation, new_name))
                            print(new_name+ " is successfully created")
                        else:
                            print(new_name + " exists")
                idn_rainyday = result_folder + "\\idn_rainyday"
                if not os.path.exists(idn_rainyday):
                    os.mkdir(idn_rainyday)
                rainydays(idn_precipitation, threshold, idn_rainyday)
                print("----------------------------------------------------------------")
                print("----------start calculating DSLR from rainy data----------------")
                print("----------------------------------------------------------------")
                start_checking = indexDateSorted[len(indexDateSorted)-(num_of_days-1)]
                date_end = indexDateSorted[0]
                idn_dslr = result_folder + "\\idn_dslr"
                if not os.path.exists(idn_dslr):
                    os.mkdir(idn_dslr)
                while date_end >= start_checking:
                    dslrfilename = 'dslr_{0:0=2d}mm_threshold_{1}.tif'.format(threshold, start_checking.strftime('%Y%m%d'))
                    #print("start processing DSLR--------------- ")
                    if not os.path.exists(os.path.join(idn_dslr, dslrfilename)):
                        print("processing " + str(start_checking))
                        dslrdate = start_checking.strftime('%Y%m%d')
                        calculatedslr(dslrdate, threshold, num_of_days, idn_rainyday, idn_dslr)
                    else:
                        print(str(start_checking) + " is available")
                    start_checking = start_checking + datetime.timedelta(days=1)
                arcpy.CheckOutExtension("spatial")
        else:
            print("wait")

        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)