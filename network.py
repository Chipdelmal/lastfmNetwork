import numpy as np
from datetime import timedelta

def calcTransitionsMatrix(
        inMat, scrobblesDF, artists,
        window=1, timeThreshold=timedelta(minutes=30), 
        verbose=False
    ):
    playNum = scrobblesDF.shape[0]
    tMat = inMat.copy()
    for ix in range(playNum-window):
        # pl0 is newer than pl1 -----------------------------------------------
        (pl0, pl1) = [scrobblesDF.iloc[i] for i in (ix, ix+window)]
        (pa0, pa1) = [play['Artist'] for play in (pl0, pl1)]
        # Check if both artists are in the top set , and time between is low --
        pTop = (pa0 in artists) and (pa1 in artists)
        pTime = (pl0['Date']-pl1['Date']) <= timeThreshold
        if pTop:
            (px0, px1) = [artists.index(artName) for artName in (pa0, pa1)]
            tMat[px0, px1] = (tMat[px0, px1] + 1)
        if verbose:
            print(f'Processing: {ix}/{playNum}', end='\r')
    return tMat

def calcWeightedTransitionsMatrix(
        scrobblesDF, artists,
        windowRange=(1, 2), timeThreshold=timedelta(minutes=30), 
        verbose=False
    ):
    tMat = np.zeros((len(artists), len(artists)), dtype=np.double)
    for w in range(windowRange[0], windowRange[1]+1):
        tmpMat = calcTransitionsMatrix(
            tMat, scrobblesDF, artists,
            window=w, timeThreshold=timeThreshold, verbose=verbose
        )
        tMat = tMat + (tmpMat/w)
    return tMat

def normalizeMatrix(matrix):
    pMat = matrix.copy()
    row_sums = pMat.sum(axis=1)
    pMat = pMat/row_sums[:, np.newaxis]
    return pMat