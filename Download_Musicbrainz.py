##############################################################################
# Musicbrainz: Download
#   
##############################################################################
from os import path
from sys import argv
import pandas as pd
import musicbrainzngs as mb
import KEYS
import auxiliary as aux
import musicbrainz as mbz

if aux.isnotebook():
    (USERNAME, PTH_DTA) = ('chipmaligno', './data')
else:
    (USERNAME, PTH_DTA) = argv[1:]
##############################################################################
# Logging In
##############################################################################
mb.auth(KEYS.MB_USR, KEYS.MB_PSW)
mb.set_useragent(KEYS.MB_NM, KEYS.MB_V, KEYS.MB_URL)
##############################################################################
# Download Data
##############################################################################
data = pd.read_csv(path.join(PTH_DTA, USERNAME+'_cln.csv'), parse_dates=[3])
mbz.parseFromMusicbrainz(data, PTH_DTA, USERNAME)
