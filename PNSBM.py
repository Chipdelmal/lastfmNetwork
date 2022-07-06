##############################################################################
# Posterior-Sampled Nested Stockastic-Block Model
##############################################################################
import numpy as np
import pandas as pd
from os import path
from sys import argv
from graph_tool.all import *
import auxiliary as aux
import network as ntw

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
# Delete self-loops and normalize ---------------------------------------------
np.fill_diagonal(F_MAT, 0)
np.fill_diagonal(P_MAT, 0)
P_MAT = ntw.normalizeMatrix(P_MAT)
# Get top artists -------------------------------------------------------------
artsTop = A_TOP['Artist']
###############################################################################
# Select Network
###############################################################################
mat = F_MAT if (TRANS_TYPE=='Frequency') else P_MAT
###############################################################################
# Generate Graph
###############################################################################
g = Graph(directed=True)
g.add_edge_list(np.transpose(mat.nonzero()))
weight = g.new_edge_property("double")
edges = list(g.edges())
for e in edges:
    weight[e] = mat[int(e.source()), int(e.target())]
###############################################################################
# Calculate NSBM
###############################################################################
state = NestedBlockState(
    g, 
    state_args=dict(
        recs=[weight], 
        rec_types=["real-exponential"]
    )
)
###############################################################################
# Sample the Posterior
###############################################################################
(dS, nmoves) = (0, 0)
for i in range(100):
    ret = state.multiflip_mcmc_sweep(niter=10)
    dS += ret[0]
    nmoves += ret[1]
mcmc_equilibrate(state, wait=1000, mcmc_args=dict(niter=10))
bs = []
def collect_partitions(s):
   global bs
   bs.append(s.get_bs())
mcmc_equilibrate(
    state, force_niter=10000, mcmc_args=dict(niter=10),
    callback=collect_partitions
)
pmode = PartitionModeState(bs, nested=True, converge=True)
pv = pmode.get_marginal(g)
bs = pmode.get_max_nested()
state = state.copy(bs=bs)
###############################################################################
# Plot and Export
###############################################################################
fName = 'PRTC{}_{:03d}-{:02d}.png'
state.draw(
    vertex_shape="pie",
    layout="radial",
    ink_scale=1,
    edge_color=weight,
    edge_pen_width=prop_to_size(weight, .05, 2, power=1, log=False),
    edge_marker_size=0.1,
    vertex_pie_fractions=pv,
    output_size=(2000, 2000),
    bg_color='#000000',
    output=path.join(
        PTH_IMG, 
        'NSBM_{:04d}-{:02d}_{}.png'.format(TOP, WRAN, TRANS_TYPE[0])
    )
)