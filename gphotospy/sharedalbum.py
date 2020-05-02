class SharedAlbum:

    PAGESIZE = 50
    SHOW_ONLY_CREATED = False

    def __init__(self, service):
        """
        Constructor. It takes the service created with authorize.init()

        Parameters
        ----------
        service: service
            Service created with authorize.init()
        """
        self._service = service

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
        self.PAGESIZE = n

    def show_only_created(self, val: bool):
        """
        Sets the list method to show only albums created by the API or not

        Parameters
        ----------
        val: bool
            value to be set (default is False)
        """
        self.SHOW_ONLY_CREATED = val

    # API ENDPOINTS
    def get(self):
        pass

    def join(self):
        pass

    def leave(self):
        pass

    def list(self, show_only_created=SHOW_ONLY_CREATED):
        """
        Iterator over the albums present in the Sharing tab

        Parameters
        ----------
        show_only_created: bool, optional
            Set if it has to list only albums created via the API
            (default is set by show_only_created(), whose default is FALSE)

        Returns
        -------
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
        """
        page_token = ""
        while page_token is not None:
            result = self._service.sharedAlbums().list(
                pageSize=self.PAGESIZE,
                excludeNonAppCreatedData=show_only_created,
                pageToken=page_token
            ).execute()
            page_token = result.get("nextPageToken", None)
            curr_list = result.get("sharedAlbums")
            for album in curr_list:
                yield album
