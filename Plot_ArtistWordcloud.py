##############################################################################
# Plot Artist Clouds
#
##############################################################################
import pandas as pd
from os import path
from sys import argv
from datetime import date
from matplotlib import colors
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import CONSTANTS as cst
import auxiliary as aux

if aux.isnotebook():
    (USERNAME, PTH_DTA, PTH_IMG, PTH_FNT, YLO, YHI) = (
        'chipmaligno', './data', './img', './fonts', 2021, 2022
    )
else:
    (USERNAME, PTH_DTA, PTH_IMG, PTH_FNT, YLO, YHI) = (
        argv[1],  argv[2], argv[3], argv[4], int(argv[5]), int(argv[6])
    )
(WIDTH, HEIGHT, RESOLUTION, DATE_PRINT) = (int(1920/2), int(1920/2), 750, True)
###############################################################################
# Read Data
###############################################################################
DTA_CLN = pd.read_csv(path.join(PTH_DTA, USERNAME+'_fxd.csv'), parse_dates=[3])
###############################################################################
# Filter Dates
###############################################################################
(yLo, yHi) = ((YLO, 1), (YHI, 1))
msk = [
    (
        (i.date() >= date(yLo[0], yLo[1], 1)) and 
        (i.date() <  date(yHi[0], yHi[1], 1))
    ) for i in DTA_CLN['Date']
]
data = DTA_CLN.loc[msk]
###############################################################################
# Setup Structures
###############################################################################
artists = sorted(data.get('Artist').unique())
artistCount = data.groupby('Artist').size().sort_values(ascending=False)
if DATE_PRINT:
    artistCount = artistCount.append(
        pd.Series([10*max(artistCount.values)], index=[str(yLo[0])])
    )
##############################################################################
# Wordcloud
##############################################################################
fontFile = path.join(PTH_FNT, 'Prompt-Thin.ttf')
fontPath = fontFile if path.exists(fontFile) else None
wordcloudDef = WordCloud(
    width=WIDTH, height=HEIGHT, max_words=2000,
    relative_scaling=.5, min_font_size=9, font_path=fontPath,
    background_color="rgba(1, 1, 1, 0)", mode='RGBA',
    colormap=cst.WORDCLOUD_MAP
)
wordcloud = wordcloudDef.generate_from_frequencies(artistCount)
##############################################################################
# Export Figure
##############################################################################
fig = plt.figure(figsize=(20, 20*(HEIGHT/WIDTH)), facecolor='w')
ax = fig.add_subplot(111)
plt.imshow(wordcloud, interpolation='bilinear')
plt.rcParams["font.family"] = "verdana"
plt.tight_layout(pad=0)
plt.axis("off")
plt.savefig(
    path.join(PTH_IMG, 'Wordcloud_{}-{}.png'.format(yLo[0], yHi[0])),
    dpi=RESOLUTION, facecolor='black', edgecolor='black',
    orientation='portrait', papertype=None, format=None,
    transparent=False, bbox_inches='tight', pad_inches=0.0,
    metadata=None
)
plt.close('all')
