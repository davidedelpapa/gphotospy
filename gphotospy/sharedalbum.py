class SharedAlbum:
    """
    Shared album manager

    Examples
    --------
    Example init of the media manager:

    Imports

    >>> from gphotospy import authorize
    >>> from gphotospy.sharedalbum import SharedAlbum

    Select Secrets file

    >>> CLIENT_SECRET_FILE = "gphoto_oauth.json"

    Get authorization and return a service object

    >>> service = authorize.init(CLIENT_SECRET_FILE)

    Init the media manager

    >>> sharing_manager = SharedAlbum(service)
    """
    _PAGESIZE = 50
    _SHOW_ONLY_CREATED = False

    def __init__(self, service):
        """
        Constructor. It takes the service created with authorize.init()

        Parameters
        ----------
        service: service
            Service created with authorize.init()

        Examples
        --------
        Example init of the media manager:

        Imports

        >>> from gphotospy import authorize
        >>> from gphotospy.sharedalbum import SharedAlbum

        Select Secrets file

        >>> CLIENT_SECRET_FILE = "gphoto_oauth.json"

        Get authorization and return a service object

        >>> service = authorize.init(CLIENT_SECRET_FILE)

        Init the media manager

        >>> sharing_manager = SharedAlbum(service)
        """
        self._service = service["service"]

    # UTILITIES
    def set_pagination(self, n: int):
        """ Undocumented: see list() """
        # There's really no need to change this,
        #  since the "list" is an iterator that takes care of pagination
        #  behind the scenes
        if n > 50:
            n = 50
        if n < 1:
            n = 1
        self._PAGESIZE = n

    def show_only_created(self, val: bool):
        """
        Sets the list method to show only albums created by the API or not

        Parameters
        ----------
        val: bool
            value to be set (default is False)

        Examples
        --------
        >>> sharing_manager.show_only_created(False)
        """
        self._SHOW_ONLY_CREATED = val

    # API ENDPOINTS
    def get(self, token: str):
        """
        Returns the album info corresponding to the specified Share token

        Parameters
        ----------
        token: str
            Share token of the shared album to get

        Returns
        -------
        json object:
            Album information
        Examples
        --------
        >>> sharing_manager.get(token)
        {'id': '...', 'title': 'test shared album', 'productUrl': 'https://photos.google.com/lr/album/...', 'isWriteable': True, 'shareInfo': {'sharedAlbumOptions': {'isCommentable': True}, 'shareableUrl': 'https://photos.app.goo.gl/...', 'shareToken': '...', 'isJoined': True, 'isOwned': True}}
        """
        return self._service.sharedAlbums().get(shareToken=token).execute()

    def join(self, token: str):
        """
        Joins the album specified by the Share token on behalf of the user

        Parameters
        ----------
        token: str
            Share token of the shared album to join

        Returns
        -------
        json object:
            Joined album information

        Examples
        --------
        >>> sharing_manager.join(token)
        """
        request_body = {
            "shareToken": token
        }
        return self._service.sharedAlbums().join(body=request_body).execute()

    def leave(self, token: str):
        """
        Leaves the album specified by the Share token on behalf of the user

        Parameters
        ----------
        token: str
            Share token of the joined shared album to leave

        Examples
        --------
        >>> sharing_manager.leave(token)
        """
        request_body = {
            "shareToken": token
        }
        return self._service.sharedAlbums().leave(body=request_body).execute()

    def list(self, show_only_created=_SHOW_ONLY_CREATED):
        """
        Iterator over the albums present in the Sharing tab

        Parameters
        ----------
        show_only_created: bool, optional
            Set if it has to list only albums created via the API
            (default is set by show_only_created(), whose default is FALSE)

        yields
        ------
        iterator:
            iteratore over the list of albums

        Notes
        -----
        Google Photo API list request returns in reality an object containing
        a paginated list of albums.

        This function transforms the list in an iterator
        and takes care of pagination behind the scenes.

        Since there is a maximum limit on API requests per day per project
        it does not seem well to ask for less than the maximum pagination
        possible.

        However, if there are concerns of bandwith or speed,
        the pagination can be set by album.set_pagination(n)
        with 1 < n < 50, since at least 1 album must be sought
        and 50 is the API maximum.  20 is API default.

        Examples
        --------
        Get iterator

        >>> album_iterator = sharing_manager.list()

        Print first item

        >>> print(next(album_iterator))
        {'id': '...', 'title': 'Test sharing album', 'productUrl': 'https://photos.google.com/lr/album/...', 'mediaItemsCount': '0', 'coverPhotoBaseUrl': 'https://lh3.googleusercontent.com/lr/...', 'coverPhotoMediaItemId': '...'}
        """
        page_token = ""
        while page_token is not None:
            result = self._service.sharedAlbums().list(
                pageSize=self._PAGESIZE,
                excludeNonAppCreatedData=show_only_created,
                pageToken=page_token
            ).execute()
            page_token = result.get("nextPageToken", None)
            curr_list = result.get("sharedAlbums")
            for album in curr_list:
                yield album
