##############################################################################
# Last.fm: Clean
#   Takes the raw last.fm data from the csv, removes duplicates, removes
#   banned artists, and converts into a timezone
##############################################################################
from os import path
from sys import argv
import pandas as pd
import operator
from functools import reduce
from collections import Counter, OrderedDict
import BANS as ban
import auxiliary as aux
import CONSTANTS as cst

if aux.isnotebook():
    (USERNAME, PTH_DTA) = ('chipmaligno', './data')
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
# data = dataRaw.drop_duplicates()
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
# Split by date
##############################################################################
data['Datetime'] = pd.to_datetime(data['Date'], errors='coerce', utc=True)
data['Day'] = data['Datetime'].dt.tz_localize(None).dt.to_period('D')
# Post-change ----------------------------------------------------------------
mask = (data['Day'] > '2000-01-01') & (data['Day'] <= '2050-12-31')
dfPst = data[mask]
# Pre-change -----------------------------------------------------------------
mask = (data['Day'] > '1900-01-01') & (data['Day'] < '2000-01-01')
dfPre = data[mask]
###############################################################################
# Check for Inflated Counts
###############################################################################
# Add Interval Column ---------------------------------------------------------
dteCpy = dfPst['Date'].copy()
dfPst['Interval'] = pd.to_datetime(dteCpy, errors='coerce', utc=True)
dfPst['Interval'] = dfPst['Interval'].dt.tz_localize(None).dt.to_period('D')
# Detect inflated dates -------------------------------------------------------
arts = sorted(list(dfPst['Artist'].unique()))
artsNum = len(arts)
banDict = OrderedDict()
for artist in arts:
    probe = dfPst[dfPst['Artist'] == artist].copy()
    probe['Date'] = pd.to_datetime(probe['Date'], errors='coerce', utc=True)
    probe['Interval'] = probe['Date'].dt.tz_localize(None).dt.to_period('D')
    counts = probe.groupby('Interval').size().sort_values(ascending=False)
    dayObjs = list(counts[counts > cst.DAILY_PLAYCOUNT_LIMIT].index)
    if len(dayObjs) > 0:
        banDict[artist] = dayObjs
# Remove Inflated Dates -------------------------------------------------------
(art, dates) = list(banDict.items())[0]
for (art, dates) in list(banDict.items()):
    fltr = (
        dfPst['Artist']==art,
        dfPst['Interval'].isin(set(dates))
    )
    fullFilter = list(map(all, zip(*fltr)))
    dfPst.drop(dfPst[fullFilter].index, inplace=True)
##############################################################################
# Total frequencies
##############################################################################
frequencies = dict(
    reduce(operator.add, map(Counter, [dfPre[['Artist']], dfPst['Artist']]))
)
{k: v for k, v in sorted(frequencies.items(), key=lambda item: item[1])[::-1]}
# data.set_index('Day')
# data.loc[date(year=2014,month=1,day=1):date(year=2014,month=2,day=1)]