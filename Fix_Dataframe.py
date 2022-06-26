##############################################################################
# Fix Dataframes
#   Filters a dataframe between dates, checks for inflated counts, and 
#   amends artists names to match musicbrainz tags
##############################################################################
from os import path
from sys import argv
import pandas as pd
from jellyfish import levenshtein_distance
from collections import OrderedDict
import auxiliary as aux
import CONSTANTS as cst
import BANS as ban

if aux.isnotebook():
    (USERNAME, PTH_DTA) = ('chipmaligno', './data')
else:
    (USERNAME, PTH_DTA) = argv[1:]
###############################################################################
# Read Data
###############################################################################
pBase = path.join(PTH_DTA, USERNAME)
DTA_CLN = pd.read_csv(pBase+'_cln.csv', parse_dates=[3])
DTA_MBZ = pd.read_csv(pBase+'_mbz.csv')
# Add Interval Column ---------------------------------------------------------
dteCpy = DTA_CLN['Date'].copy()
DTA_CLN['Interval'] = pd.to_datetime(dteCpy, errors='coerce', utc=True)
DTA_CLN['Interval'] = DTA_CLN['Interval'].dt.tz_localize(None).dt.to_period('D')
###############################################################################
# Filter by Dates
###############################################################################
(dLo, dHi) = (cst.DF_DTE_RANGE[0], cst.DF_DTE_RANGE[1])
msk = [
    ((i.date() >= dLo) and (i.date() <= dHi)) 
    if (type(i) is not float) else (False) for i in DTA_CLN['Date']
]
DTA_CLN = DTA_CLN.loc[msk]
###############################################################################
# Check for Inflated Counts
###############################################################################
arts = sorted(list(DTA_CLN['Artist'].unique()))
artsNum = len(arts)
banDict = OrderedDict()
for artist in arts:
    probe = DTA_CLN[DTA_CLN['Artist'] == artist].copy()
    probe['Date'] = pd.to_datetime(probe['Date'], errors='coerce', utc=True)
    probe['Interval'] = probe['Date'].dt.tz_localize(None).dt.to_period('D')
    counts = probe.groupby('Interval').size().sort_values(ascending=False)
    dayObjs = list(counts[counts > cst.DAILY_PLAYCOUNT_LIMIT].index)
    if len(dayObjs) > 0:
        banDict[artist] = dayObjs
# Remove Inflated Dates -------------------------------------------------------
DTA_CLN.shape
(art, dates) = list(banDict.items())[0]
for (art, dates) in list(banDict.items()):
    fltr = (
        DTA_CLN['Artist']==art,
        DTA_CLN['Interval'].isin(set(dates))
    )
    fullFilter = list(map(all, zip(*fltr)))
    DTA_CLN.drop(DTA_CLN[fullFilter].index, inplace=True)
###############################################################################
# Match Musicbrainz artists into dataframe
###############################################################################
artsMB = sorted(list(DTA_MBZ['Artist'].unique()))
replacements = {}
for art in arts:
    dists = [levenshtein_distance(art.lower(), mbArt.lower()) for mbArt in artsMB]
    replacements[artsMB[dists.index(min(dists))]] = {art}
DTA_CLN = aux.replace(DTA_CLN, replacements, ('Artist', 'Artist'))
###############################################################################
# Export
###############################################################################
DTA_CLN.to_csv(path.join(PTH_DTA, USERNAME+'_fxd.csv'), index=False)