# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2016-2017 GiovanniMCMXCIX

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from .http import HTTPClient
from .track import Track
from . import utils


class Release:
    """Represents a release from connect.
    
    Attributes
    ----------
    id : str
        The release ID.
    catalog_id : str
        The Catalog ID of the release. Could be None.
    artists : str
        The release artists.
    title : str
        The release title.
    release_date : datetime.datetime
        A naive UTC datetime object containing the time the release was launched.
    type : str
        Release type.
    urls : List[str]
        A list of urls for supporting or listening to the release.
    downloadable : bool
        Indicates if the release can be downloaded.
    streamable : bool
        Indicates if the release can be streamed.
    early_access : bool
        Indicates if the release is in early access for gold users.
    free_download : bool
        Indicates if the track can be downloaded for free.
    """

    __slots__ = [
        'id', 'catalog_id', 'artists', 'title', 'release_date', 'type', 'cover_url',
        'urls', 'downloadable', 'streamable', 'early_access', 'free_download', '_tracks'
    ]

    def __init__(self, **kwargs):
        self.id = kwargs.pop('_id')
        self.catalog_id = kwargs.pop('catalogId', None)
        self.artists = kwargs.pop('renderedArtists', None)
        self.title = kwargs.pop('title', None)
        self.release_date = utils.parse_time(kwargs.pop('releaseDate'))
        self.type = kwargs.pop('type')
        self.cover_url = kwargs.pop('coverUrl')
        self.urls = kwargs.pop('urls')
        self.downloadable = kwargs.pop('downloadable', None)
        self.streamable = kwargs.pop('streamable', None)
        self.early_access = kwargs.pop('inEarlyAccess', None)
        self.free_download = kwargs.pop('freeDownloadForUsers')
        self._tracks = {}

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __str__(self):
        return '{0.artists} - {0.title}'.format(self)

    def thumbnails(self, resolution: int):
        """Returns a hash to a bound resolution."""
        return '{}?image_width={}'.format(self.cover_url, resolution)

    def _add_track(self, track):
        self._tracks[track.id] = track

    @property
    def tracks(self):
        """Returns a list of connect.Tracks items."""
        if self._tracks:
            return list(self._tracks.values())
        else:
            for t_data in HTTPClient().get_release_tracklist(self.id)['results']:
                track = Track(**t_data)
                self._add_track(track)
            return list(self._tracks.values())


class ReleaseEntry:
    """Represents a release from a playlist track.

    Attributes
    ----------
    id : str
        The release ID.
    catalog_id : str
        The Catalog ID of the release. Could be None.
    title : str
        The release title.
    release_date : datetime.datetime
        A naive UTC datetime object containing the time the release was launched.
    """

    __slots__ = ['id', 'catalog_id', 'title', 'release_date']

    def __init__(self, **kwargs):
        self.id = kwargs.pop('_id')
        self.catalog_id = kwargs.pop('catalogId', None)
        self.title = kwargs.pop('title')
        self.release_date = utils.parse_time(kwargs.pop('releaseDate'))

    def __eq__(self, other):
        return self.id == other.id and isinstance(other, self.__class__)

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.id != other.id
        return True

    def __str__(self):
        return self.title


class Album:
    """Represents a release from a track.

    Attributes
    ----------
    id : str
        The release ID.
    track_number : int
        Placement in a release.
    stream_id : str
        The stream hash of the release.
    """

    __slots__ = ['id', 'track_number', 'stream_id']

    def __init__(self, **kwargs):
        self.id = kwargs.pop('albumId')
        self.track_number = kwargs.pop('trackNumber')
        stream_id = kwargs.pop('streamHash')
        self.stream_id = None if stream_id in [None, ''] else stream_id

    def __eq__(self, other):
        return self.id == other.id and isinstance(other, self.__class__)

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.id != other.id
        return True

    @property
    def stream_url(self):
        """Returns a friendly URL version of the stream_id variable the release has."""
        if not self.stream_id:
            return None
        else:
            return 'https://s3.amazonaws.com/data.monstercat.com/blobs/{0.stream_id}'.format(self)
