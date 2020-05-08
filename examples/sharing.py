from gphotospy import authorize
from gphotospy.sharedalbum import SharedAlbum
from gphotospy.album import Album
from googleapiclient.errors import HttpError

# Select secrets file
CLIENT_SECRET_FILE = "gphoto_oauth.json"

# Get authorization and return a service object
service = authorize.init(CLIENT_SECRET_FILE)

# Init the media manager
sharing_manager = SharedAlbum(service)

# Set default behaviors
sharing_manager.show_only_created(False)

# Get iterator over the list of shared albums
print("Getting a list of shared albums...")
album_iterator = sharing_manager.list()

# Loop first 3 elements
for _ in range(3):
    try:
        # Print only albums's title (if present, otherwise None)
        print(next(album_iterator).get("title"))
    except (StopIteration, TypeError) as e:
        # Handle exception if there are no media left
        print("No (more) shared albums.")
        break

# Create a test album and share it
# create and share
print("Create and share a new album")

album_manager = Album(service)
created_album = album_manager.create('test shared album')
id_album = created_album.get("id")
share_info = album_manager.share(id_album)
token = share_info.get('shareToken')

# Using get() for info retrieval on the shared album
print("Getting album's info")
print(sharing_manager.get(token))

# Trying to join the shared album
print("Trying to join it")
try:
    sharing_manager.join(token)
except HttpError as e:
    print("Can't join albums already joined\n{}".format(e))

# Trying to leave the shared album
print("Trying to leave it, then")
try:
    sharing_manager.leave(token)
except HttpError as e:
    print("Can't leave your own albums!\n{}".format(e))
