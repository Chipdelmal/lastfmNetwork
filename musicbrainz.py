###############################################################################
# Musicbrainz
#   Functions needed to scrape artists' data
###############################################################################
import csv
import sys
from os import path
import musicbrainzngs as mb
from termcolor import colored
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import KEYS
import auxiliary as aux
geolocator = Nominatim(user_agent=KEYS.GEO_USR)

def doGeocode(address):
    try:
        return geolocator.geocode(address)
    except (GeocoderTimedOut):
        return doGeocode(address)

def geocodeEntries(info, geoSize=6):
    # NEEDS IMPROVEMENT (info.get('area') with city)
    (tmp, p1, p2) = (info, info[1], info[2])
    if p1 is None:
        p1 = ''
    if p2 is None:
        p2 = ''
    location = doGeocode(p1 + ' ' + p2)
    if location is None:
        tmp.extend(geoSize*[None])
    else:
        tmp.extend([location.latitude, location.longitude])
        gcList = [i.strip() for i in location.address.split(',')]
        gcList.reverse()
        tmp.extend(aux.padList(gcList, geoSize))
    return tmp

def getArtistInfo(artist, topGenres=3):
    srch = mb.search_artists(artist=artist).get('artist-list')
    if len(srch) > 0:
        # Scrape best artist match
        arts = mb.search_artists(artist=artist).get('artist-list')
        names = [i['name'] for i in arts]
        ix = names.index(artist) if artist in names else -1
        info = arts[ix] if (ix>=0) else arts[0]
        # Get artist info (NEEDS IMPROVEMENT!!!!)
        (id, name, country, city, genre) = (
                info.get('id'), info.get('name'), info.get('country'),
                getArea(info), getTopGenres(info, topGenres=topGenres)
            )
        tmp = [name, country, city, id]
        tmp.extend(genre)
        return tmp
    else:
        tmp = [artist, None, None, None]
        tmp.extend(topGenres * [None])
        return tmp

def getTopGenres(info, topGenres=3):
    tags = info.get('tag-list')
    # Check that genres are available
    if tags is not None:
        lst = []
        for i in info.get('tag-list'):
            lst.append((int(i.get('count')), i.get('name')))
        lst.sort(reverse=True)
        # Check that there are enough tags and pad with None
        if (len(lst) >= topGenres):
            return [i[1] for i in lst[0:topGenres]]
        else:
            tmp = [i[1] for i in lst[0:len(lst)]]
            return aux.padList(tmp, topGenres)
    else:
        return [None] * topGenres

def getArea(info):
    area = info.get('begin-area')
    if area is not None:
        city = area.get('name')
        if city is not None:
            return city
    else:
        return None

def generateMBHeader(topGenres, geoSize):
    partA = ['Artist', 'MB_Geo1', 'MB_Geo2', 'MB_Hash']
    gnrPad = ['Gen_' + str(i) for i in range(1, topGenres + 1)]
    geoPad = ['Geo_' + str(i) for i in range(1, geoSize + 1)]
    partA.extend(gnrPad)
    partA.extend(['Lat', 'Lon'])
    partA.extend(geoPad)
    return partA

def parseFromMusicbrainz(
        clnData, dataPath, username,
        topGenres=3, geoSize=6, verbose=True
    ):
    artists = sorted(clnData['Artist'].unique())
    artNum = len(artists)
    # Generate output path
    FILE_PATH = path.join(dataPath, username)
    # print('Parsing from musicbranz!\n')
    with open(FILE_PATH + '_mbz.csv', mode='w') as mbFile:
        mbWriter = csv.writer(
            mbFile, quoting=csv.QUOTE_MINIMAL
        )
        header = generateMBHeader(topGenres, geoSize)
        print(header)
        mbWriter.writerow(header)
        with open(FILE_PATH + '_dbg.txt', 'w') as out:
            for (i, art) in enumerate(artists):
                # Parse musicbranz database
                info = getArtistInfo(art, topGenres=topGenres)
                try:
                    info = geocodeEntries(info)
                    mbWriter.writerow(info)
                    if verbose:
                        txt = '* {}/{}: {} [{} - {}]'.format(
                            str(i+1).zfill(3), str(artNum).zfill(3), 
                            art, info[0], info[1]
                        )
                        sys.stdout.write("\033[K") 
                        print(colored(txt, 'blue'), end='\r')
                    out.write(txt+'\n')
                except:
                    if verbose:
                        txt = f'* Error with {info}' 
                        sys.stdout.write("\033[K") 
                        print(colored(txt, 'red'), end='\n')
                    out.write(txt+'\n') 
        if verbose:
            sys.stdout.write("\033[K") 
            print("", end='\r')
                