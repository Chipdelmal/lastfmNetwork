#!/bin/bash
###############################################################################
# Data Pipeline
#   USRM: Last.fm dataset username
#   PTHO: Path out
#   WRAN: Window range size (upper limit)
#   DTAP: Data process ("dp" or empty for true, anything else for false)
#   SPLT: Strip plot export ("sp" or empty for true, anything else for false)
#   CPLT: Chords plot ("cp" or empty for true, anything else for false)
###############################################################################
USRM=$1
PTHO=$2
WRAN=${3:-3}
# Optional arguments ----------------------------------------------------------
DTAP=${4:-'dp'}
SPLT=${5:-'sp'}
CPLT=${6:-'cp'}
###############################################################################
# Terminal Colors
###############################################################################
RED='\033[0;31m'
NCL='\033[0m'
###############################################################################
# Generate Datasets and Matrices
###############################################################################
if [ "$DTAP" = "dp" ]; then
    bash GenerateDatasets.sh $USRM $PTHO
    for top in 50 75 100 150 200 250 300 400 500 600
    do
        bash GenerateMatrices.sh $USRM $PTHO $top $WRAN
    done
fi
###############################################################################
# Strip Plots
###############################################################################
if [ "$SPLT" = "sp" ]; then
    for top in 100 150 200 250 300 400 500 600
    do
        printf "${RED}* Scatter Plots [${top}]...${NCL}\n"
        python Plot_Scatter.py $USRM "$PTHO/data" "$PTHO/cache" "$PTHO/img" $top $WRAN
    done
fi
###############################################################################
# Chord Plots
###############################################################################
if [ "$CPLT" = "cp" ]; then
    for top in 50 100 150 200 250 350
    do
        for (( wran=1;wran<=$WRAN;wran++ ))
        do
            printf "${RED}* Chord Plots [${top}:$wran]...${NCL}\n"
            python Plot_Chord.py $USRM "$PTHO/cache" "$PTHO/img" $top $wran 'Frequency'
        done
    done
fi