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

if aux.isnotebook():
    (USERNAME, PTH_DTA, PTH_CHE, PTH_IMG, TOP, WRAN) = (
        'chipmaligno', './data', './cache', './img', 150, 3
    )
else:
    (USERNAME, PTH_DTA, PTH_CHE, PTH_IMG, TOP, WRAN) = (
        argv[1], argv[2], argv[3], argv[4], int(argv[5]), int(argv[6])
    ) 
# Internal Constants ----------------------------------------------------------
(CSCALE, SORTED) = ('Linear', True)
rotation = 90
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
# Daily intervals -------------------------------------------------------------
dteCpy = DTA_CLN['Date'].copy()
DTA_CLN['Interval'] = pd.to_datetime(dteCpy, errors='coerce', utc=True)
DTA_CLN['Interval'] = DTA_CLN['Interval'].dt.tz_localize(None).dt.to_period('D')
###############################################################################
# Fill Array
###############################################################################
for (ix, art) in enumerate(artists):
    artSmple = DTA_CLN[DTA_CLN['Artist']==art]
    playDates = list(artSmple['Interval'])
    playDays = [
        (datetime(i.year, i.month, i.day)-to.replace(tzinfo=None)).days 
        for i in playDates
    ]
    artCounts = dict(Counter(playDays))
    for d in list(artCounts.keys()):
        countsArray[ix, d] = artCounts[d]
###############################################################################
# Plot Scatter
###############################################################################
norm = colors.LogNorm(vmin=1, vmax=50)
artFontSize = np.interp(TOP, (50, 100, 250, 500, 600), (3, 3, 2, .25, .025))
yearFontSize = np.interp(TOP, (50, 250, 500), (8, 4.5, 4.5))
yearLineLen = np.interp(TOP, (50, 250, 500), (1.25, 2, 3))
artPad = np.interp(TOP, (50, 250, 500), (50, 25, 15))
pad = np.interp(TOP, (50, 250, 500), (.5, 2.5, 5))
if rotation==90:
    aligns = (
        ('left', 'center'), ('right', 'center'), 
        ('center', 'top'), ('center', 'bottom')
    )
else:
    aligns = (
        ('right', 'center'), ('left', 'center'), 
        ('right', 'top'), ('left', 'bottom')
    )
# norm = colors.Normalize(vmin=0, vmax=50) # np.max(countsArray))
# Plot artists ----------------------------------------------------------------
cYear = to.year
(fig, ax) = plt.subplots(figsize=(19.2/2, 10.8/2), dpi=1500)
# Counts Lines ----------------------------------------------------------------
for (r, art) in enumerate(artists):
    clr = cst.MAPS[r%len(cst.MAPS)]
    for day in np.nonzero(countsArray[r])[0]:
        ax.plot(
            [r-.325, r+.325], [day, day],
            color=clr(norm(countsArray[r][day])),
            lw=.2, zorder=5
        )
# Years -----------------------------------------------------------------------
for d in range(len(countsArray[0])):
    (tod, tfd) = (d, 0)
    if (to+timedelta(int(d))).year > cYear:
        # Year Lines ----------------------------------------------------------
        ax.hlines(
            d, -1, -yearLineLen, '#ffffffBB', 
            lw=.35, ls='-', zorder=-10
        )
        ax.hlines(
            d, len(artists), len(artists)+yearLineLen-1, '#ffffffbb', 
            lw=.35, ls='-', zorder=-10
        )
        cYear += 1
        # Years Text ----------------------------------------------------------
        if cYear < tf.year:
            ax.text(
                -pad-1, (d-tod)/2+tod+365/2, cYear, 
                fontsize=yearFontSize, color='#ffffff', rotation=rotation,
                ha=aligns[0][0], va=aligns[0][1]             
            )
            ax.text(
                len(artists)+pad, (d-tod)/2+tod+365/2, cYear, 
                fontsize=yearFontSize, color='#ffffff', rotation=rotation,
                ha=aligns[1][0], va=aligns[1][1]   
            )
        tod = d
# Artists Labels --------------------------------------------------------------
for (ix, a) in enumerate(artists):
    ax.text(
        ix, -artPad, a, 
        fontsize=artFontSize, color='w', rotation=rotation,
        ha=aligns[2][0], va=aligns[2][1]
        
    )
    ax.text(
        ix, len(countsArray[0])+artPad, a, 
        fontsize=artFontSize, color='w', rotation=rotation,
        ha=aligns[3][0], va=aligns[3][1]
    )
# Axes and Style --------------------------------------------------------------
# ax.set_aspect(.25/ax.get_data_ratio())
ax.set_facecolor('#000000')
ax.set_xlim(-pad*2, len(artists)+2*pad)
ax.set_ylim(-pad, daysTotal+pad)
ax.axis('off')
# Savefig ---------------------------------------------------------------------
fName = 'Scatter_{}.png'.format(str(TOP).zfill(4))
plt.savefig(
    path.join(PTH_IMG, fName), # dpi=1500, 
    transparent=True, facecolor='#000000', 
    bbox_inches='tight'
)
plt.close('all')
