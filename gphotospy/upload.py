import os
import requests
import mimetypes
from .authorize import get_credentials

upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
mimetypes.init()


def upload(secrets, media_file):
    """
    Uploads files of media to Google Server, to put in Photos

    Parameters
    ----------
    secrets: str
        JSON file containing the secrets for OAuth,
        as created in the Google Cloud Consolle
    media_file: Path
        Path to the file to upload

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

    header['X-Goog-Upload-Content-Type'] = mimetypes.guess_type(media_file)[0]

    f = open(media_file, 'rb').read()

    response = requests.post(upload_url, data=f, headers=header)
    if response.ok:
        return response.content.decode('utf-8')
    return None
