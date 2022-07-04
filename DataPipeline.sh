#!/bin/bash
###############################################################################
# Data Pipeline
#   
###############################################################################
USRM=$1
PTHO=$2
WRAN=$3

bash GenerateDatasets.sh $USRM $PTHO
for top in 25 50 75 100 125 150 200 250 300 350 400 500 600
do
    bash GenerateMatrices.sh $USRM $PTHO $top $WRAN
done