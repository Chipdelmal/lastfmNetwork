# Last.fm Network Analysis


[lastfm-to-csv](https://benjaminbenben.com/lastfm-to-csv/)

## Setting Up Keys, Folders and Constants

### Keys

Create a [Musicbrainz API](https://musicbrainz.org/doc/MusicBrainz_API) account and application, then create a file named `KEYS.py` file with the contents:

```python
# KEYS.py
(MB_NM, MB_V, MB_URL) = (<MUSICBRAINZ_APP_NAME>, "0.1", <USER_HOMEPAGE>)
(MB_USR, MB_PSW) = (<USERNAME>, <PASSWORD>)
GEO_USR = 'test'
```

### Folders

These pipelines are easiest to use by creating the following structure 

```
./data
    - Place the original CSV containing Last.fm's data here
./cache
    - Networks and artists counts will be exported here
./img
    - Images and plots will be exported here
```

### Constants and Bans



## Cleaning the Dataset

To clean the original dataset from Last.fm, download artists' information from Musicbrainz, and amend the artists in Last.fm data with Musicbrainz tags; run:


```bash
./GenerateDatasets.sh 'chipmaligno' '.'
```

```bash
python Clean_Lastfm.py 'chipmaligno' './data'
python Download_Musicbrainz.py 'chipmaligno' './data'
python Filter_Dataframe.py 'chipmaligno' './data'
```


## Generating Matrices

```bash
./GenerateMatrices.sh 'chipmaligno' '.' 100 10
```

```bash
python Compute_Transitions.py 'chipmaligno' './data' './cache' 100 5
```