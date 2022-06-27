##############################################################################
# Markov Playlist
#   Generates a playlist purely based on a Markov random walker process based
#   on the artists probability matrix and song frequencies.
##############################################################################
import numpy as np
import pandas as pd
from os import path
from sys import argv
from quantecon import MarkovChain
from collections import Counter
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
# Get Song Counts
###############################################################################
artsTop = list(A_TOP['Artist'])
artsSongDict = mkv.getSongCounts(DTA_CLN, artsTop)
###############################################################################
# Markov
###############################################################################
mc = MarkovChain(P_MAT, state_values=artsTop)
ss = mc.stationary_distributions[0]
ssPrint = ['{}: {}'.format(a, p) for (a, p) in zip(artsTop, ss)]
###############################################################################
# Simulate Trace
###############################################################################
(songsNumber, initArt) = (20, 'Caamp')
playlist = mkv.generateMarkovPlaylist(mc, songsNumber, artsSongDict, initArt)
playlist
