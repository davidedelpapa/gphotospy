
class POSITION:
    """
    Defines positions for enrichments inside an album.

    Used in the function set_position()

    Attributes
    ----------
    UNSPECIFIED:
        Position is unspecified. Default in API if not specified.
    FIRST:
        First position in the album
    LAST:
        Last position in the album
    AFTER_MEDIA:
        After the specified media (specify media id)
    AFTER_ENRICHMENT:
        After the specified enrichment (specify enrichment id)
    """
    UNSPECIFIED = 'POSITION_TYPE_UNSPECIFIED'
    FIRST = 'FIRST_IN_ALBUM'
    LAST = 'LAST_IN_ALBUM'
    AFTER_MEDIA = 'AFTER_MEDIA_ITEM'
    AFTER_ENRICHMENT = 'AFTER_ENRICHMENT_ITEM'


def set_position(position=POSITION.FIRST, id_item=None):
    """
    Contructs the position of Enrichment item inside the album

    Parameters
    ----------
    position: POSITION
        position in the album. Possible values are:
            * POSITION.UNSPECIFIED Left unspecified
            * POSITION.FIRST First inside the album
            * POSITION.LAST Last inside the album
            * POSITION.AFTER_MEDIA After the media
                specified by id_item
            * POSITION.AFTER_ENRICHMENT After another enrichment,
                specified by id_item
    Returns
    -------
    Item position

    Examples
    --------
    Set absolute position:

    >>> pos1 = set_position(POSITION.LAST)

    Set relative position; enrichment_id contains the id
    of the enrichment after which to position the element:

    >>> pos2 = set_position(POSITION.AFTER_ENRICHMENT, enrichment_id)
    """
    pos = {}
    if position == POSITION.AFTER_MEDIA:
        pos = {
            "position": position,
            "relativeMediaItemId": id_item
        }
    elif position == POSITION.AFTER_ENRICHMENT:
        pos = {
            "position": position,
            "relativeEnrichmentItemId": id_item
        }
    else:
        pos = {
            "position": position
        }
    return pos


def geolocate(name: str, lat: float, lon: float):
    """
    Returns a quasi-codified geopositioned element.

    Latitude and Longitude have to follow the WGS84 standard.
    The name of the position is not codified, so it is allowed to nikckname
    positions, such as "uncle Tobi's house",
    while keeping the geographic cordinates standard

    Parameters
    ----------
    name: str
        Any meaningful name to give to the position
    lat: float
        Latitude as following the WGS84 standard [range: -90.0, +90.0]
    lon: float
        Longitude as following the WGS84 standard [range: -90.0, +90.0]

    Returns
    -------
    A geographic point to use in Location or Map enrichments

    Examples
    --------
    >>> rome = geolocate("Rome", 41.9028, 12.4964)
    """
    return {
        "locationName": name,
        "latlng": {
            "latitude": lat,
            "longitude": lon
        }
    }


