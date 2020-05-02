class Val:
    def __init__(self, v, t: str):
        self.val = v
        self.type = t

    def isinstance(self, t: str):
        return t == self.type


class CONTENTFILTER:
    """
    Filters to search media by categories

    Available Filters
    -----------------

    - NONE          Default content category.
    - LANDSCAPES    Media contains landscape
    - RECEIPTS      Media contains receipts
    - CITYSCAPES    Media contains cityscapes
    - LANDMARKS     Media contains landmarks
    - SELFIES       Media contains selfies
    - PEOPLE        Media contains people
    - PETS          Media contains pets
    - WEDDINGS      Media contains wedding scenes
    - BIRTHDAYS     Media contains birthday scenes
    - DOCUMENTS     Media contains documents
    - TRAVEL        Media contains media taken during
    - ANIMALS       Media contains animals
    - FOOD          Media contains food
    - SPORT         Media contains sporting events
    - NIGHT         Media taken at night
    - PERFORMANCES  Media from performances
    - WHITEBOARDS   Media contains whiteboards
    - SCREENSHOTS   Media item is a screenshot
    - UTILITY       Media that are considered utilities, such as documents,
                    whiteboards, receipts, ...
    - ARTS          Media contains art
    - CRAFTS        Media contains crafts
    - FASHION       Media is fashion related
    - HOUSES        Media contains houses
    - GARDENS       Media contains gardens
    - FLOWERS       Media contains flowers
    - HOLIDAYS      Media taken on holidays
    """
    NONE = Val('NONE', 'CONTENTFILTER')
    LANDSCAPES = Val('LANDSCAPES', 'CONTENTFILTER')
    RECEIPTS = Val('RECEIPTS', 'CONTENTFILTER')
    CITYSCAPES = Val('CITYSCAPES', 'CONTENTFILTER')
    LANDMARKS = Val('LANDMARKS', 'CONTENTFILTER')
    SELFIES = Val('SELFIES', 'CONTENTFILTER')
    PEOPLE = Val('PEOPLE', 'CONTENTFILTER')
    PETS = Val('PETS', 'CONTENTFILTER')
    WEDDINGS = Val('WEDDINGS', 'CONTENTFILTER')
    BIRTHDAYS = Val('BIRTHDAYS', 'CONTENTFILTER')
    DOCUMENTS = Val('DOCUMENTS', 'CONTENTFILTER')
    TRAVEL = Val('TRAVEL', 'CONTENTFILTER')
    ANIMALS = Val('ANIMALS', 'CONTENTFILTER')
    FOOD = Val('FOOD', 'CONTENTFILTER')
    SPORT = Val('SPORT', 'CONTENTFILTER')
    NIGHT = Val('NIGHT', 'CONTENTFILTER')
    PERFORMANCES = Val('PERFORMANCES', 'CONTENTFILTER')
    WHITEBOARDS = Val('WHITEBOARDS', 'CONTENTFILTER')
    SCREENSHOTS = Val('SCREENSHOTS', 'CONTENTFILTER')
    UTILITY = Val('UTILITY', 'CONTENTFILTER')
    ARTS = Val('ARTS', 'CONTENTFILTER')
    CRAFTS = Val('CRAFTS', 'CONTENTFILTER')
    FASHION = Val('FASHION', 'CONTENTFILTER')
    HOUSES = Val('HOUSES', 'CONTENTFILTER')
    GARDENS = Val('GARDENS', 'CONTENTFILTER')
    FLOWERS = Val('FLOWERS', 'CONTENTFILTER')
    HOLIDAYS = Val('HOLIDAYS', 'CONTENTFILTER')


class MEDIAFILTER:
    """
    Filters to search media by type

    Available Filters
    -----------------

    - ALL_MEDIA     All media types included
    - VIDEO         Media is a video
    - PHOTO         Media is a photo
    """
    ALL_MEDIA = Val('ALL_MEDIA', 'MEDIAFILTER')
    VIDEO = Val('VIDEO', 'MEDIAFILTER')
    PHOTO = Val('PHOTO', 'MEDIAFILTER')


class FEATUREFILTER:
    """
    Filters to search media by feature

    Available Filters
    -----------------

    - NONE          No filter applied
    - FAVORITES     Media marked as favorites
    """
    NONE = Val('NONE', 'FEATUREFILTER')
    FAVORITES = Val('FAVORITES', 'FEATUREFILTER')


