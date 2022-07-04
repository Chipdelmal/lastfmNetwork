##############################################################################
# Plot Scatter
#
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
import markov as mkv

#if aux.isnotebook():
(USERNAME, PTH_DTA, PTH_CHE, PTH_IMG, TOP, WRAN) = (
    'chipmaligno', './data', './cache', './img', 250, 3
)
# else:
#     (USERNAME, PTH_DTA, PTH_CHE, PTH_IMG, TOP, WRAN) = (
#         argv[1], argv[2], argv[3], argv[4], int(argv[5]), int(argv[6])
#     )
# Internal Constants ----------------------------------------------------------
(SELF_LOOP, CSCALE, SORTED) = (False, 'Linear', True)
###############################################################################
# Read Data
###############################################################################
fName = '{}_{:04}-{:02}'.format(USERNAME, TOP, WRAN)
DTA_CLN = pd.read_csv(path.join(PTH_DTA, USERNAME+'_fxd.csv'), parse_dates=[3])
F_MAT = np.load(path.join(PTH_CHE, fName+'_Fmat.npy'))
P_MAT = np.load(path.join(PTH_CHE, fName+'_Pmat.npy'))
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
# Daily intervals -------------------------------------------------------------
dteCpy = DTA_CLN['Date'].copy()
DTA_CLN['Interval'] = pd.to_datetime(dteCpy, errors='coerce', utc=True)
DTA_CLN['Interval'] = DTA_CLN['Interval'].dt.tz_localize(None).dt.to_period('D')
###############################################################################
# Fill Array
###############################################################################
# ix = 100
# art = artists[ix]
for (ix, art) in enumerate(artists):
    artSmple = DTA_CLN[DTA_CLN['Artist'] == art]
    playDates = list(artSmple['Interval'])
    playDays = [
        (datetime(i.year, i.month, i.day)-to.replace(tzinfo=None)).days 
        for i in playDates
    ]
    artCounts = dict(Counter(playDays))
    for d in list(artCounts.keys()):
        countsArray[ix, d] = artCounts[d]
# plt.imshow(countsArray, vmin=0, vmax=2)
###############################################################################
# Plot Scatter
###############################################################################
norm = colors.LogNorm(vmin=1, vmax=40)
# norm = colors.Normalize(vmin=0, vmax=50) # np.max(countsArray))
# Iterate through artists -----------------------------------------------------
pad = 1
artPad = 5
cYear = to.year
(fig, ax) = plt.subplots(figsize=(19.2/2, 10.8/2), dpi=1500) #plt.subplots(figsize=(6, 10))
for (r, art) in enumerate(artists):
    clr = cst.MAPS[r%len(cst.MAPS)]
    for day in np.nonzero(countsArray[r])[0]:
        plt.plot(
            [r-.325, r+.325], [day, day],
            color=clr(norm(countsArray[r][day])),
            lw=.2, zorder=5
        )
for d in range(len(countsArray[0])):
    (tod, tfd) = (d, 0)
    if (to+timedelta(int(d))).year > cYear:
        plt.hlines(
            d, -pad*100, -pad, '#ffffffBB', 
            lw=.35, ls='-', zorder=-10
        )
        plt.hlines(
            d, len(artists)+pad, len(artists)+100*pad, '#ffffffbb', 
            lw=.35, ls='-', zorder=-10
        )
        # plt.hlines(
        #     d, -pad, len(artists)+pad, '#ffffff22', 
        #     lw=.2, ls='-', zorder=-10
        # )
        # ax.axhspan(
        #     d+5, d+365-5, -pad, len(artists)+pad, 
        #     fc = '#ffffff11', zorder=-10
        #     # lw=.2, ls='-', zorder=-10 
        # )
        cYear += 1
        if cYear < tf.year:
            ax.text(
                -2, (d-tod)/2+tod+365/2, cYear, fontsize=4.5, 
                color='#ffffff', 
                horizontalalignment='right',
                verticalalignment='center',
                rotation=90
            )
            ax.text(
                len(artists)+2, (d-tod)/2+tod+365/2, cYear, fontsize=4.5, 
                color='#ffffff', 
                horizontalalignment='right',
                verticalalignment='center',
                rotation=90
            )
        tod = d
for (ix, a) in enumerate(artists):
    ax.text(
        ix, -artPad, a, 
        fontsize=1.75, color='w', 
        horizontalalignment='center',
        verticalalignment='top',
        rotation=90
    )
    ax.text(
        ix, len(countsArray[0])+4*artPad, a, 
        fontsize=1.75, color='w', 
        horizontalalignment='center',
        verticalalignment='bottom',
        rotation=90
    )
# ax.set_aspect(.25/ax.get_data_ratio())
ax.set_facecolor('#000000')
ax.set_xlim(-pad*2, len(artists)+2*pad)
ax.set_ylim(-pad, daysTotal+pad)
ax.axis('off')
fName = 'Scatter.png'
plt.savefig(
    path.join(PTH_IMG, fName), # dpi=1500, 
    transparent=True, facecolor='#000000', 
    bbox_inches='tight'
)
plt.close('all')