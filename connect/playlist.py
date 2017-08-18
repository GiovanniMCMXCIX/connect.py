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
from .release import ReleaseEntry


class Playlist:
    """Represents a release from connect.

        Attributes
        ----------
        id: str
            The playlist ID.
        name: str
            The playlist name.
        owner_id: str
            The owner id.
        is_public: bool
            If the playlist is public.
        is_deleted: bool
            If the playlist is deleted.
        """

    __slots__ = ['id', 'name', 'owner_id', 'is_public', 'is_deleted', '_tracks']

    def __init__(self, **kwargs):
        self.id = kwargs.pop('_id')
        self.name = kwargs.pop('name')
        self.owner_id = kwargs.pop('userId')
        self.is_public = kwargs.pop('public')
        self.is_deleted = kwargs.pop('deleted')
        self._tracks = {}

    def __eq__(self, other):
        return self.id == other.id and isinstance(other, self.__class__)

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.id != other.id
        return True

    def __str__(self):
        return self.name

    @property
    def tracks(self) -> list:
        """Returns a list of connect.playlist.PlaylistEntry items."""
        if self._tracks:
            return list(self._tracks.values())
        else:
            for t_data in HTTPClient().get_playlist_tracklist(self.id)['results']:
                track = PlaylistEntry(**t_data)
                self._add_track(track)
            return list(self._tracks.values())

    def _add_track(self, track):
        self._tracks[track.id] = track


class PlaylistEntry:
    """Represents a track from a playlist.

    Attributes
    ----------
    id: str
        The track ID.
    artists: str
        The track artists.
    title: str
        The track title.
    duration: int
        The track duration.
    bpm: int
        The track BPM.
    genre: str
        The track genre.
    genres: List[str]
        It usually returns a list with one item that is the same with :attr:`connect.Track.genre`
    release: :class:`release.ReleaseEntry`
        Release that the playlist entry is a part of.
    tags: List[str]
        The track tags.
    """

    __slots__ = [
        'id', 'artists', 'title', 'duration', 'bpm', 'genre', 'genres',
        'tags', 'release', '_albums_raw', '_artists_raw', '_albums', '_artists'
    ]

    def __init__(self, **kwargs):
        self.id = kwargs.pop('_id')
        self.artists = kwargs.pop('artistsTitle')
        self.title = kwargs.pop('title')
        duration = kwargs.pop('duration', None)
        bpm = kwargs.pop('bpm', None)
        self.duration = None if not duration else round(duration)
        self.bpm = None if not bpm else round(bpm)
        self.genre = kwargs.pop('genre', None)
        self.genres = kwargs.pop('genres')
        self.release = ReleaseEntry(**kwargs.pop('release'))
        self.tags = kwargs.pop('tags')
        self._albums_raw = kwargs.pop('albums')
        self._artists_raw = kwargs.pop('artists')
        self._albums = {}
        self._artists = {}
        self._from_data()

    def __eq__(self, other):
        return self.id == other.id and isinstance(other, self.__class__)

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.id != other.id
        return True

    def __str__(self):
        return f'{self.artists} - {self.title}'

    @property
    def albums(self) -> list:
        """List[:class:`release.Album`]: A list of Albums that this track is a part of."""
        return list(self._albums.values())

    def get_artists(self) -> list:
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
