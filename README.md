# Last.fm Network Analysis

## Download Last.fm History

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

## 1. Cleaning the Dataset

To clean the original dataset from Last.fm, download artists' information from Musicbrainz, and amend the artists in Last.fm data with Musicbrainz tags; run:


```bash
./GenerateDatasets.sh 'chipmaligno' '.'
```

Which launches the following scripts in order:

```bash
python Clean_Lastfm.py 'chipmaligno' './data'
python Download_Musicbrainz.py 'chipmaligno' './data'
python Filter_Dataframe.py 'chipmaligno' './data'
```


## 2. Generating Matrices

```bash
./GenerateMatrices.sh 'chipmaligno' '.' 100 10
```

```bash
python Compute_Transitions.py 'chipmaligno' './data' './cache' 100 5
```