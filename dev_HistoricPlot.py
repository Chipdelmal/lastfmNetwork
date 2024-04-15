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
from matplotlib.ticker import EngFormatter
import matplotlib.pyplot as plt
from matplotlib import rcParams
from random import randrange
from functools import reduce
import matplotlib.font_manager as fm
from engineering_notation import EngNumber
from decimal import Decimal
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
dfPst = data[mask].drop_duplicates()
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
    '#f72585EE', '#2614edEE', '#f8f7ffEE', 
    '#f038ffEE', '#e2ef70EE', '#9381ffEE',
    '#fd796aEE', '#4E85C1EE'
)
ARTS = 50
(XRAN, YRAN) = ((0, 10000), (0-.5, ARTS-0.5))
ALTERNATE = False
fontsize = 20
maxYear = max(dfPst['Date']).year
prop = fm.FontProperties(fname='./fonts/Robgraves-lKYV.ttf')
mpl.rcParams['font.family'] = ['sans-serif']
mpl.rcParams['font.size'] = 12
keySort = list(fDict.keys())[:ARTS]

plt.style.use('dark_background')
(fig, ax) = plt.subplots(figsize=(20, 20))
for (row, key) in enumerate(keySort[::-1]):
    # Alternating variables --------------------------------------------------
    clr = COLORS[row%len(COLORS)]
    even = ((row%2==0) if ALTERNATE else True)
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
    if ALTERNATE:
        align = ('right' if even else 'left')
        xText = (xO-250 if even else xF+250)
        fText = (
            f'[{ARTS-row:02d}] {key}' 
            if not even else 
            f'{key} [{ARTS-row:02d}]'
        )
    else:
        align = ('right' if even else 'left')
        xText = (xO-250 if even else xF+250)
        fText = f'{key}'
    # Plot lines -------------------------------------------------------------
    with mpl.rc_context({'path.sketch': (8, 0.1, 100)}):
        ax.plot((xO+randrange(-25, 25), xF), (y, y), lw=2, color=clr)
    # ax.plot(xF, y, '>', color=clr)
    # ax.plot(xO, y, '<', color=clr)
    ax.text(
        xText, y, fText, 
        ha=align, va='center', 
        fontproperties=prop, fontsize=fontsize,
        color='#ffffffee'
    )
    if not ALTERNATE:
        ax.text(
            fDict[key]+250, y, 
            str(EngNumber(fDict[key])),
            ha='left', va='center', style='normal',
            fontproperties=prop, fontsize=fontsize
        )
with mpl.rc_context({'path.sketch': (2, 0.1, 100)}):
    for x in range(XRAN[0], XRAN[1]+500, 1000):
        ax.plot(
            (x, x), YRAN, 
            color='#ffffff55', ls='--'
        )
ax.text(
    .65, .2, f'Top {ARTS} {cat}s\n2005-{maxYear}',
    fontproperties=prop, fontsize=75,
    transform=ax.transAxes, rotation=25,
    color='#ffffffEE', ha='center', va='center'
)
ax.set_axis_off()
ax.set_xlim(XRAN[0]-500, XRAN[1]+500)
ax.set_ylim(*YRAN)
ax.set_facecolor('#000000')
