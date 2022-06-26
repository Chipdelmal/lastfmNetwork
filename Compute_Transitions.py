##############################################################################
# Transitions Matrix
#   
##############################################################################
from sys import argv
from os import path
import numpy as np
import pandas as pd
import auxiliary as aux
import network as ntw
import CONSTANTS as cst

if aux.isnotebook():
    (USERNAME, PTH_DTA, PTH_CHE, TOP, WRAN) = (
        'chipmaligno', './data', './cache', 50, 5
    )
else:
    (USERNAME, PTH_DTA, TOP, WRAN) = (
        argv[1], argv[2], int(argv[3]), int(argv[4])
    )
###############################################################################
# Read Data
###############################################################################
DTA_CLN = pd.read_csv(path.join(PTH_DTA, USERNAME+'_fxd.csv'), parse_dates=[3])
###############################################################################
# Setup Structures
###############################################################################
arts = sorted(list(DTA_CLN['Artist'].unique()))
(artsNum, playNum) = (len(arts), DTA_CLN.shape[0])
artsCount = DTA_CLN.groupby('Artist').size().sort_values(ascending=False)
artsCount = artsCount.to_frame('Count').reset_index()
###############################################################################
# Filter Top
###############################################################################
artsTop = list(artsCount['Artist'])[:TOP]
artsTopSet = set(artsTop)
###############################################################################
# Iterate Through Plays (Generate Frequency and Probability Matrix)
###############################################################################
tMat = ntw.calcWeightedTransitionsMatrix(
    DTA_CLN, artsTop, windowRange=(1, WRAN), 
    timeThreshold=cst.PLAYTIME_THRESHOLD, verbose=True
)
pMat = ntw.normalizeMatrix(tMat)
###############################################################################
# Save Matrices
###############################################################################
fName = '{}_{:04}-{:02}'.format(USERNAME, TOP, WRAN)
np.save(path.join(PTH_CHE, fName+'_Fmat'), tMat)
np.save(path.join(PTH_CHE, fName+'_Pmat'), pMat)