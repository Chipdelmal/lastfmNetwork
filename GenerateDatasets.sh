#!/bin/bash
###############################################################################
# Generate Datasets
#   Cleans the original dataset for bans and name errors, downloads 
#   musicbrainz data for the artists' names, and filters the dataset for
#   dates and inflated counts
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
python Clean_Lastfm.py "$USRM" "$PTHO/data"
printf "${RED}* Downloading Musicbrainz artists' data...${NCL}\n"
python Download_Musicbrainz.py "$USRM" "$PTHO/data"
printf "${RED}* Filtering and amending dataframe...${NCL}\n"
python Fix_Dataframe.py "$USRM" "$PTHO/data"