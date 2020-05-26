# gPhotoSpy

Interact with Google Photos in Python

[![PyPI version](https://badge.fury.io/py/gphotospy.svg)](https://badge.fury.io/py/gphotospy) [![Documentation Status](https://readthedocs.org/projects/gphotospy/badge/?version=latest)](https://gphotospy.readthedocs.io/en/latest/?badge=latest) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

You can use Pypi distribution (recommended method):

```bash
pip install gphotospy
```

Otherwise clone this repo and use the modules in _gphotospy_ directly (not recommended).

## Usage examples

This library is unofficial; most of the API is covered, however no proper test coverage has been implemented so far.

Please refer to [Google's authorization guide](https://developers.google.com/photos/library/guides/get-started#configure-app) (recommended), or see the below "Set up authorization" for a quick review on how to get Google's API keys and authorization (save it in a `gphoto_oauth.json` file).

```python
from gphotospy import authorize
from gphotospy.album import Album

# Select secrets file (got through Google's API console)
CLIENT_SECRET_FILE = "gphoto_oauth.json"

# Get authorization and return a service object
service = authorize.init(CLIENT_SECRET_FILE)

# Init the album manager
album_manager = Album(service)

# Create a new album
new_album = album_manager.create('test album')

# Get the album id and share it
id_album = new_album.get("id")
album_manager.share(id_album)
```

### Examples

Check the _examples_ folder for more examples of use.

### Tutorials

Check the [wiki](https://github.com/davidedelpapa/gphotospy/wiki) for tutorials

## API Coverage

- [x] OAuth authorization
- [ ] Google server upload
  - [x] Simple uploader
  - [ ] Resumable uploader
- [x] Albums
  - [x] addEnrichment
  - [x] batchAddMediaItems
  - [x] batchRemoveMediaItems
  - [x] create
  - [x] get
  - [x] list
  - [x] share
  - [x] unshare
- [ ] MediaItems
  - [x] batchCreate
  - [ ] batchGet
  - [x] get
  - [x] list
  - [x] search
- [x] SharedAlbums
  - [x] get
  - [x] join
  - [x] leave
  - [x] list

## Test Coverage

Not yet implemented. The tests have been done "live" on my account. I'm planning to set up mock tests for this suite, just for regression purposes.

## Documentation

- [x] Docstrings
- [x] Examples
- [-] Tutorials (See the wiki)
- [x] API docs (must be improved though)

## Near future plans

These are the next steps:

- [ ] Finish Documentation
- [ ] Mock tests
- [ ] Resumable Uploads
- [ ] Objects representations
  - [x] Media
  - [ ] Album
  - ...

Accepting ideas, so don't be shy and put them forth!

## Set up authorization

Browse through [Google's authorization guide](https://developers.google.com/photos/library/guides/get-started#configure-app)

Quick recap:

Go to [Google Cloud Console](https://console.cloud.google.com).
Set up a new project, then on the menu select: `Api & Services` > `Library`.
In the library, search for "photos", select `Photo Library API` and click on the `ENABLE` button.
On the `API & Services, Photo Library API` select `Credentials`, and select the `+CREDENTIALS` and select in the dropdown `OAuth client ID`. Select the type of app to be created (for desktop application select "other") and give it a name. If you are an occasional user, you should before this thing select the authorization display (`OAuth Consent Screen`), and make it public (if you are not a g-Suite user \$\$\$. THe interface prompts you already to do so, if never done before).
After this, coming back to the main interface, select in the row of the OAuth 2.0 Client ID just created the download button (rightmost one). Download the `.json` file in the root of the project, and give it a meaningful name (because it must be used afterwards). Remember to keep all these secret files far from git pushes, so if you are committing your porject to a repository, add the downloaded file to the _.gitignore_.

Once run the authentication it should open a browser to authenticate.
If you are creating a project for non commercial use you need not apply for review, but you have to allow it, because Google show a big message of warining. Clicking on advanced, it shows the button to allow the authorization, even though the app is not reviewed by Google (useful for tests and personal use projects). A .token file will keep the authorization for further use

## Contributing

Please give me some heads up if you are working on an interesting feature to add to _gphotospy_ before a PR (well, even afterwards it's ok).

1. Fork it (<https://github.com/davidedelpapa/gphotospy/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## License

MIT, see the _LICENSE_ file.

## Changelog

- V. 0.1.2: Added media item object representation
- V. 0.1.1: Added documentation
- V. 0.1.0: Fisrt usable version

## About me

Too shy to talk about it (not true). This project though has been a relief during COVID lockdown.
