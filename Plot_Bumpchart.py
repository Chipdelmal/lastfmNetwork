##############################################################################
# Plot Bumpchart
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
    (USERNAME, PTH_DTA, PTH_CHE, PTH_IMG, TOP, WRAN, YLO, YHI) = (
        'chipmaligno', './data', './cache', './img', 600, 3, 2012, 2023
    )
else:
    (USERNAME, PTH_DTA, PTH_CHE, PTH_IMG, TOP, WRAN, YLO, YHI) = (
        argv[1], argv[2], argv[3], argv[4], int(argv[5]), int(argv[6]),
        int(argv[7]), int(argv[8])
    )
###############################################################################
# Read Data
###############################################################################
fName = '{}_{:04}-{:02}'.format(USERNAME, TOP, WRAN)
DTA_CLN = pd.read_csv(path.join(PTH_DTA, USERNAME+'_fxd.csv'), parse_dates=[3])
DTA_MBZ = pd.read_csv(path.join(PTH_DTA, USERNAME+'_mbz.csv'))
A_TOP = pd.read_csv(path.join(PTH_CHE, fName+'_top.csv'))
###############################################################################
# Get Genres
###############################################################################
# GEN_LABS = ('Gen_1', 'Gen_2', 'Gen_3')
# artGen = {
#     DTA_MBZ.iloc[i]['Artist']: set([DTA_MBZ.iloc[i][gen] for gen in GEN_LABS])
#     for i in range(DTA_MBZ.shape[0])
# }
# # Get top genres --------------------------------------------------------------
# gensList = []
# for gen in GEN_LABS:
#     gensList.extend(DTA_MBZ[gen])
# GEN_TOP = Counter(gensList)
# GEN_TOP.most_common()
###############################################################################
# Filter Dates
###############################################################################
msk = [
    (
        (i.date() >= datetime.date(YLO[0], YLO[1], 1)) and 
        (i.date() < datetime.date(YHI[0], YHI[1], 1))
    ) 
    if (type(i) is not float) else (False) for i in DTA_CLN['Date']
]
data = DTA_CLN.loc[msk]