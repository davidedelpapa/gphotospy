from gphotospy import authorize
from gphotospy.media import Media
from gphotospy.media import CONTENTFILTER, MEDIAFILTER, FEATUREFILTER
from gphotospy.media import date, date_range
from gphotospy.album import Album

# Select secrets file
CLIENT_SECRET_FILE = "gphoto_oauth.json"

# Get authorization and return a service object
service = authorize.init(CLIENT_SECRET_FILE)

# Init the media manager
media_manager = Media(service)

# Set default behaviors (don't show archived media)
media_manager.show_archived(False)

# Get iterator over the list of media
print("Getting a list of media...")
media_iterator = media_manager.list()

# Loop first 3 elements
for _ in range(3):
    try:
        # Print only media's filename (if present, otherwise None)
        print(next(media_iterator).get("filename"))
    except StopIteration:
        # Handle exception if there are no media left
        print("No (more) media.")
        break

# get next media's id
media_id = next(media_iterator).get("id")

# Using get() to get media's info based on id
print("Getting media's mimetype...")
print(media_manager.get(media_id).get('mimeType'))

# Search media
# Search using filters or the items inside an album

# Search by content
print("Searching 3 travel-related media")
search_iterator = my_media.search(filter=[CONTENTFILTER.TRAVEL])
try:
    for _ in range(3):
        print(next(search_iterator).get("filename"))
except e:
    print("No (more) travel-related media.")

# Search by media type
print("Searching any 3 videos")
search_iterator = media_manager.search(filter=[MEDIAFILTER.VIDEO])
try:
    for _ in range(3):
        print(next(search_iterator).get("filename"))
except e:
    print("No (more) video.")

# Search by featured
print("Searching for at least a featured media")
search_iterator = media_manager.search(filter=[FEATUREFILTER.FAVORITES])
try:
    print(next(search_iterator).get("filename"))
except e:
    print("No featured media.")

# Search by exact date
print("Searching 3 media for Christmas... whichever Christmas!")
Xmas = date(0, 12, 25)
search_iterator = media_manager.search(filter=[Xmas])
try:
    for _ in range(3):
        print(next(search_iterator).get("filename"))
except e:
    print("No (more) Xmas' media.")

# Search by range of dates
print("Searching 3 media after Christmas, before new year's eve... whichever year too")
StSteven = date(0, 12, 26)
new_year_eve = date(0, 12, 31)
my_range = date_range(
    start_date=StSteven,
    end_date=new_year_eve)
search_iterator = media_manager.search(filter=[my_range])
try:
    for _ in range(3):
        print(next(search_iterator).get("filename"))
except e:
    print("No (more) media in the range.")

# Combining search filters
# Remeber: combining filters work as 'OR', not as 'AND'!

print("Let's do a detailed search")

search_iterator = my_media.search(filter=[
    FEATUREFILTER.NONE,  # This is default, didn't need be specified
    CONTENTFILTER.TRAVEL,
    CONTENTFILTER.SELFIES,
    MEDIAFILTER.ALL_MEDIA,  # This too is default...
    media.date(2020, 4, 24),
    media.date_range(
        start_date=media.date(2020, 4, 19),
        end_date=media.date(2020, 4, 21)
    )
])
try:
    print(next(search_iterator))
except e:
    print("No media found :-(")

# Search for media in album
print("Search media in album")
# get an album's id
album_manager = Album(service)
album_iterator = album_manager.list()
album = next(album_iterator)
album_id = album.get("id")
album_title = album.get("title")
print("Album title: {}".format(album_title))
# search in album
search_iterator = media_manager.search_album(album_id)
try:
    for _ in range(3):
        print(next(search_iterator).get("filename"))
except e:
    print("No (more) media in album {}.".format(album_title))
