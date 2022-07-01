##############################################################################
# Constants
#   General constants common for all the scripts
##############################################################################
import auxiliary as aux
from datetime import date, timedelta

TIMEZONE = 'US/Pacific'
DAILY_PLAYCOUNT_LIMIT = 100
PLAYTIME_THRESHOLD = timedelta(minutes=30)
DF_DTE_RANGE = (date(2010, 1, 1), date(2050, 1, 1))
##############################################################################
# Colors
##############################################################################
C_NBLUE_LBLUE = ['#04067B', '#bdedf6']
C_WHITE_MGNTA = ['#ff006e11', '#fdfffcDD']
C_WHITE_NBLUE = ['#04067B11', '#fdfffcDD']
C_MAGNT_PRPLE = ['#ff006e', '#fdfffc', '#3a0ca3']
BLUE_CATS = [
    '#fe73aa', '#65dbff', '#aaa9f7', '#f6f4b9', 
    '#9efab9', '#dcddd8'
]
SAT_CATS = [
    '#3a86ff66', '#ff006e66', '#8338ec66',  '#f15bb566'
]
OTHER = '#101044'
MAPS = [aux.colorPaletteFromHexList([c, '#ffffff99']) for c in SAT_CATS]