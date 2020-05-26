import os.path
import json
from urllib.request import urlopen
from .album import set_position, POSITION
from .upload import upload


class Val:
    """ Internal use only """

    def __init__(self, v, t: str):
        self.val = v
        self.type = t

    def isinstance(self, t: str):
        return t == self.type


class MediaItem(Val):
    """ Maps a MediaItem """

    def __init__(self, media_object):
        """ MediaItem Constructor """
        super().__init__(media_object, 'MEDIAITEM')

    def __str__(self):
        """ Used for print() """
        return(json.dumps(self.val, indent=4))

    def dimensions(self, max_width=0, max_height=0):
        """
        Gets media dimensions

        Parameters
        ----------
        max_width: int
            If specified sets a maximum allowed width
        max_height: int
            If specified sets a maximum allowed height

        Returns
        -------
        (int, int):
            (Width, Height) tuple

        Examples
        --------
        >>> media.get_media_dimesions(media_id)
        (720, 200)
        """
        metadata = self.val.get("mediaMetadata")
        width = int(metadata.get("width"))
        height = int(metadata.get("height"))
        if max_width != 0:
            if width > max_width:
                width = max_width
        if max_height != 0:
            if height > max_height:
                height = max_height
        return (width, height)

    def filename(self):
        """ Gets media filename """
        return self.val.get("filename", "")

    def metadata(self):
        """ Gets the MediaItem's metadata (JSON object mapped to a dict) """
        return self.val.get("mediaMetadata", {})

    def is_photo(self):
        """ Returns True if the media item is a photo """
        metadata = self.val.get("mediaMetadata")
        if "photo" in metadata:
            return True
        return False

    def is_video(self):
        """ Returns True if the media item is a video """
        metadata = self.val.get("mediaMetadata")
        if "video" in metadata:
            return True
        return False

    def get_url(self,
                for_download=True,
                max_width=0,
                max_height=0,
                crop=False):
        """
        Gets the media's URL.

        This method tries to recognize if the media is a video or a photo,
        and gets the URL accordingly.

        Parameters
        ----------
        for_download: bool
            Specify if the url is for download purposes.
            If False and the media is a video, it retrieves the thumbnail (default True)
        max_width: int
            If specified, sets the picture's or video thumbnail's maximum width
        max_height: int
            If specified, sets the picture's or video thumbnail's maximum height
        crop: bool
            If True, crops the image at the exact dimensions set by (default False)
        Returns
        -------
        Url: str

        Raise
        -----
        UnknownMediaType
            If it cannot guess which type is the media

        Examples
        --------
        >>> media.get_url()
        """
        base_url = self.val.get("baseUrl")
        metadata = self.val.get("mediaMetadata")
        if for_download:
            if "photo" in metadata:
                return "{}=d".format(base_url)
            elif "video" in metadata:
                return "{}=dv".format(base_url)
            else:
                raise UnknownMediaType
        # if max_width and max_height set to 0, gets them from media info
        if max_width == 0:
            max_width = metadata.get("width", 0)
        if max_height == 0:
            max_height = metadata.get("height", 0)
        url = "{}=w{}-h{}".format(base_url, max_width, max_height)
        if crop:
            url = "{}-c".format(url)
        return url

    def raw_download(self):
        """
        Downloads the raw media.

        This method tries to recognize if the media is a video or a photo,
        and downloads it accordingly.

        Returns
        -------
        File object data.
            Internally it applies a `read()` to the `rullib.urlopen`
            on the media address

        Raise
        -----
        UnknownMediaType
            If it cannot guess which type is the media

        Examples
        --------
        >>> media_iterator = media_manager.list()
        >>> media = MediaItem(next(media_iterator))

        Once we have the media item we can download the media as a file

        >>> with open(media.filename(), 'wb') as output:
        >>> ...    output.write(media.raw_download())
        """
        return urlopen(self.get_url()).read()


class MediaError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return(repr(self.msg))


class UnknownMediaType(MediaError):
    """Exception raised when donloading media has an unknown type"""
    pass


