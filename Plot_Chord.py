##############################################################################
# Chord Diagram
#   
##############################################################################
import numpy as np
import pandas as pd
from os import path
from sys import argv
from matplotlib import colors
import matplotlib.pyplot as plt
from mpl_chord_diagram import chord_diagram
import auxiliary as aux
import CONSTANTS as cst

if aux.isnotebook():
    (USERNAME, PTH_CHE, PTH_IMG, TOP, WRAN, ID) = (
        'chipmaligno', './cache', './img', 25, 5, 'Frequency'
    )
else:
    (USERNAME, PTH_CHE, PTH_IMG, TOP, WRAN, ID) = (
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
colorPalette = aux.colorPaletteFromHexList(cst.C_NBLUE_LBLUE)
pColors = [colorPalette(norm(i)) for i in selfProb]
###############################################################################
# Patch Matrix
###############################################################################
if ID=='Frequency':
    cMat = F_MAT.copy()
    np.fill_diagonal(cMat, 0)
else:
    cMat = P_MAT.copy()
    np.fill_diagonal(cMat, 0)
artsTop = A_TOP['Artist']
###############################################################################
# Plot Diagram
###############################################################################
chord_diagram(
    cMat, 
    names=artsTop[:TOP], 
    rotate_names=[True]*TOP,
    alpha=.65, pad=.5, gap=0.05,
    fontcolor='k', chordwidth=.7, width=0.1, 
    extent=360, fontsize=2.25, start_at=0,
    colors=pColors, use_gradient=True
)
fName = 'Chord_{:04d}-{:02d}_{}.png'
plt.savefig(
    path.join(PTH_IMG, fName.format(TOP, WRAN, ID[0])),
    dpi=750, transparent=True, facecolor='w', 
    bbox_inches='tight'
)
plt.close('all')