class Media:
    LIST_PAGESIZE = 100
    SEARCH_PAGESIZE = 100

    SHOW_ONLY_CREATED = False
    INCLUDE_ARCHIVED = False

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
    def set_list_pagination(self, n: int):
        """ Undocumented: see list() """
        # There's really no need to change this,
        #  since the "list" is an iterator that takes care of pagination
        #  behind the scenes
        if n > 100:
            n = 100
        if n < 1:
            n = 1
        self.LIST_PAGESIZE = n

    def set_search_pagination(self, n: int):
        """ Undocumented: see search() """
        # There's really no need to change this,
        #  since the "list" is an iterator that takes care of pagination
        #  behind the scenes
        if n > 100:
            n = 100
        if n < 1:
            n = 1
        self.SEARCH_PAGESIZE = n

    def show_only_created(self, val: bool):
        """
        Sets the search method to show only media created by the API or not

        Parameters
        ----------
        val: bool
            value to be set (default is False)
        """
        self.SHOW_ONLY_CREATED = val

    def show_archived(self, val: bool):
        """
        Sets the search method to show archived media or not

        Parameters
        ----------
        val: bool
            value to be set (default is False)
        """
        self.INCLUDE_ARCHIVED = val

    # API ENDPOINTS
    def list(self):
        """
        Iterator over the meda present in the Google Photos account

        Returns
        -------
        iterator:
            iteratore over the list of media

        Notes
        -----
        Google Photo API list request returns in reality an object containing
        a paginated list of media.

        This function transforms the list in an iterator
        and takes care of pagination behind the scenes.

        Since there is a maximum limit on API requests per day per project
        it does not seem well to ask for less than the maximum pagination
        possible.

        However, if there are concerns of bandwith or speed,
        the pagination can be set by album.set_list_pagination(n)
        with 1 < n < 100, since at least 1 album must be sought
        and 100 is the API maximum.  25 is API default.
        """
        page_token = ""
        while page_token is not None:
            result = self._service.mediaItems().list(
                pageSize=self.LIST_PAGESIZE,
                pageToken=page_token
            ).execute()
            page_token = result.get("nextPageToken", None)
            curr_list = result.get("mediaItems")
            for media in curr_list:
                yield media

    def search(self, filter, exclude=None):
        """
        Iterator over a filtered search of all the media
        present in the Google Photos account.

        Parameters
        ----------
        fileter: array
            filtrs to be included
        exclude: array
            filtrs to be excluded

        Filters
        -------
        There are 4 categories of filters, each with its own class.
        More info on the relative class.
        - Date Filter:
        - Content Filter:       class CONTENTFILTER
        - Media Type Filter:    class MEDIAFILTER
        - Feature Fileter:      class FEATUREFILTER

        Returns
        -------
        iterator:
            iteratore over the list of media

        Notes
        -----
        Google Photo API search request returns in reality an object containing
        a paginated list of media.

        This function transforms the list in an iterator
        and takes care of pagination behind the scenes.

        Since there is a maximum limit on API requests per day per project
        it does not seem well to ask for less than the maximum pagination
        possible.

        However, if there are concerns of bandwith or speed,
        the pagination can be set by album.set_search_pagination(n)
        with 1 < n < 100, since at least 1 album must be sought
        and 100 is the API maximum.  25 is API default.
        """

        # dicts
        search_filter = {
            "includeArchivedMedia": self.INCLUDE_ARCHIVED,
            "excludeNonAppCreatedData": self.SHOW_ONLY_CREATED
        }
        filter_content = {}
        filter_date = {}
        filter_mediatype = {}
        filter_feature = {}

        # lists
        date_filters = []
        content_filters = []
        mediatype_filters = []
        feature_filters = []

        content_excludes = []

        # Add filters
        for f in filter:
            if f.isinstance('CONTENTFILTER'):
                content_filters.append(f.val)
            if f.isinstance('MEDIAFILTER'):
                mediatype_filters.append(f.val)
            if f.isinstance('FEATUREFILTER'):
                feature_filters.append(f.val)
        # Add exclude
        if exclude is not None:
            for e in exclude:
                if e.isinstance('CONTENTFILTER'):
                    content_excludes.append(e.val)

        # Add dicts
        '''
        # TODO: dates filters
        if len(date_filters) > 0
            filter_date["includedContentCategories"] = date_filters
        '''
        if len(content_filters) > 0:
            filter_content["includedContentCategories"] = content_filters
        if len(content_excludes) > 0:
            filter_content["excludedContentCategories"] = content_excludes

        if len(mediatype_filters) > 0:
            filter_mediatype["mediaTypes"] = mediatype_filters

        if len(feature_filters) > 0:
            filter_feature["includedFeatures"] = feature_filters

        # Construct filter
        if len(filter_content) > 0:
            search_filter["contentFilter"] = filter_content
        if len(mediatype_filters) > 0:
            search_filter["mediaTypeFilter"] = filter_mediatype
        if len(feature_filters) > 0:
            search_filter["featureFilter"] = filter_feature

        # print(search_filter)

        page_token = ""
        request_body = {
            "pageSize": self.SEARCH_PAGESIZE,
            "pageToken": page_token,
            "filters": search_filter
        }

        while page_token is not None:
            result = self._service.mediaItems().search(
                body=request_body).execute()
            page_token = result.get("nextPageToken", None)
            curr_list = result.get("mediaItems")
            for media in curr_list:
                yield media

    def search_album(self, album_id):
        """
        Specialized search in album, no other filter can apply.

        You can consider using instead Album.list() for similar purposes
        """
        pass
