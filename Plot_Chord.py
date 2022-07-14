##############################################################################
# Chord Diagram
#   Exports a chord diagram with a given number of artists and a window range
#   (as exported by "Compute_Transitions.py")
##############################################################################
import numpy as np
import pandas as pd
from os import path
from sys import argv
from matplotlib import colors
import matplotlib.pyplot as plt
from mpl_chord_diagram import chord_diagram
import chord as chd
import network as ntw
import CONSTANTS as cst
import auxiliary as aux

if aux.isnotebook():
    (USERNAME, PTH_CHE, PTH_IMG, TOP, WRAN, TRANS_TYPE) = (
        'chipmaligno', './cache', './img', 100, 3, 'Frequency'
    )
else:
    (USERNAME, PTH_CHE, PTH_IMG, TOP, WRAN, TRANS_TYPE) = (
        argv[1], argv[2], argv[3], int(argv[4]), int(argv[5]), argv[6]
    )
# Internal Constants ----------------------------------------------------------
(SELF_LOOP, CSCALE) = (False, 'Linear')
###############################################################################
# Read Data
###############################################################################
fName = '{}_{:04}-{:02}'.format(USERNAME, TOP, WRAN)
F_MAT = np.load(path.join(PTH_CHE, fName+'_Fmat.npy'))
P_MAT = np.load(path.join(PTH_CHE, fName+'_Pmat.npy'))
A_TOP = pd.read_csv(path.join(PTH_CHE, fName+'_top.csv'))
###############################################################################
# Colors
###############################################################################
selfProb = np.diag(P_MAT.copy(), k=0)
# Color scale -----------------------------------------------------------------
if CSCALE == 'Log':
    norm = colors.LogNorm(vmin=np.min(selfProb), vmax=np.max(selfProb))
else:
    norm = colors.Normalize(vmin=np.min(selfProb), vmax=np.max(selfProb))
# Colors list -----------------------------------------------------------------
colorPalette = aux.colorPaletteFromHexList(cst.C_NBLUE_WHITE)
pColors = [colorPalette(norm(i)) for i in selfProb]
###############################################################################
# Patch Matrix
###############################################################################
artsTop = A_TOP['Artist']
if TRANS_TYPE=='Frequency':
    cMat = F_MAT.copy()
    np.fill_diagonal(cMat, 0)
    fontSize = np.interp(
        TOP, (25, 100, 150, 300, 350), (3, 1.75, 1.25, .65, .45)
    )
else:
    cMat = P_MAT.copy()
    np.fill_diagonal(cMat, 0)
    cMat = ntw.normalizeMatrix(cMat)
    fontSize = np.interp(TOP, (25, 100, 150), (4, 1.75, 1.25))
###############################################################################
# Plot Diagram
###############################################################################
pad = 1.5
ax = chd.chord_modded(
    cMat, 
    names=artsTop[:TOP], 
    rotate_names=[True]*TOP,
    alpha=.75, pad=.5, gap=0.05, fontsize=fontSize,
    fontcolor='w', chordwidth=.7, width=0.1, 
    extent=360, start_at=0,
    colors=pColors, use_gradient=True
)
ax.set_xlim(-pad, pad)
ax.set_ylim(-pad, pad)
ax.axis('off')
fName = 'Chord_{:04d}-{:02d}_{}.png'.format(TOP, WRAN, TRANS_TYPE[0])
plt.savefig(
    path.join(PTH_IMG, fName),
    dpi=1000, transparent=True, facecolor='k', 
    bbox_inches='tight'
)
plt.close('all')