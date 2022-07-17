#!/bin/bash
###############################################################################
# Data Pipeline
#   USRM: Last.fm dataset username
#   PTHO: Path out
#   WRAN: Window range size (upper limit)
#   DTAP: Data process ("-dp" or empty for true, anything else for false)
#   SPLT: Strip plot export ("-sp" or empty for true, anything else for false)
#   CPLT: Chords plot ("-cp" or empty for true, anything else for false)
###############################################################################
USRM=$1
PTHO=$2
# Optional arguments ----------------------------------------------------------
DTAP=${3:-'-dp'}
WPLT=${4:-'-wp'}
SPLT=${5:-'-sp'}
CPLT=${6:-'-cp'}
# Constants -------------------------------------------------------------------
YLO=2012
YHI=2022
WLO=1
WHI=5
###############################################################################
# Terminal Colors
###############################################################################
RED='\033[0;31m'; NCL='\033[0m'
###############################################################################
# Generate Datasets and Matrices
###############################################################################
if [ "$DTAP" = "-dp" ]; then
    bash GenerateDatasets.sh $USRM $PTHO
    for top in 50 75 100 150 200 250 300 400 500 600
    do
        bash GenerateMatrices.sh $USRM $PTHO $top $WHI
    done
fi
###############################################################################
# Wordclouds
###############################################################################
if [ "$WPLT" = "-wp" ]; then
    for ylo in $(seq $YLO $YHI)
    do
        yhi=$(expr $ylo + 1)
        printf "${RED}* Wordcloud Plots [${ylo}:${yhi}]...${NCL}\n"
        python Plot_ArtistWordcloud.py $USRM "$PTHO/data" "$PTHO/img" "$PTHO/fonts" $ylo $yhi
    done
fi
###############################################################################
# Strip Plots
###############################################################################
if [ "$SPLT" = "-sp" ]; then
    for top in 100 150 200 250 300 400 500 600
    do
        printf "${RED}* Strip Plots [${top}]...${NCL}\n"
        python Plot_Scatter.py $USRM "$PTHO/data" "$PTHO/cache" "$PTHO/img" $top $WHI
    done
fi
###############################################################################
# Chord Plots
###############################################################################
if [ "$CPLT" = "-cp" ]; then
    for top in 50 100 150 200 250
    do
        for (( wran=$WLO;wran<=$WHI;wran++ ))
        do
            printf "${RED}* Chord Plots [${top}:$wran]...${NCL}\n"
            python Plot_Chord.py $USRM "$PTHO/cache" "$PTHO/img" $top $wran 'Frequency'
        done
    done
fi