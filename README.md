# Last.fm Network Analysis


## Setting Up Folders and Constants

## Cleaning the Dataset

To clean the original dataset from Last.fm, download artists' information from Musicbrainz, and amend the artists in Last.fm data with Musicbrainz tags; run:


```bash
./GenerateDatasets.sh 'chipmaligno' '.'
```

```bash
python Clean_Lastfm.py 'chipmaligno' './data'
python Download_misucbrainz.py 'chipmaligno' './data'
python Filter_Dataframe.py 'chipmaligno' './data'
```


## Generating Matrices

```bash
./GenerateMatrices.sh 'chipmaligno' '.' 100 10
```

```bash
python Compute_Transitions.py 'chipmaligno' './data' './cache' 100 5
```