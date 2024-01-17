##############################################################################
# Plot Frequencies
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
        'chipmaligno', './data', './cache', './img', 600, 3
    )
else:
    (USERNAME, PTH_DTA, PTH_CHE, PTH_IMG, TOP, WRAN) = (
        argv[1], argv[2], argv[3], argv[4], int(argv[5]), int(argv[6])
    ) 
TOP_ARTISTS = 25
SORTED = True
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
DTA_RNK = DTA_CNT.rank(axis=0, ascending=False, method='first').astype(int)
DTA_RNK.loc[list(A_TOP['Artist'][:TOP_ARTISTS])]


DTA_RNK.loc['Pixies']