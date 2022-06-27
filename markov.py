###############################################################################
# Auxiliary
#   Non-specific functions needed by routines
###############################################################################
import numpy as np
from collections import Counter
from quantecon import MarkovChain

def getSongCounts(dataFull, topArtists):
    artsSongDict = {}
    for art in topArtists:
        songPlays = list(dataFull[dataFull['Artist']==art]['Song'])
        songCounts = Counter(songPlays)
        counts = np.array(list(songCounts.values()))
        countsNormalized = counts/sum(counts)
        itr = zip(list(songCounts.keys()), countsNormalized)
        countsDict = {s:n for (s, n) in itr}
        artsSongDict[art] = countsDict
    return artsSongDict

def generateMarkovPlaylist(
        markovChain, songsNumber, songsDictionary, initArtist,
        noRepetition=True
    ):
    sChain = markovChain.simulate(ts_length=songsNumber, init=initArtist)
    # Generate a random playlist ----------------------------------------------
    playlist = []
    ca = sChain[0]
    for ca in sChain:
        (songs, probs) = (
            list(songsDictionary[ca].keys()), 
            list(songsDictionary[ca].values())
        )
        if len(songs) > 0:
            six = np.random.choice(len(probs), 1, p=probs)[0]
            playlist.append((ca, songs[six]))
            # Remove from the pool for no repetitions -------------------------
            if noRepetition:
                songs.pop(six); probs.pop(six)
                normProbs = np.asarray(probs)/sum(probs)
                songsDictionary[ca]= {s:p for (s, p) in zip(songs, normProbs)}
    return playlist