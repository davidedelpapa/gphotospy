import os
from tkinter import filedialog
from tkinter import *
from gphotospy import authorize
from gphotospy.media import Media
from gphotospy.album import Album

# Select secrets file
CLIENT_SECRET_FILE = "gphoto_oauth.json"

# Get authorization and return a service object
service = authorize.init(CLIENT_SECRET_FILE)

# Init the album and media manager
album_manager = Album(service)
media_manager = Media(service)

# FIle dialog to select media to upload
root = Tk()
curr_dir = os.getcwd()
filetypes = [("JPEG files", "*.jpg *.jpeg"),
             ("PNG files", "*.png"),
             ("BMP files", "*.bmp"),
             ("GIF files", "*.gif"),
             ("HEIC files", "*.heic"),
             ("ICO files", "*.ico"),
             ("TIFF files", "*.tiff *.tif"),
             ("WEBP files", "*.webp"),
             ("3GP files", "*.3gp"),
             ("3G2 files", "*.3g2"),
             ("ASF files", "*.asf"),
             ("AVI files", "*.avi"),
             ("DIVX files", "*.dvx"),
             ("M2T files", "*.m2t"),
             ("M2TS files", "*.m2ts"),
             ("M4V files", "*.m4v"),
             ("MMV files", "*.mmv"),
             ("MOD files", "*.mod"),
             ("MOV files", "*.mov"),
             ("MP4 files", "*.mp4"),
             ("MPG files", "*.mpg *.mpeg"),
             ("MTS files", "*.mts"),
             ("TOD files", "*.tod"),
             ("WMV files", "*.wmv"),
             ("all files", "*.*")]
root.filename = filedialog.askopenfilenames(
    initialdir=curr_dir, title="Select media file(s)", filetypes=filetypes)

# staging the media files (no description in this case)
for f in root.filename:
    media_manager.stage_media(f)

# actually put the uploaded media in a album
# (otherwise they can't be seen in Google Photos)
media_manager.batchCreate()

# batchCreate() when no name is given, uploads all media by default
# to a album named with the current date and time
# They are at this point also available ouside this album

# Some more album management #####

# create an album to add images to
created_album = album_manager.create('test album')
id_album = created_album.get("id")

# Show only media created though the API
media_manager.show_only_created(True)

# Now list will show first recently created media,
# and only those created with the API
list_iterator = media_manager.list()

items = []
added_images = len(root.filename)  # Recently added media number

for _ in range(added_images):
    media_item = next(list_iterator)
    items.append(media_item.get("id"))

# Batch add images
album_manager.batchAddMediaItems(id_album, items)


# Batch remove at least 2 of the media added to the album
if added_images > 2:
    list_iterator = media_manager.search_album(id_album)
    items = []
    for _ in range(added_images - 2):
        media_item = next(list_iterator)
        items.append(media_item.get("id"))

    album_manager.batchRemoveMediaItems(id_album, items)
