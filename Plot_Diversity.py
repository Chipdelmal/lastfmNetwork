##############################################################################
# Plot Diversity
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
        'chipmaligno', './data', './cache', './img', 100, 3
    )
else:
    (USERNAME, PTH_DTA, PTH_CHE, PTH_IMG, TOP, WRAN) = (
        argv[1], argv[2], argv[3], argv[4], int(argv[5]), int(argv[6])
    ) 
WIN_SIZE = 8
# Internal Constants ----------------------------------------------------------
(CSCALE, SORTED) = ('Linear', True)
rotation = 45
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
(tInit, tEnd) = (min(DTA_CLN['Interval']), max(DTA_CLN['Interval']))
entries = ((tEnd-tInit).delta.days-WIN_SIZE)-1
(twInit, diversity) = (tInit, np.zeros(entries))
for tx in range(entries):
    twEnd = twInit + timedelta(days=WIN_SIZE)
    # Generate filter
    dteFltr = (
        list(DTA_CLN['Interval'] >= twInit),
        list(DTA_CLN['Interval'] < twEnd)
    )
    fltr = [all(i) for i in zip(*dteFltr)]
    # Get entries
    windowPlays = DTA_CLN[fltr]
    artCount = len(windowPlays['Artist'].unique())
    # Update variables
    diversity[tx] = artCount
    twInit += 1
diversityRolling = aux.rollingAverage(diversity, int(WIN_SIZE*4))
###############################################################################
# Plot
###############################################################################
fig, ax = plt.subplots()
ax.plot(diversity)
ax.plot(diversityRolling)