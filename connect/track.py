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


class Track:
    """Represents a track from connect.

    Attributes
    ----------
    id : str
        The track ID.
    artists : str
        The track artists.
    title : str
        The track title.
    duration : int
        The track duration.
    bpm : int
        The track BPM.
    genre : str
        The track genre.
    genres : List[str]
        It usually returns a list with one item that is the same with :attr:`connect.Track.genre`.
    tags : List[str]
        The track tags.
    downloadable : bool
        Indicates if the track can be downloaded.
    streamable : bool
        Indicates if the track can be streamed.
    early_access : bool
        Indicates if the track is in early access for gold users.
    free_download : bool
        Indicates if the track can be downloaded for free.
    """

    __slots__ = [
        'id', 'artists', 'title', 'duration', 'bpm', 'genre', 'genres', 'tags', 'downloadable',
        'streamable', 'early_access', 'free_download', '_albums_raw', '_artists_raw', '_albums', '_artists'
    ]

    def __init__(self, **kwargs):
        self.id = kwargs.pop('_id')
        self.artists = kwargs.pop('artistsTitle', None)
        self.title = kwargs.pop('title', None)
        duration = kwargs.pop('duration', None)
        bpm = kwargs.pop('bpm', None)
        self.duration = None if not duration else round(duration)
        self.bpm = None if not bpm else round(bpm)
        self.genre = kwargs.pop('genre', None)
        self.genres = kwargs.pop('genres')
        self.tags = kwargs.pop('tags')
        self.downloadable = kwargs.pop('downloadable', None)
        self.streamable = kwargs.pop('streamable', None)
        self.early_access = kwargs.pop('inEarlyAccess', None)
        self.free_download = kwargs.pop('freeDownloadForUsers', None)
        self._albums_raw = kwargs.pop('albums')
        self._artists_raw = kwargs.pop('artists')
        self._albums = {}
        self._artists = {}
        self._from_data()

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return '{0.artists} - {0.title}'.format(self)

    @property
    def albums(self):
        """List[:class:`release.Album`]: A list of Albums that this track is a part of."""
        return list(self._albums.values())

    def get_artists(self):
        """List[:class:`artist.ArtistEntry`]: A list of artists that are featured."""
        return list(self._artists.values())

    def _add_album(self, album):
        self._albums[album.id] = album

    def _add_artist(self, artist):
        self._artists[artist.id] = artist

    def _from_data(self):
        from .release import Album
        for data in self._albums_raw:
            release = Album(**data)
            self._add_album(release)

        from .artist import ArtistEntry
        for data in self._artists_raw:
            artist = ArtistEntry(**data)
            self._add_artist(artist)
