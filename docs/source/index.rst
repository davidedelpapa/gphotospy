.. gphotospy documentation master file, created by
   sphinx-quickstart on Tue May  5 16:54:58 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to gphotospy's documentation!
=====================================

Interact with Gooogle Photos in Python


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



Installation
------------

You can use Pypi distribution (recommended method)::

   pip install gphotospy

Otherwise clone this repo and use the modules in _gphotospy_ directly (not recommended).

Usage
-----

This library is unofficial; most of the API is covered, however no proper test coverage has been implemented so far.

Please refer to `Google's authorization guide <https://developers.google.com/photos/library/guides/get-started#configure-app>`_ (recommended),
or see the below "Set up authorization" for a quick review on how to get Google's API keys and authorization (save it in a `gphoto_oauth.json` file).

Quickstart::

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

Check the *examples* folder of `gphotospy repo <https://github.com/davidedelpapa/gphotospy>`_ for more examples of use.

Always refer to:

:ref:`modindex`

