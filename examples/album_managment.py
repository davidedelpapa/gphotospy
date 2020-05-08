from gphotospy import authorize
from gphotospy.album import Album
from googleapiclient.errors import HttpError

# Select secrets file
CLIENT_SECRET_FILE = "gphoto_oauth.json"

# Get authorization and return a service object
service = authorize.init(CLIENT_SECRET_FILE)

# Init the album manager
album_manager = Album(service)

# Set default behaviors
album_manager.set_collaborative_share(False)
album_manager.set_commentable_share(True)

# Get iterator over the list of albums
print("Getting a list of albums...")
album_iterator = album_manager.list()

# Loop first 3 elements
for _ in range(3):
    try:
        # Print only album's title (if present, otherwise None)
        print(next(album_iterator).get("title"))
    except (StopIteration, TypeError) as e:
        # Handle exception if there are no albums left
        print("No (more) albums.")
        break

# get next album's id
album_id = next(album_iterator).get("id")

# get album's info based on id
print("Getting album's title...")
print(album_manager.get(album_id).get('title'))

id_album = None
# Create new album and get its Id if no error
print("Let's create a new album!")
try:
    new_album = album_manager.create('test album')
except HttpError as e:
    print("Failed to create new album.\n{}".format(e))
else:
    id_album = new_album.get("id")

if id_album is not None:
    # Share the album
    print("Sharing it...")
    try:
        album_manager.share(id_album)
    except HttpError as e:
        print("Failed to share.\n{}".format(e))

    # Unshare the album
    print("Unsharing it...")
    try:
        album_manager.unshare(id_album)
    except HttpError as e:
        print("Failed to unshare.\n{}".format(e))

    # Add enrichments

    # Add Text enrichment and get its id
    print("We add text to the new album")
    try:
        txt = album_manager.add_text(id_album, 'Test Text Enrichment')
    except HttpError as e:
        print("Could not create text enrichment")
    else:
        txt_id = txt.get("id")

    # Add Location enrichment
    from gphotospy.album import set_position, geolocate, POSITION

    # Get Rome's location and last position in the album
    Rome = geolocate("Rome", 41.9028, 12.4964)
    last_pos = set_position(POSITION.LAST)
    # Add as location enrichment
    print("We add a location to the new album...")
    try:
        album_manager.add_location(id_album, Rome, last_pos)
    except HttpError as e:
        print("Could not create location enrichment.\n{}".format(e))

    # Add Map enrichment
    after_text = set_position(POSITION.AFTER_ENRICHMENT, txt_id)
    Pescara = geolocate("Nice city", 42.5102, 14.1437)
    print("...end even a map!")
    try:
        album_manager.add_map(id_album, Pescara, Rome, after_text)
    except HttpError as e:
        print("Could not create map enrichment.\n{}".format(e))

print("Go check out your account what we did")