class Album:
    """
    Album manager

    Examples
    --------
    Example init of the album manager:

    Imports

    >>> from gphotospy import authorize
    >>> from gphotospy.album import Album

    Select Secrets file

    >>> CLIENT_SECRET_FILE = "gphoto_oauth.json"

    Get authorization and return a service object

    >>> service = authorize.init(CLIENT_SECRET_FILE)

    Init the album manager

    >>> album_manager = Album(service)
    """
    _PAGESIZE = 50
    _SHOW_ONLY_CREATED = False
    _COLLABORATIVE = False
    _COMMENTABLE = True

    def __init__(self, service):
        """
        Constructor. It takes the service created with authorize.init()

        Parameters
        ----------
        service: service
            Service created with authorize.init()

        Examples
        --------
        Example init of the album manager:

        Imports

        >>> from gphotospy import authorize
        >>> from gphotospy.album import Album

        Select Secrets file

        >>> CLIENT_SECRET_FILE = "gphoto_oauth.json"

        Get authorization and return a service object

        >>> service = authorize.init(CLIENT_SECRET_FILE)

        Init the album manager

        >>> album_manager = Album(service)
        """

        self._service = service["service"]
        self._secrets = service["secrets"]

    # UTILITIES
    def set_pagination(self, n: int):
        """ Undocumented: see list() for more info """

        # There's really no need to change this,
        #  since the "list" is an iterator that takes care of pagination
        #  behind the scenes

        if n > 50:
            n = 50
        if n < 1:
            n = 1
        self._PAGESIZE = n

    def set_collaborative_share(self, val: bool):
        """
        Sets the share method to allow collaborative by default or not

        Parameters
        ----------
        val: bool
            value to be set (default is False)

        Examples
        --------
        >>> album_manager.set_collaborative_share(False)
        """

        self._COLLABORATIVE = val

    def set_commentable_share(self, val: bool):
        """
        Sets the share method to allow commentable by default or not

        Parameters
        ----------
        val: bool
            value to be set (default is True)

        Examples
        --------
        >>> album_manager.set_commentable_share(True)
        """

        self._COMMENTABLE = val

    def show_only_created(self, val: bool):
        """
        Sets the list method to show only albums created by the API or not

        Parameters
        ----------
        val: bool
            value to be set (default is False)

        Examples
        --------
        >>> album_manager.show_only_created(False)
        """

        self._SHOW_ONLY_CREATED = val

    # API ENDPOINTS
    def add_enrichment(self, album_id: str, enrichement_type, position):
        """ Generic. Use the specified versions """
        # To be used by the other enrichemnts methods
        request_body = {
            "newEnrichmentItem": enrichement_type,
            "albumPosition": position
        }
        return self._service.albums().addEnrichment(
            albumId=album_id,
            body=request_body).execute()

    def add_location(
            self,
            album_id: str,
            location,
            position=None):
        """
        Add a location enrichment to the album, at the given position

        Parameters
        ----------
        album_id: str
            Id of the album to add text to
        location: Location object
            Location object, as returned from geolocate() function
        position: Position object
            Position object where to add the location.
            Contruct it with the set_position() function

        Examples
        --------
        Imports:

        >>> from gphotospy.album import set_position, geolocate, POSITION

        Location and position inside the album

        >>> Rome = geolocate("Rome", 41.9028, 12.4964)
        >>> last_pos = set_position(POSITION.LAST)

        Create enrichemnt

        >>> album_manager.add_location(id_album, Rome, last_pos)
        {'id': '...'}
        """
        if position is None:
            position = set_position()
        enrichement_type = {
            "locationEnrichment": {
                "location": location
            }
        }
        result = self.add_enrichment(album_id, enrichement_type, position)
        return result.get("enrichmentItem")

    def add_map(
            self,
            album_id: str,
            origin_loc,
            destination_loc,
            position=None):
        """
        Add a map enrichment to the album, at the given position

        Parameters
        ----------
        album_id: str
            Id of the album to add text to
        origin_loc: Location object
            Location of MAP origin, as returned from geolocate() function
        destination_loc: Location object
            Location of MAP origin, as returned from geolocate() function
        position: Position object
            Position object where to add the location.
            Contruct it with the set_position() function

        Examples
        --------
        Imports:

        >>> from gphotospy.album import set_position, geolocate, POSITION

        Add two locations and a position inside the album

        >>> Rome = geolocate("Rome", 41.9028, 12.4964)
        >>> Pescara = geolocate("Nice city", 42.5102, 14.1437)
        >>> first_pos = set_position(POSITION.FIRST)

        Create enrichemnt

        >>> album_manager.add_map(id_album, Pescara, Rome, first_pos)
        {'id': '...'}
        """
        if position is None:
            position = set_position()
        enrichement_type = {
            "mapEnrichment": {
                "origin": origin_loc,
                "destination": destination_loc
            }
        }
        result = self.add_enrichment(album_id, enrichement_type, position)
        return result.get("enrichmentItem")

    def add_text(
            self,
            album_id: str,
            text: str,
            position=None):
        """
        Add a text enrichment to the album, at the given position

        Parameters
        ----------
        album_id: str
            Id of the album to add text to
        text: str
            Text to be added as enrichment
        position: Position object
            Position object where to add the text.
            Contruct it with the set_position() function

        Examples
        --------
        Add text enrichment

        >>> album_manager.add_text(id_album, 'Test Text Enrichment')
        {'id': '...'}
        """
        if position is None:
            position = set_position()
        enrichement_type = {
            "textEnrichment": {
                "text": text
            }
        }
        result = self.add_enrichment(album_id, enrichement_type, position)
        return result.get("enrichmentItem")

    def batchAddMediaItems(self, album_id: str, items):
        """
        Add a list of media items to the given album

        The media items and the album must have been created
        by the developer via the API.

        Parameters
        ----------
        album_id: str
            Id of the album to add the items to
        items: [str]
            list of Ids of items to add to the album

        Returns
        -------
        Empty object if successfull
        """
        request_body = {
            "mediaItemIds": items
        }
        return self._service.albums().batchAddMediaItems(
            albumId=album_id,
            body=request_body).execute()

    def batchRemoveMediaItems(self, album_id: str, items):
        """
        Removes a list of media items to the given album

        The media items and the album must have been created
        by the developer via the API.

        Parameters
        ----------
        album_id: str
            Id of the album to add the items to
        items: [str]
            list of Ids of items to add to the album

        Returns
        -------
        Empty object if successfull
        """
        request_body = {
            "mediaItemIds": items
        }
        return self._service.albums().batchRemoveMediaItems(
            albumId=album_id,
            body=request_body).execute()

    def create(self, title: str):
        """
        Creates an empty album with the given title

        Parameters
        ----------
        title: str
            Title of the album to create

        Returns
        -------
        json object:
            Album information

        Examples
        --------
        Create new album

        >>> album_manager.create('test album')
        {'id': '...', 'title': 'test album', 'productUrl': 'https://photos.google.com/lr/album/...', 'isWriteable': True}
        """
        request_body = {
            "album": {'title': title}
        }
        return self._service.albums().create(body=request_body).execute()

    def get(self, id: str):
        """
        Returns the album info corresponding to the specified id

        Parameters
        ----------
        id: str
            Id of the album to get

        Returns
        -------
        json object:
            Album information

        Examples
        --------
        Get an iterator:

        >>> album_iterator = album_manager.list()

        Get next album's id

        >>> album_id = next(album_iterator).get("id")

        Get album's info based on id

        >>> album_manager.get(album_id)
        """
        return self._service.albums().get(albumId=id).execute()

    def list(self, show_only_created=_SHOW_ONLY_CREATED):
        """
        Iterator over the albums present in the Google Photos account

        Parameters
        ----------
        show_only_created: bool, optional
            Set if it has to list only albums created via the API
            (default is set by show_only_created(), whose default is FALSE)

        Yields
        -------
        An iterator over the list of albums

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
        Get an iterator:

        >>> album_iterator = album_manager.list()

        Print first item:

        >>> print(next(album_iterator))
        """
        page_token = ""
        while page_token is not None:
            result = self._service.albums().list(
                pageSize=self._PAGESIZE,
                excludeNonAppCreatedData=show_only_created,
                pageToken=page_token
            ).execute()
            page_token = result.get("nextPageToken", None)
            curr_list = result.get("albums")
            for album in curr_list:
                yield album

    def share(
            self,
            id: str,
            collaborative=_COLLABORATIVE,
            commentable=_COMMENTABLE):
        """
        Shares the album with the given id and options

        Parameters
        ----------
        id: str
            Id of the album to be shared
        collaborative: bool, optional
            Set if the album is collabotative (default is set by
            set_collaborative_share(), whose default is False)
        commentable: bool, optional
            Set if the album is commentable (default is set by
            set_commentable_share(), whose default is True)

        Returns
        -------
        json object:
            ShareInfo object if all went well

        Notes
        -----
        This action is allowed only on albums which were created via the API.

        Examples
        --------
        Create new album and get its id:

        >>> new_album = album_manager.create('test album')
        >>> id_album = new_album.get("id")

        Share the newly created album

        >>> album_manager.share(id_album)
        {'sharedAlbumOptions': {'isCommentable': True}, 'shareableUrl': 'https://photos.app.goo.gl/...', 'shareToken': '...', 'isJoined': True, 'isOwned': True}

        Unshare the album

        >>> album_manager.unshare(id_album)
        {}
        """
        request_body = {
            "sharedAlbumOptions": {
                "isCollaborative": collaborative,
                "isCommentable": commentable
            }
        }
        result = self._service.albums().share(
            albumId=id,
            body=request_body).execute()
        return result.get('shareInfo')

    def unshare(self, id: str):
        """
        Unshares the album with the given id

        Parameters
        ----------
        id: str
            Id of the shared album to be unshared

        Returns
        -------
        json object:
            Empty if all went well

        Notes
        -----
        This action is allowed only on albums which were created via the API.

        Examples
        --------
        Create new album and get its id:

        >>> new_album = album_manager.create('test album')
        >>> id_album = new_album.get("id")

        Share the newly created album

        >>> album_manager.share(id_album)
        {'sharedAlbumOptions': {'isCommentable': True}, 'shareableUrl': 'https://photos.app.goo.gl/...', 'shareToken': '...', 'isJoined': True, 'isOwned': True}

        Unshare the album

        >>> album_manager.unshare(id_album)
        {}
        """
        return self._service.albums().unshare(albumId=id).execute()
