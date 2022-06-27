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

if aux.isnotebook():
    (USERNAME, PTH_DTA, PTH_CHE, PTH_IMG, TOP, WRAN) = (
        'chipmaligno', './data', './cache', './img', 100, 3
    )
else:
    (USERNAME, PTH_DTA, PTH_CHE, PTH_IMG, TOP, WRAN) = (
        argv[1], argv[2], argv[3], argv[4], int(argv[5]), int(argv[6])
    )
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
artists = sorted(list(A_TOP['Artist'])) # sorted(list(DTA_CLN['Artist'].unique()))
countsArray = np.empty([len(artists), daysTotal])
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
# norm = colors.LogNorm(vmin=1, vmax=5)
norm = colors.Normalize(vmin=0, vmax=25) # np.max(countsArray))
colorPalette = aux.colorPaletteFromHexList(cst.C_WHITE_NBLUE)
# Iterate through artists -----------------------------------------------------
r = 100
pad = 20
(fig, ax) = plt.subplots()
for (r, _) in enumerate(artists[:]):
    clrs = [colorPalette(norm(i)) for i in countsArray[r]]
    ax.scatter(
        [i*r for i in range(daysTotal)], 
        [r]*daysTotal,
        c=clrs,
        s=1,
    )
ax.set_aspect(.001/ax.get_data_ratio())
ax.set_xlim(-pad, daysTotal+pad)
ax.set_ylim(-pad/2, len(artists)+pad/2)
ax.axis('off')
fName = 'Scatter.png'
plt.savefig(
    path.join(PTH_IMG, fName),
    dpi=1000, transparent=True, facecolor='w', 
    bbox_inches='tight'
)
plt.close('all')