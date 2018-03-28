import datetime
import dslr
from datetime import date

raindayfolder = "D:\\IDN_GIS\\01_Data\\01_Global\\Rasters\\Climate\\Precipitation\\IMERG\\daily\\rainday_1"
dslrfolder = "D:\\IDN_GIS\\01_Data\\01_Global\\VampireData\\global_dslr_1mm"
datestart = date(2017,10,24)
dateend = date(2017,10,10)
while dateend <= datestart:
    dslrdate = dateend.strftime('%Y%m%d')
    print(dslrdate)
    dslr.calculatedslr(dslrdate, 1, 90, raindayfolder, dslrfolder)
    dateend = dateend + datetime.timedelta(days=1)