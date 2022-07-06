##############################################################################
# Nested Stockastic-Block Model
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
# Vertices names --------------------------------------------------------------
v_prop = g.new_vertex_property("string")
for (i, v) in enumerate(g.vertices()):
    v_prop[v] = artsTop[i]
###############################################################################
# Calculate NSBM
###############################################################################
state = minimize_nested_blockmodel_dl(
    g, state_args=dict(
        recs=[weight], 
        rec_types=["real-exponential"]
    )
)
mcmc_anneal(
    state, 
    beta_range=(1, 30), niter=200, 
    mcmc_equilibrate_args=dict(force_niter=10),
    verbose=False
)
###############################################################################
# Plot and Export
###############################################################################
# pos = sfdp_layout(g)
state.draw(
    # pos=pos,
    # vertex_text=v_prop, 
    # edge_marker_size=e_size,
    ink_scale=1,
    vertex_font_size=3,
    edge_marker_size=0.1,
    edge_pen_width=prop_to_size(weight, 0.075, 1.5, power=1),
    bg_color='#000000',
    output_size=(2000, 2000),
    output=path.join(
        PTH_IMG, 
        'NSBM_{:04d}-{:02d}_{}.png'.format(TOP, WRAN, TRANS_TYPE[0])
    )
)
###############################################################################
# Inspect Results
###############################################################################
# blocks = list(state.get_bs()[0])
# mylist = list(zip(artsTop, blocks))
# values = set(map(lambda x:x[1], mylist))
# clusters = [[y[0] for y in mylist if y[1]==x] for x in values]
# clusters