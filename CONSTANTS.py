##############################################################################
# Constants
#   General constants common for all the scripts
##############################################################################
from datetime import date, timedelta

TIMEZONE = 'US/Pacific'
DAILY_PLAYCOUNT_LIMIT = 100
PLAYTIME_THRESHOLD = timedelta(minutes=30)
DF_DTE_RANGE = (date(2010, 1, 1), date(2050, 1, 1))
##############################################################################
# Colors
##############################################################################
C_NBLUE_LBLUE = ['#04067B', '#bdedf6']
C_MAGNT_PRPLE = ['#ff006e', '#fdfffc', '#3a0ca3']