def date(year=0, month=0, day=0):
    """
    Return a Date object.

    Parameters
    ----------
    year: int
        Year component of the date. Set to 0 if searching for recurrences,
        when day and month is fixed, such as birthdays, ...
        Must be from 1 to 9999, or 0 if specifying a date without a year.
    month: int
        Month component of the date. Set to 0 month and day
        if only the year is significant.
        Must be from 1 to 12, or 0 if specifying a date without a month.
    day: int
        Day component of the date. Set to 0 if only month and year are
        to be sought, or set to 0 day and month if searching
        only for years.
        Must be from 1 to 31, and valid for the month, or 0 if specifying
        a date without a day.

    Returns
    -------
    Date object

    Examples
    --------
    Import

    >>> from gphotospy.media import date

    Set Christmas and search for Christmas media

    >>> Xmas = date(0, 12, 25)
    >>> search_iterator = media_manager.search(filter=[Xmas])
    >>> next(search_iterator)
    {'id': '...', 'productUrl': 'https://photos.google.com/lr/photo/...', 'baseUrl': 'https://lh3.googleusercontent.com/lr/...', 'mimeType': 'image/jpeg', 'mediaMetadata': {'creationTime': '...', 'width': '899', 'height': '1599', 'photo': {}}, 'filename': '...jpg'}
    """
    return Val({
        "year": year,
        "month": month,
        "day": day
    }, "DATE")


def date_range(start_date, end_date):
    """
    Return a dateRange object.

    Parameters
    ----------
    start_date: Date object
        Starting date of the range. Use date() function to set it
    end_date: Date object
        Ending date of the range. Use date() function to set it

    Returns
    -------
    dateRange object
    Examples
    --------
    Import

    >>> from gphotospy.media import date, date_range

    Set Christmas and search for Christmas media

    >>> Xmas = date(0, 12, 25)
    >>> new_year_eve = date(0, 12, 31)
    >>> my_range = date_range(Xmas, new_year_eve)
    >>> search_iterator = media_manager.search(filter=[my_range])
    >>> next(search_iterator)
    {'id': '...', 'productUrl': 'https://photos.google.com/lr/photo/...', 'baseUrl': 'https://lh3.googleusercontent.com/lr/...', 'mimeType': 'image/jpeg', 'mediaMetadata': {'creationTime': '...', 'width': '899', 'height': '1599', 'photo': {}}, 'filename': '...jpg'}
    """
    return Val({
        "startDate": start_date.val,
        "endDate": end_date.val
    }, "DATERANGE")


class CONTENTFILTER:
    """
    Filters to search media by categories

    Attributes
    ----------
    NONE:
        Default content category.
    LANDSCAPES:
        Media contains landscape
    RECEIPTS:
        Media contains receipts
    CITYSCAPES:
        Media contains cityscapes
    LANDMARKS:
        Media contains landmarks
    SELFIES:
        Media contains selfies
    PEOPLE:
        Media contains people
    PETS:
        Media contains pets
    WEDDINGS:
        Media contains wedding scenes
    BIRTHDAYS:
        Media contains birthday scenes
    DOCUMENTS:
        Media contains documents
    TRAVEL:
        Media contains media taken during
    ANIMALS:
        Media contains animals
    FOOD:
        Media contains food
    SPORT:
        Media contains sporting events
    NIGHT:
        Media taken at night
    PERFORMANCES:
        Media from performances
    WHITEBOARDS:
        Media contains whiteboards
    SCREENSHOTS:
        Media item is a screenshot
    UTILITY:
        Media that are considered utilities, such as documents, whiteboards, receipts, ...
    ARTS:
        Media contains art
    CRAFTS:
        Media contains crafts
    FASHION:
        Media is fashion related
    HOUSES:
        Media contains houses
    GARDENS:
        Media contains gardens
    FLOWERS:
        Media contains flowers
    HOLIDAYS:
        Media taken on holidays

    Examples
    --------
    Import

    >>> from gphotospy.media import CONTENTFILTER

    Search media by setting content

    >>> search_iterator = media_manager.search(filter=[CONTENTFILTER.TRAVEL])
    >>> next(search_iterator)
    {'id': '...', 'productUrl': 'https://photos.google.com/lr/photo/...', 'baseUrl': 'https://lh3.googleusercontent.com/lr/...', 'mimeType': 'image/jpeg', 'mediaMetadata': {'creationTime': '...', 'width': '899', 'height': '1599', 'photo': {}}, 'filename': '...jpg'}
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

    Attributes
    ----------
    ALL_MEDIA:
        All media types included
    VIDEO:
        Media is a video
    PHOTO:
        Media is a photo

    Examples
    --------
    Import

    >>> from gphotospy.media import MEDIAFILTER

    Search media by setting content

    >>> search_iterator = media_manager.search(filter=[MEDIAFILTER.VIDEO])
    >>> next(search_iterator)
    {'id': '...', 'productUrl': 'https://photos.google.com/lr/photo/...', 'baseUrl': 'https://lh3.googleusercontent.com/lr/...', 'mimeType': 'video/mp4', 'mediaMetadata': {'creationTime': '2020-05-07T15:05:13Z', 'width': '480', 'height': '848', 'video': {'fps': 30.000768068818967, 'status': 'READY'}}, 'filename': '...mp4'}
    """
    ALL_MEDIA = Val('ALL_MEDIA', 'MEDIAFILTER')
    VIDEO = Val('VIDEO', 'MEDIAFILTER')
    PHOTO = Val('PHOTO', 'MEDIAFILTER')


