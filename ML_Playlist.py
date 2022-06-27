##############################################################################
# ML_Playlist
#
##############################################################################
import numpy as np
import pandas as pd
from os import path
from sys import argv
import category_encoders as ce
import chord as chd
import network as ntw
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
# Encode Categories
###############################################################################
artists = sorted(list(DTA_CLN['Artist'].unique()))
encoder = ce.HashingEncoder()
encoder.fit_transform(artists)
###############################################################################
# Setup Features and Labels
###############################################################################
features = encoder.transform(list(DTA_CLN['Artist']))
