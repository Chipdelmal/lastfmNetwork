##############################################################################
# Last.fm: Clean
#   Takes the raw last.fm data from the csv, removes duplicates, removes
#   banned artists, and converts into a timezone
##############################################################################
from os import path
from sys import argv
import pandas as pd
import operator
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rcParams
from functools import reduce
from collections import Counter, OrderedDict
import BANS as ban
import auxiliary as aux
import CONSTANTS as cst
# rcParams['path.sketch'] = (1, 100, 100)

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
cat = 'Artist'
frequencies = dict(
    reduce(operator.add, map(Counter, [dfPre[cat], dfPst[cat]]))
)
fDict = {
    k: v 
    for k, v in 
    sorted(frequencies.items(), key=lambda item: item[1])[::-1]
}
##############################################################################
# Plot
##############################################################################
COLORS = (
    '#f72585', '#2614ed', '#f8f7ff', 
    '#f038ff', '#e2ef70', '#9381ff'
)
ARTS = 50
(XRAN, YRAN) = ((0, 8000), (0-.5, ARTS-0.5))

# plt.xkcd()

mpl.rcParams['font.family'] = ['sans-serif']
keySort = list(fDict.keys())[:ARTS]
plt.style.use('dark_background')
mpl.rcParams['font.size'] = 12
(fig, ax) = plt.subplots(figsize=(15, 15))
for (row, key) in enumerate(keySort[::-1]):
    # Alternating variables --------------------------------------------------
    clr = COLORS[row%len(COLORS)]
    even = (row%2==0)
    (xO, xF) = (
        (0, fDict[key]) 
        if even else 
        (XRAN[1]-fDict[key], XRAN[1])
    )
    y = (
        row
        if even else
        ARTS-row
    )
    align = ('right' if even else 'left')
    xText = (xO-250 if even else xF+250)
    fText = (
        f'[{ARTS-row:02d}] {key}' 
        if not even else 
        f'{key} [{ARTS-row:02d}]'
    )
    # Plot lines -------------------------------------------------------------
    with mpl.rc_context({'path.sketch': (5, 25, 100)}):
        ax.plot((xO, xF), (y, y), lw=2, color=clr)
    # ax.plot(xF, y, '>', color=clr)
    # ax.plot(xO, y, '<', color=clr)
    ax.text(xText, y, fText, ha=align, va='center')
ax.vlines(
    range(*XRAN, 1000), ymin=YRAN[0], ymax=YRAN[1], 
    color='#ffffff33', ls='--'
)
ax.set_axis_off()
ax.set_xlim(XRAN[0]-500, XRAN[1]+500)
ax.set_ylim(*YRAN)
ax.set_facecolor('#000000')
# ax.set_yscale('log')