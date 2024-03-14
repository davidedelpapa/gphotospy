import os
import pickle
import logging
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request


service_name = "photoslibrary"
version = "v1"
token_file = f'{service_name}_{version}.token'
scopes_arr = [
    'https://www.googleapis.com/auth/photoslibrary',
    'https://www.googleapis.com/auth/photoslibrary.sharing'
]


def get_credentials(secrets, open_browser=True):
    credentials = None
    secrets_dir = os.path.dirname(os.path.abspath(secrets))
    token_path = os.path.join(secrets_dir, token_file)

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            app_flow = InstalledAppFlow.from_client_secrets_file(
                secrets, scopes_arr)
            credentials = app_flow.run_local_server(open_browser=open_browser)

        with open(token_path, 'wb') as token:
            pickle.dump(credentials, token)
    return credentials


def init(secrets, open_browser=True):
    """
    Initializes the service, requesting the authorization from the browser.

    Parameters
    ----------
    secrets: str
        JSON file containing the secrets for OAuth,
        as created in the Google Cloud Console

    Returns
    -------
    A service object to pass to the Media, Album, or SharedAlbum contructors
    """
    credentials = get_credentials(secrets, open_browser)
    service_object = {
        "secrets": secrets
    }
    try:
        service = build(service_name, version,  static_discovery=False, credentials=credentials)
        logging.debug('service created successfully: {}'.format(service_name))
        service_object["service"] = service
        return service_object
    except Exception as e:
        logging.error(e)
    return None
