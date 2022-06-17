import os
import requests
import mimetypes
from .authorize import get_credentials

upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
mimetypes.init()


def upload(secrets, media_file, mime_type=None):
    """
    Uploads files of media to Google Server, to put in Photos

    Parameters
    ----------
    secrets: str
        JSON file containing the secrets for OAuth,
        as created in the Google Cloud Consolle
    media_file: Path, file-like object, or requests iterator
        Path to the file to upload
        File-like object opened in binary mode to upload
        Python requests iterator for chunked encoded requests

    Returns
    -------
    Upload Token if successfull, otherwise None
    """
    credentials = get_credentials(secrets)

    header = {
        'Authorization': "Bearer " + credentials.token,
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-Protocol': 'raw'
    }

    if mime_type is None:
        mime_type =  mimetypes.guess_type(media_file)[0]
    header['X-Goog-Upload-Content-Type'] = mime_type
    is_file_like = False
    try: # maintain potential python2 compat
        is_file_like = not isinstance(media_file, str)
    except:
        pass
    
    f = media_file
    if not is_file_like:
        f = open(media_file, 'rb')

    response = requests.post(upload_url, data=f, headers=header)
    if response.ok:
        return response.content.decode('utf-8')
    return None
