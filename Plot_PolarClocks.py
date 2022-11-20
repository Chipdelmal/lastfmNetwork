
from os import path
from sys import argv
import datetime
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib.pyplot import figure, show, rc
mpl.rcParams['axes.linewidth'] = 1
import CONSTANTS as cst
import auxiliary as aux

if aux.isnotebook():
    (USERNAME, PTH_DTA, PTH_IMG, PTH_FNT, YLO, YHI) = (
        'chipmaligno', './data', './img', './fonts', 2019, 2020
    )
else:
    (USERNAME, PTH_DTA, PTH_IMG, PTH_FNT, YLO, YHI) = (
        argv[1],  argv[2], argv[3], argv[4], int(argv[5]), int(argv[6])
    )
YEAR_ONLY = 'True'
##############################################################################
# Aesthetics parameters
##############################################################################
(WIDTH, HEIGHT, RESOLUTION) = (3840, 2160, 500)
(HOURS_OFFSET, N) = (6, 24)
(MAX_RANGE, AUTO_RANGE) = (4e3, False)
###############################################################################
# Read Data
###############################################################################
DTA_CLN = pd.read_csv(path.join(PTH_DTA, USERNAME+'_fxd.csv'), parse_dates=[3])
##############################################################################
# Read artists file
##############################################################################
msk = [
    (
        (i.date() >= datetime.date(YLO, 1, 1)) and 
        (i.date() < datetime.date(YHI, 1, 1))
    ) 
    if (type(i) is not float) else (False) for i in DTA_CLN['Date']
]
dates = DTA_CLN.loc[msk]["Date"]
hoursPlays = sorted([i.hour for i in dates if (type(i) is not float)], reverse=True)
hoursFreq = [hoursPlays.count(hD) for hD in list(range(23, -1, -1))]
#############################################################################
# Polar
#############################################################################
barSwatch = ['#bbdefb', '#64b5f6', '#2196f3', '#1976d2', '#0d47a1', '#001d5d']
(minFreq, maxFreq) = (min(hoursFreq), max(hoursFreq))
fig = figure(figsize=(8, 8), dpi=RESOLUTION)
ax = fig.add_axes([0.2, 0.1, 0.8, 0.8], polar=True)
step=  2*np.pi/N
(theta, radii, width) = (
    np.arange(0.0+step, 2*np.pi+step, step),
    hoursFreq,
    2*np.pi/24-0.001
)
bars = ax.bar(
    theta, radii, width=width, 
    bottom=0.0, zorder=25, edgecolor='#ffffff77', lw=.75
)
rvb = aux.colorPaletteFromHexList(barSwatch)
for r, bar in zip(radii, bars):
    bar.set_facecolor(rvb(r/(np.max(hoursFreq)*1)))
    bar.set_alpha(0.75)
# Shading -------------------------------------------------------------------
shades = 12
rvb = aux.colorPaletteFromHexList(
    ['#ffffff00', '#ffffff00', '#ffffff00', '#ffffff00']
)
colors = list(rvb(np.linspace(0, 1, shades)))
colors.extend(reversed(colors))
step =  np.pi/shades
yTop = (maxFreq*1.0035 if AUTO_RANGE else MAX_RANGE)
ax.bar(
    np.arange(0.0+step, 2*np.pi+step, step), 
    yTop,
    width=step,
    color=colors, #'white', #colors, 
    alpha=.2, edgecolor="black", ls='-', lw=.5,
    zorder=-1
)
ax.set_theta_zero_location("N")
label = '{}'.format(YLO)
ax.text(
    0.5, 0.75, label,
    horizontalalignment='center',
    verticalalignment='center',
    fontsize=60, color='#000000DD',
    transform=ax.transAxes, zorder=15
)
ax.text(
    0.5, 0.68, 'playcount: {}'.format(sum(hoursFreq)),
    horizontalalignment='center',
    verticalalignment='center',
    fontsize=20, color='#000000DD',
    transform=ax.transAxes, zorder=15
)
fig.patch.set_facecolor('#ffffff')
ax.set_ylim(0, yTop)
ax.set_yticks(np.arange(0, maxFreq, maxFreq*.25))
ax.set_yticklabels([])
ax.set_xticks(np.arange(np.pi*2, 0, -np.pi*2/24))
ax.set_xticklabels(np.arange(0, 24, 1))
ax.grid(which='major', axis='x', color='#000000', alpha=0, lw=.5, ls='--', zorder=15)
ax.grid(which='major', axis='y', color='#000000', alpha=0, lw=.5, ls='-', zorder=15)
ax.tick_params(direction='in', pad=10)
ax.tick_params(axis="x", labelsize=17.5, colors='#000000ff')
for spine in ax.spines.values():
    spine.set_edgewidth=2
fig.savefig(
    path.join(PTH_IMG, 'Clock_{}-{}.png'.format(YLO, YHI)),
    dpi=RESOLUTION, facecolor='White', edgecolor='w',
    orientation='portrait', papertype=None, format=None,
    transparent=False, bbox_inches='tight', pad_inches=.1,
    metadata=None
)
