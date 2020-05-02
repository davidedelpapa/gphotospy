class FILTER:
    NONE = 'NONE'
    LANDSCAPES = 'LANDSCAPES'
    RECEIPTS = 'RECEIPTS'
    CITYSCAPES = 'CITYSCAPES'
    LANDMARKS = 'LANDMARKS'
    SELFIES = 'SELFIES'
    PEOPLE = 'PEOPLE'
    PETS = 'PETS'
    WEDDINGS = 'WEDDINGS'
    BIRTHDAYS = 'BIRTHDAYS'
    DOCUMENTS = 'DOCUMENTS'
    TRAVEL = 'TRAVEL'
    ANIMALS = 'ANIMALS'
    FOOD = 'FOOD'
    SPORT = 'SPORT'
    NIGHT = 'NIGHT'
    PERFORMANCES = 'PERFORMANCES'
    WHITEBOARDS = 'WHITEBOARDS'
    SCREENSHOTS = 'SCREENSHOTS'


class Media:
    PAGESIZE = 100

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
        if n > 100:
            n = 100
        if n < 1:
            n = 1
        self.PAGESIZE = n

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
        the pagination can be set by album.set_pagination(n)
        with 1 < n < 100, since at least 1 album must be sought
        and 100 is the API maximum.  25 is API default.
        """
        page_token = ""
        while page_token is not None:
            result = self._service.mediaItems().list(
                pageSize=self.PAGESIZE,
                pageToken=page_token
            ).execute()
            page_token = result.get("nextPageToken", None)
            curr_list = result.get("mediaItems")
            for media in curr_list:
                yield media