class FEATUREFILTER:
    """
    Filters to search media by feature

    Attributes
    ----------
    NONE:
        No filter applied
    FAVORITES:
        Media marked as favorites

    Examples
    --------
    Import

    >>> from gphotospy.media import FEATUREFILTER

    Search media by setting content

    >>> search_iterator = media_manager.search(filter=[FEATUREFILTER.FAVORITES])
    >>> next(search_iterator)
    """
    NONE = Val('NONE', 'FEATUREFILTER')
    FAVORITES = Val('FAVORITES', 'FEATUREFILTER')


class Media:
    """
    Media manager

    Examples
    --------
    Example init of the media manager:

    Imports

    >>> from gphotospy import authorize
    >>> from gphotospy.media import Media

    Select Secrets file

    >>> CLIENT_SECRET_FILE = "gphoto_oauth.json"

    Get authorization and return a service object

    >>> service = authorize.init(CLIENT_SECRET_FILE)

    Init the media manager

    >>> media_manager = Media(service)
    """
    _LIST_PAGESIZE = 100
    _SEARCH_PAGESIZE = 100

    _SHOW_ONLY_CREATED = False
    _INCLUDE_ARCHIVED = False

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
        >>> from gphotospy.media import Media

        Select Secrets file

        >>> CLIENT_SECRET_FILE = "gphoto_oauth.json"

        Get authorization and return a service object

        >>> service = authorize.init(CLIENT_SECRET_FILE)

        Init the media manager

        >>> media_manager = Media(service)
        """
        self._service = service["service"]
        self._secrets = service["secrets"]
        self._staged_media = []

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
        self._LIST_PAGESIZE = n

    def set_search_pagination(self, n: int):
        """ Undocumented: see search() """
        # There's really no need to change this,
        #  since the "list" is an iterator that takes care of pagination
        #  behind the scenes
        if n > 100:
            n = 100
        if n < 1:
            n = 1
        self._SEARCH_PAGESIZE = n

    def show_only_created(self, val: bool):
        """
        Sets the search method to show only media created by the API or not

        Parameters
        ----------
        val: bool
            value to be set (default is False)

        Examples
        --------
        >>> media_manager.show_only_created(False)
        """
        self._SHOW_ONLY_CREATED = val

    def show_archived(self, val: bool):
        """
        Sets the search method to show archived media or not

        Parameters
        ----------
        val: bool
            value to be set (default is False)

        Examples
        --------
        >>> media_manager.show_archived(False)
        """
        self._INCLUDE_ARCHIVED = val

    def get_upload_object(self, upload_token, file_name="", description=""):
        """
        Manually constructs an upload object.

        It is recommended to follow the stage procedure instead of the raw
        uploading method.

        Parameters
        ----------
        upload_token: upload token
            Upload token as returned from the upload.upload() function
        file_name: str, optional
            File name to register in the server, in the form of name.extension
        description: str, optional
            Description to display in the media info panel

        Returns
        -------
        Upload object
        """
        return {
            "description": description,
            "simpleMediaItem": {
                "uploadToken": upload_token,
                "fileName": file_name
            }
        }

    def stage_media(self, media_file, description=""):
        """
        Stage media to be added to the photo account,
        by uploading to Google server.

        To complete the operation all the staged media should be uploaded
        through the batchCreate() method (see).

        Parameters
        ----------
        media_file: Path
            Path of the media file to be uploaded
        description: str, optional
            Description to display in the media info panel

        Returns
        -------
        New media object if successfull, None if unsuccessfull.

        Examples
        --------
        Stage media (raw upload)

        >>> media_manager.stage_media(os.path.join(os.getcwd(), 'picture.jpg'))

        Finalize all staged media

        >>> media_manager.batchCreate()
        """
        upload_token = upload(self._secrets, media_file)
        if upload_token is None:
            return None
        new_media = self.get_upload_object(
            upload_token,
            os.path.basename(media_file),
            description)

        self._staged_media.append(new_media)
        return new_media

    # API ENDPOINTS

    def batchCreate(self,
                    album_id=None,
                    album_position=None,
                    media_items=None):
        """
        Create medias in the Photos account

        The media must be previously uploaded. It is recommended to stage them
        using the stage_media() method, and once a batch has been uploaded
        use this method to complete the transition.

        Parameters
        ----------
        media_items: list, optional
            List of upload objects, uploaded to the server.
            If you are using stage_media() ignore this parameter.
            if not staging, use upload.upload() to upload the file and get
            the token, and media.get_upload_object() to get the upload object,
            and create a list with these object to pass to this parameter.
        album_id: str
            Id of the album to attach the media to. It is optional, if not
            specified, it will create an album with the current date, and
            add all media to that album
        album_position: POSITION, optional
            Position in the album where to put the media.
            See the relative class in album.POSITION

        Returns
        -------
        Media item result (some media creation may fail, the list has
        the results for each attempted item creation)

        Examples
        --------
        Stage media (raw upload)

        >>> media_manager.stage_media(os.path.join(os.getcwd(), 'picture.jpg'))

        Finalize all staged media

        >>> res = media_manager.batchCreate()

        Advanced creation without stage_media:

        >>> from gphotospy.upload import upload
        >>> img_file = os.path.join(os.getcwd(), 'picture.jpg')

        Uploading file

        >>> upload_token = upload(service.get("secrets"), img_file)

        Constructing the upload file list

        >>> upload_items = []
        >>> upload_items.append(media_manager.get_upload_object(upload_token, description="a new picture"))

        Batch Create (we need an album's id)

        >>> media_manager.batchCreate(album_id, media_items=upload_items)
        """
        if album_position is None:
            album_position = set_position()
        if media_items is None:
            if len(self._staged_media) > 0:
                media_items = self._staged_media
            else:
                return None
        if album_id is None:
            from .album import Album
            from datetime import datetime
            curr_datetime = datetime.now()
            date_str = curr_datetime.strftime("%c")
            service_object = {
                "secrets": self._secrets,
                "service": self._service
            }
            _album = Album(service_object)
            _resp = _album.create(date_str)
            album_id = _resp.get("id")
        request_body = {
            "album_id": album_id,
            "newMediaItems": media_items,
            "albumPosition": album_position
        }
        if album_id is None:
            request_body["albumId"] = album_id
        result = self._service.mediaItems().batchCreate(
            body=request_body).execute()
        self._staged_media.clear()
        return result.get("newMediaItemResults")

    def get(self, id: str):
        """
        Returns the media info corresponding to the specified id

        Parameters
        ----------
        id: str
            Id of the media to get

        Returns
        -------
        json object:
            Media inforamtion

        Examples
        --------
        Get an iterator:

        >>> media_iterator = media_manager.list()

        Get next media's id

        >>> media_id = next(media_iterator).get("id")

        Get media's info based on id

        >>> media_manager.get(media_id)
        {'id': '...', 'productUrl': 'https://photos.google.com/lr/photo/...', 'baseUrl': 'https://lh3.googleusercontent.com/lr/...', 'mimeType': 'image/jpeg', 'mediaMetadata': {'creationTime': '...', 'width': '899', 'height': '1599', 'photo': {}}, 'filename': '...jpg'}
        """
        return self._service.mediaItems().get(mediaItemId=id).execute()

    def list(self):
        """
        Iterator over the meda present in the Google Photos account

        Yields
        -------
        Iterator over the list of media

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

        Examples
        --------
        Get iterator

        >>> media_iterator = media_manager.list()

        Print first item

        >>> print(next(media_iterator))
        """
        page_token = ""
        while page_token is not None:
            result = self._service.mediaItems().list(
                pageSize=self._LIST_PAGESIZE,
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
            filters to be included
        exclude: array
            filters to be excluded

        Yields
        ------
        Iterator over the list of media

        Notes
        -----
        There are 4 categories of filters, each with its own class.
        More info on the relative class.
        - Date Filter:
        - Content Filter:       class CONTENTFILTER
        - Media Type Filter:    class MEDIAFILTER
        - Feature Fileter:      class FEATUREFILTER

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
        if not isinstance(filter, list):
            filter = [filter]
        # dicts
        search_filter = {
            "includeArchivedMedia": self._INCLUDE_ARCHIVED,
            "excludeNonAppCreatedData": self._SHOW_ONLY_CREATED
        }

        filter_date = {}
        filter_daterange = {}
        filter_content = {}
        filter_mediatype = {}
        filter_feature = {}

        # lists
        date_filters = []
        daterange_filters = []
        content_filters = []
        mediatype_filters = []
        feature_filters = []

        content_excludes = []

        # Add filters
        for f in filter:
            if f.isinstance('DATE'):
                date_filters.append(f.val)
            if f.isinstance('DATERANGE'):
                daterange_filters.append(f.val)
            if f.isinstance('CONTENTFILTER'):
                content_filters.append(f.val)
            if f.isinstance('MEDIAFILTER'):
                mediatype_filters.append(f.val)
            if f.isinstance('FEATUREFILTER'):
                feature_filters.append(f.val)
        # Add exclude
        if exclude is not None:
            if not isinstance(exclude, list):
                exclude = [exclude]
            for e in exclude:
                if e.isinstance('CONTENTFILTER'):
                    content_excludes.append(e.val)

        # Add dicts

        if len(date_filters) > 0:
            filter_date["dates"] = date_filters
        if len(daterange_filters) > 0:
            filter_date["ranges"] = daterange_filters
        if len(content_filters) > 0:
            filter_content["includedContentCategories"] = content_filters
        if len(content_excludes) > 0:
            filter_content["excludedContentCategories"] = content_excludes

        if len(mediatype_filters) > 0:
            filter_mediatype["mediaTypes"] = mediatype_filters

        if len(feature_filters) > 0:
            filter_feature["includedFeatures"] = feature_filters

        # Construct filter
        if len(filter_date) > 0:
            search_filter["dateFilter"] = filter_date
        if len(filter_content) > 0:
            search_filter["contentFilter"] = filter_content
        if len(mediatype_filters) > 0:
            search_filter["mediaTypeFilter"] = filter_mediatype
        if len(feature_filters) > 0:
            search_filter["featureFilter"] = filter_feature

        # print(search_filter)

        page_token = ""
        request_body = {
            "pageSize": self._SEARCH_PAGESIZE,
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

    def search_album(self, album_id: str):
        """
        Specialized search in album, no other filter can apply.

        Parameters
        ----------
        album_id: str
            Id of the album containing the media sought

        Yields
        ------
        Iterator over the list of media present in the album

        Examples
        --------
        Get an album id

        >>> from gphotospy.album import Album
        >>> album_manager = Album(service)
        >>> album_iterator = album_manager.list()
        >>> album_id = next(album_iterator).get("id")

        Search in album

        >>> search_iterator = media_manager.search_album(album_id)
        >>> next(search_iterator)
        """
        page_token = ""
        request_body = {
            "albumId": album_id,
            "pageSize": self._SEARCH_PAGESIZE,
            "pageToken": page_token
        }

        while page_token is not None:
            result = self._service.mediaItems().search(
                body=request_body).execute()
            page_token = result.get("nextPageToken", None)
            curr_list = result.get("mediaItems")
            for media in curr_list:
                yield media
