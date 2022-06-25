#!/bin/bash
###############################################################################
# Generate Datasets
#   
###############################################################################
USRM=$1
PTHO=$2

###############################################################################
# Terminal Colors
###############################################################################
RED='\033[0;31m'
NCL='\033[0m'
###############################################################################
# Run Scripts
###############################################################################
printf "${RED}* Cleaning Last.fm's dataset...${NCL}\n"
python Clean_Lastfm.py "$USRM" "$PTHO/dta"
printf "${RED}* Downloading Musicbrainz artists' data...${NCL}\n"
python Download_Musicbrainz.py "$USRM" "$PTHO/dta"
printf "${RED}* Filtering and amending dataframe...${NCL}\n"
python Filter_Dataframe.py "$USRM" "$PTHO/dta"