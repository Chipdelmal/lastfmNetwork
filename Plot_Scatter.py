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
from datetime import datetime
from collections import Counter
import CONSTANTS as cst
import auxiliary as aux
import markov as mkv

#if aux.isnotebook():
(USERNAME, PTH_DTA, PTH_CHE, PTH_IMG, TOP, WRAN) = (
    'chipmaligno', './data', './cache', './img', 100, 3
)
# else:
#     (USERNAME, PTH_DTA, PTH_CHE, PTH_IMG, TOP, WRAN) = (
#         argv[1], argv[2], argv[3], argv[4], int(argv[5]), int(argv[6])
#     )
# Internal Constants ----------------------------------------------------------
(SELF_LOOP, CSCALE) = (False, 'Linear')
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
daysTotal = (tf-to).days
artists = sorted(list(DTA_CLN['Artist'].unique())) # sorted(list(A_TOP['Artist'])) # 
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
norm = colors.LogNorm(vmin=1, vmax=50)
# norm = colors.Normalize(vmin=0, vmax=50) # np.max(countsArray))
colorPalA = aux.colorPaletteFromHexList(cst.C_WHITE_NBLUE)
colorPalB = aux.colorPaletteFromHexList(cst.C_WHITE_MGNTA)
# Iterate through artists -----------------------------------------------------
# r = 10
# pad = 20
# (fig, ax) = plt.subplots()
# for (r, _) in enumerate(artists[:]):
#     clrs = [colorPalette(norm(i)) for i in countsArray[r]]
#     ax.scatter(
#         [i*r for i in range(daysTotal)], 
#         [r]*daysTotal,
#         c=clrs,
#         s=1,
#     )
# ax.set_aspect(.001/ax.get_data_ratio())
# ax.set_xlim(-pad, daysTotal+pad)
# ax.set_ylim(-pad/2, len(artists)+pad/2)
# ax.axis('off')
# fName = 'Scatter.png'
# plt.savefig(
#     path.join(PTH_IMG, fName),
#     dpi=1000, transparent=True, facecolor='w', 
#     bbox_inches='tight'
# )
# plt.close('all')
# Iterate through artists -----------------------------------------------------
r = 10
yPad = 4
pad = 10
(fig, ax) = plt.subplots(figsize=(10,6))
for (r, art) in enumerate(artists[:]):
    clr = colorPalA if r % 2 == 0 else colorPalB
    # ax.text(
    #     -2, r*yPad, art, fontsize=1, color='w', 
    #     horizontalalignment='right',
    #     verticalalignment='center'
    # )
    for day in np.nonzero(countsArray[r])[0]:
        plt.plot(
            [day, day+25], [r+r*yPad-2.5, r+r*yPad+2.5],
            color=clr(norm(countsArray[r][day])),
            lw=.25
        )
ax.set_aspect(1/ax.get_data_ratio())
ax.set_facecolor('k')
ax.set_xlim(-pad, daysTotal+pad*10)
ax.set_ylim(-pad, len(artists)+pad)
ax.axis('off')
fName = 'Scatter.png'
plt.savefig(
    path.join(PTH_IMG, fName),
    dpi=1000, transparent=True, facecolor='k', 
    bbox_inches='tight'
)
plt.close('all')