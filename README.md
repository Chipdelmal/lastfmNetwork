# Last.fm Network Analysis


Download your [Last.fm](https://www.last.fm/home) history through [lastfm-to-csv](https://benjaminbenben.com/lastfm-to-csv/) and place it in the `/data` folder.

<hr>

## Setting Things Up

### Keys

Create a [Musicbrainz API](https://musicbrainz.org/doc/MusicBrainz_API) account and application, then **create** a file named `KEYS.py` file with the contents:

```python
###############################################################################
# KEYS.py
###############################################################################
(MB_NM, MB_V, MB_URL) = (<MUSICBRAINZ_APP_NAME>, "0.1", <USER_HOMEPAGE>)
(MB_USR, MB_PSW) = (<USERNAME>, <PASSWORD>)
GEO_USR = 'test'
```

### Bans

To help cleanup the original last.fm dataset, these scripts also require the **creation** of a `BANS.py` file with contents similar to the following:

```python
###############################################################################
# BANS.py
###############################################################################
# The following set of names will be excluded from parsing and analysis
#   (this happens before musicbrainz data)
BAN = set([
    'Nature Publishing Group', 'Douglas Adams',
    "The Skeptics' Guide to the Universe", 'chipdelmal'
])
# The following dictionary will replace the artists name on the sets with the
#   name defined by the entry key
SWP_PRE = {
    'Courteeners': {'The Courteeners', 'Courteeners'},
    'Belle & Sebastian': {'Belle & Sebastian', 'Belle Sebastian'},
    'The Smashing Pumpkins': {'Smashing Pumpkins'},
}
```

### Folders

These pipelines are easiest to use by following the folder structure: 

```
./data
    - Place the original CSV containing Last.fm's data here
./cache
    - Networks and artists counts will be exported here
./img
    - Images and plots will be exported here
```

<hr>

## Use

### 1. Cleaning the Dataset

To clean the original dataset from Last.fm, download artists' information from Musicbrainz, and amend the artists in Last.fm data with Musicbrainz tags; run:


```bash
./GenerateDatasets.sh 'chipmaligno' '.'
```

Which launches the following scripts in order:

```bash
python Clean_Lastfm.py 'chipmaligno' './data'
python Download_Musicbrainz.py 'chipmaligno' './data'
python Fix_Dataframe.py 'chipmaligno' './data'
```


### 2. Generating Matrices

Generating the transitions matrices can be done with the following command:

```bash
./GenerateMatrices.sh 'chipmaligno' '.' 100 5
```

Which launches the following script ranging from 1 to 5 in the window size:

```bash
python Compute_Transitions.py 'chipmaligno' './data' './cache' 100 1
...
python Compute_Transitions.py 'chipmaligno' './data' './cache' 100 5
```

<hr>

## Files' Description


### Main Routines

* `Clean_Lastfm.py`: Takes the raw last.fm data from the csv, removes duplicates, removes banned artists, and converts into a timezone
* `Download_Musicbrainz.py`: Downloads artists' data from musibrainz into a CSV file.
* `Fix_Dataframe.py`: Filters a dataframe between dates, checks for inflated counts, and amends artists names to match musicbrainz tags.
* `Compute_Transitions.py`: Calculates transitions matrix (both in frequency and probability) for top N artists through a weighted window. Please have a look at my [blogpost](https://chipdelmal.github.io/dataViz/2022-06-17-LastfmNetwork.html).
* `Plot_Chord.py`: Exports a chord diagram with a given number of artists and a window range (as exported by `Compute_Transitions.py`).
* `Markov_Playlist.py`: Generates a playlist purely based on a Markov random walker process based on the artists probability matrix and song frequencies.

### Functions Files

* `auxiliary.py`: Non-specific functions needed by routines.
* `musicbrainz.py`: Functions needed to scrape artists' data.
* `network.py`: Functions needed to do network and transitions matrices transformations.

### Constants

* `CONSTANTS.py`: General constants common for all the scripts.
* `BANS.py`: Dictionaries and sets that contain bans and fixes for artists' names.
* `KEYS.py`: Musicbrainz app keys and login information.
