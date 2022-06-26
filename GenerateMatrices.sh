#!/bin/bash
###############################################################################
# Generate Datasets
#   
###############################################################################
USRM=$1
PTHO=$2
TOPA=$3
WRAN=$4

###############################################################################
# Terminal Colors
###############################################################################
RED='\033[0;31m'
NCL='\033[0m'
###############################################################################
# Run Scripts
###############################################################################
# for top in 25 50 100 150 200 250 300 350 400
# do
for (( n=1; n<=$WRAN; n++ ))
do
    printf "${RED}* Generating Transitions [${TOPA}:${n}]...${NCL}\n"
    python Compute_Transitions.py $USRM "$PTHO/data" "$PTHO/cache" $TOPA $n
done
# done