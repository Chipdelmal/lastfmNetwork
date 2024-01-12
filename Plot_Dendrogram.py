##############################################################################
# Dendrogram
#
##############################################################################
import numpy as np
import pandas as pd
from os import path
from sys import argv
from matplotlib import colors
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, set_link_color_palette
from scipy.spatial.distance import squareform
import CONSTANTS as cst
import auxiliary as aux

if aux.isnotebook():
    (USERNAME, PTH_CHE, PTH_IMG, TOP, WRAN, TRANS_TYPE) = (
        'chipmaligno', './cache', './img', 150, 3, 'Frequency'
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
# Distance Matrix
###############################################################################
distMat = 1/F_MAT
tri_up = np.triu(distMat, k=0)
tri_lo = np.tril(distMat, k=0)
X = (tri_lo.T + tri_up)
d = X + X.T - np.diag(np.diag(X))
np.fill_diagonal(d, 0)
d[d == np.inf] = 1000
###############################################################################
# Linkage Matrix
###############################################################################
dists = squareform(d)
linkage_matrix = linkage(dists, "single")
###############################################################################
# Dendrogram
###############################################################################
fName = 'Dendrogram_{:04d}-{:02d}_{}.png'.format(TOP, WRAN, TRANS_TYPE[0])
set_link_color_palette(['#ff006e88']*10)
with plt.rc_context({'lines.linewidth': 0.4}):
    (fig, ax) = plt.subplots()
    dend = dendrogram(
        linkage_matrix, 
        orientation='right',
        labels=list(A_TOP['Artist']),
        above_threshold_color='#ff006e88', 
        count_sort='descending',
        distance_sort=True
    )
    ax.set_aspect(1e-4)
    plt.xticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', which='major', labelsize=.5, colors='#ffffff')
    plt.savefig(
        path.join(PTH_IMG, fName),
        dpi=1500, transparent=True, facecolor='k', 
        bbox_inches='tight'
    )
    plt.close('all')