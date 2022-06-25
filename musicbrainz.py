
import KEYS
import musicbrainzngs as mb
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
geolocator = Nominatim(user_agent=KEYS.GEO_USR)


def doGeocode(address):
    try:
        return geolocator.geocode(address)
    except (GeocoderTimedOut):
        return doGeocode(address)

def geocodeEntries(info, geo_size=6):
    (tmp, p1, p2) = (info, info[1], info[2])
    if p1 is None:
        p1 = ''
    if p2 is None:
        p2 = ''
    location = doGeocode(p1 + ' ' + p2)
    if location is None:
        tmp.extend(geo_size*[None])
    else:
        tmp.extend([location.latitude, location.longitude])
        gcList = [i.strip() for i in location.address.split(',')]
        gcList.reverse()
        tmp.extend(padList(gcList, geo_size))
    return tmp

def getArtistInfo(artist, topGenres=3):
    srch = mb.search_artists(artist=artist).get('artist-list')
    if len(srch) > 0:
        info = mb.search_artists(artist=artist).get('artist-list')[0]
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

def padList(lst, n):
    lst.extend([None] * n)
    lst = lst[:n]
    return lst

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
            return padList(tmp, topGenres)
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
