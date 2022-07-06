import KEYS
import musicbrainzngs as mb
import musicbrainz as mbz
import CONSTANTS as cst

##############################################################################
# Logging In
##############################################################################
mb.auth(KEYS.MB_USR, KEYS.MB_PSW)
mb.set_useragent(KEYS.MB_NM, KEYS.MB_V, KEYS.MB_URL)
##############################################################################
# Geocoding
##############################################################################
artist = 'Radiohead'
# info = mbz.getArtistInfo(artist)

arts = mb.search_artists(artist=artist).get('artist-list')
names = [i['name'] for i in arts]
ix = names.index(artist) if artist in names else -1
info = arts[ix] if (ix>=0) else arts[0]
info.get('country')



from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent=KEYS.GEO_USR)

mbz.getArtistInfo("Radiohead")

##############################################################################
# Data Parsing
##############################################################################
topGenres = 3

artist = 'Radiohead'
srch = mb.search_artists(artist=artist).get('artist-list')
# if srch:
# Get the best match for the artist --------------------------------------
names = [i['name'] for i in srch]
ix = names.index(artist) if artist in names else -1
info = srch[ix] if (ix>=0) else srch[0]
# Get info on result -----------------------------------------------------
(artID, artName) = (info.get('id'), info.get('name'))
genres = mbz.getTopGenres(info, topGenres=topGenres)
# Get area and country ---------------------------------------------------
if info.get('begin-area'):
    area = info.get('begin-area').get('name')
elif info.get('area'):
    area = info.get('area').get('name')
if info.get('country'):
    area = '{}, {}'.format(area, info.get('country'))
# Geocode area -----------------------------------------------------------
locations = geolocator.geocode(
    area, 
    addressdetails=True, exactly_one=False,
    namedetails=True, language="english", 
)
# Get most likely according to priority list -----------------------------
for loc in locations:
    ctry = loc.raw['address']['country_code'].upper()
    for c in cst.COUNTRY_PRIORITY:
        if ctry == c:
            break
(country, state) = (
    loc.raw['address']['country_code'].upper(), 
    loc.raw['address']['state']
)
