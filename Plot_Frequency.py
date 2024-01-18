##############################################################################
# Plot Frequencies
##############################################################################

import numpy as np
import pandas as pd
from os import path
from sys import argv
from matplotlib import colors
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import Counter
import CONSTANTS as cst
import auxiliary as aux

if aux.isnotebook():
    (USERNAME, PTH_DTA, PTH_CHE, PTH_IMG, TOP, WRAN) = (
        'chipmaligno', './data', './cache', './img', 600, 3
    )
else:
    (USERNAME, PTH_DTA, PTH_CHE, PTH_IMG, TOP, WRAN) = (
        argv[1], argv[2], argv[3], argv[4], int(argv[5]), int(argv[6])
    ) 
TOP_ARTISTS = 10
SORTED = True
HIGHLIGHT = 'Wilco' # None
###############################################################################
# Read Data
###############################################################################
fName = '{}_{:04}-{:02}'.format(USERNAME, TOP, WRAN)
DTA_CLN = pd.read_csv(path.join(PTH_DTA, USERNAME+'_fxd.csv'), parse_dates=[3])
A_TOP = pd.read_csv(path.join(PTH_CHE, fName+'_top.csv'))
###############################################################################
# Process Prerequisites
###############################################################################
# Numpy array shape -----------------------------------------------------------
(to, tf) = (min(DTA_CLN['Date']), max(DTA_CLN['Date']))
daysTotal = (tf-to).days+1
# artists = sorted(list(DTA_CLN['Artist'].unique()))
artists = sorted(list(A_TOP['Artist'])) if not SORTED else list(A_TOP['Artist'])
countsArray = np.zeros([len(artists), daysTotal], dtype=np.int16)
daysTotals = np.sum(countsArray, axis=0)
# Timely intervals ------------------------------------------------------------
dteCpy = DTA_CLN['Date'].copy()
DTA_CLN['Interval'] = pd.to_datetime(dteCpy, errors='coerce', utc=True)
DTA_CLN['Interval'] = DTA_CLN['Interval'].dt.tz_localize(None).dt.to_period('Y')
###############################################################################
# Time counts
###############################################################################
DTA_CLN['count'] = pd.Series([1 for _ in range(len(DTA_CLN.index))])
DTA_CNT = DTA_CLN.pivot_table(
    index='Artist', columns='Interval', values='count',
    aggfunc="sum", fill_value=0,
).rename_axis(None, axis=1).reset_index('Artist').set_index('Artist')
###############################################################################
# Get Sorting
###############################################################################
year = 2024
freqSort = {}
for year in range(2012, 2024):
    fltrd = DTA_CLN[DTA_CLN['Interval']==str(year)]
    freqSort[year] = Counter(fltrd['Artist']).most_common()
###############################################################################
# Filter top
###############################################################################
tops = [freqSort[y][:TOP_ARTISTS] for y in range(2012, 2024)]
nums = [len(freqSort[y]) for y in range(2012, 2024)]
names = set([item for row in [[x[0] for x in y] for y in tops] for item in row])
A_TOP[A_TOP['Artist'].isin(names)]
###############################################################################
# Generate Ranking
###############################################################################
# DTA_RNK = DTA_CNT.rank(axis=0, ascending=False, method='min').astype(int)
# DTA_RNK_FULL = DTA_RNK.loc[list(A_TOP['Artist'][:TOP_ARTISTS])]
artistsList = list(A_TOP['Artist'][:TOP_ARTISTS])
DTA_RNK_TOP = DTA_CNT.loc[artistsList].rank(
    axis=0, ascending=False, method='first'
).astype(int)
DTA_RNK_TOP = DTA_RNK_TOP.sort_values(by=DTA_RNK_TOP.columns[0])
# DTA_RNK_TOP.loc['Wilco']
###############################################################################
# Plot
###############################################################################
COLS = [
    '#8691AC', '#9BBBCB', '#DBC3A8', '#C8C4E4', 
    '#F5E4BF', '#DFA145', '#CC8D6F', '#D1C87A',
    '#D3B1C1', '#9FC4E5', '#FFC41A', '#FCC176', '#A1BE7C'
]
FONT_SIZE = 14

(yInts, arts) = (
    [int(i.year) for i in list(DTA_RNK_TOP.columns)],
    list(A_TOP['Artist'][:TOP_ARTISTS])
)

artUnsorted = list(DTA_RNK_TOP.index)
(artSortStart, artSortEnd) = (
    DTA_RNK_TOP[DTA_RNK_TOP.columns[0]].values,
    DTA_RNK_TOP[DTA_RNK_TOP.columns[-1]].values
)
(lblL, lblR) = (
    [x for _,x in sorted(zip(artSortStart, artUnsorted))[::-1]],
    [x for _,x in sorted(zip(artSortEnd, artUnsorted))[::-1]]
)

(fig, ax) = plt.subplots(figsize=(15, 5))
for (ix, art) in enumerate(arts[:]):
    if art==HIGHLIGHT:
        (color, zorder) = ('#000000', 10)
    else:
        (color, zorder) = (COLS[ix%len(COLS)], 1)
    ax.plot(
        yInts, 
        [TOP_ARTISTS-i for i in list(DTA_RNK_TOP.loc[art])],
        c=color, lw=5,
        zorder=zorder, alpha=0.75
    )
    ax.scatter(
        yInts, 
        [TOP_ARTISTS-i for i in list(DTA_RNK_TOP.loc[art])], 
        c='w', ec=color, alpha=1, s=75, lw=2,
        zorder=zorder
    )
ax.set_xticks(yInts)
ax.set_xticklabels(yInts, size=FONT_SIZE, rotation=0)
ax.set_xlim(min(yInts)-.125, max(yInts)+.125)
ticks = range(0, TOP_ARTISTS)
ax.set_yticks(range(0, TOP_ARTISTS))
ax.set_yticklabels(lblL, size=FONT_SIZE)
ax.tick_params(axis='both', which='both',length=0)
ax2 = ax.twinx()
ax2.tick_params(axis='both', which='both',length=0)
ax2.set_ylim([0, TOP_ARTISTS])
ax2.set_yticks(np.arange(0.5, TOP_ARTISTS+0.5))
ax2.set_yticklabels(lblR, size=FONT_SIZE)
for x in (ax, ax2):
    [x.spines[i].set_visible(False) for i in ('top', 'right', 'bottom', 'left')]
[ax.axvline(i, 0, 1, ls=':', color='#58586B', zorder=-1) for i in yInts]
# [ax.axhline(i, 0, 1, ls=':', color='#58586B') for i in range(0, TOP_ARTISTS, 5)]