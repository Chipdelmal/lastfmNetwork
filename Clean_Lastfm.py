##############################################################################
# Last.fm: Clean
#   
##############################################################################
from os import path
from sys import argv
import pandas as pd
import BANS as ban
import auxiliary as aux
import CONSTANTS as cst

if aux.isnotebook():
    (USERNAME, PTH_DTA) = ('chipmaligno', './dta')
else:
    (USERNAME, PTH_DTA) = argv[1:]
##############################################################################
# Read and shape CSV
##############################################################################
dataRaw = pd.read_csv(
    path.join(PTH_DTA, USERNAME+'.csv'),
    header=None, names=['Artist', 'Album', 'Song', 'Date'],
    parse_dates=[3]
)
# Remove duplicate entries ---------------------------------------------------
dataRaw = dataRaw.drop_duplicates()
##############################################################################
# Process artists: remove artists present in the BAN list and fix names
##############################################################################
data = aux.removeBanned(dataRaw, bans=ban.BAN)
data = aux.replace(data, ban.SWP_PRE, ('Artist', 'Artist'))
##############################################################################
# Fix time information
##############################################################################
timeInfo = pd.to_datetime(data["Date"], unit='ms')
fixedTime = timeInfo.dt.tz_localize('UTC').dt.tz_convert(cst.TIMEZONE)
data = data.assign(Date=fixedTime)
##############################################################################
# Export dataframe
##############################################################################
data.to_csv(path.join(PTH_DTA, USERNAME+'_cln.csv'), index=False)