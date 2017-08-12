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
from .errors import NotFound
from .release import Release
from .track import Track
from .artist import Artist
from .playlist import Playlist
from .browse import BrowseEntry
from typing import List
from urllib.parse import quote


class Client:
    def __init__(self):
        self.http = HTTPClient()

    def sign_in(self, email: str, password: str, token: int = None):
        """Logs in the client with the specified credentials.

        Parameters
        ----------
        email: str

        password: str

        token: int


        Raises
        ------
        HTTPSException
            Invalid email, password or token.
        """
        if not token:
            self.http.email_sign_in(email, password)
        else:
            self.http.two_feature_sign_in(email, password, token)

    @property
    def is_signed_in(self):
        """bool: Indicates if the client has logged in successfully."""
        return self.http.is_singed_in()

    def sign_out(self):
        """Logs out of Monstercat Connect."""
        self.http.sign_out()

    def edit_profile(self, *, name: str = None, real_name: str = None, location: str = None, password: str = None):
        """Edits the current profile of the client.

        Parameters
        ----------
        name: str

        real_name: str

        location: str

        password: str


        Raises
        ------
        Forbidden
            The client isn't signed in order to edit the profile.
        """
        self.http.edit_profile(name=name, real_name=real_name, location=location, password=password)

    def add_reddit_username(self, username: str):
        """Adds the reddit username to the current profile of the client.

        Parameters
        ----------
        username: str


        Raises
        ------
        NotFound
            "I need to buy monstercat gold again in order to finish this library" ~ GiovanniMCMXCIX
        """
        self.http.add_reddit_username(username)

    def get_discord_invite(self) -> str:
        """Gets an invite for the gold discord channel on the monstercat discord guild.
        The client needs gold subscription in order to get the invite for that channel.

        Raises
        ------
        NotFound
            "I need to buy monstercat gold again in order to finish this library" ~ GiovanniMCMXCIX
        """
        return self.http.get_discord_invite()

    def get_release(self, catalog_id: str) -> Release:
        """Returns a release with the given ID.

        Parameters
        ----------
        catalog_id: str


        Raises
        ------
        NotFound
            The client couldn't get the release.
        """
        return Release(**self.http.get_release(catalog_id))

    def get_track(self, track_id: str) -> Track:
        """Returns a track with the given ID.

        Parameters
        ----------
        track_id: str


        Raises
        ------
        NotFound
            The client couldn't get the track.
        """
        return Track(**self.http.get_track(track_id))

    def get_artist(self, artist_id: str) -> Artist:
        """Returns a artist with the given ID.

        Parameters
        ----------
        artist_id: str


        Raises
        ------
        NotFound
            The client couldn't get the artist.
        """
        return Artist(**self.http.get_artist(artist_id))

    def get_playlist(self, playlist_id: str) -> Playlist:
        """Returns a playlist with the given ID.

        Parameters
        ----------
        playlist_id: str


        Raises
        ------
        Forbidden
            The client can't access a private playlist.
        NotFound
            The client couldn't get the playlist.
        """
        return Playlist(**self.http.get_playlist(playlist_id))

    def get_all_releases(self, *, singles: bool = True, eps: bool = True, albums: bool = True, podcasts: bool = False, limit: int = None, skip: int = None) -> List[Release]:
        """Retrieves every release the client can access.

        Parameters
        ----------
        singles: bool

        eps: bool

        albums: bool

        podcasts: bool

        limit: int
           The limit for how many tracks are supposed to be shown.
        skip: int
           Number of tracks that are skipped to be shown.
        """
        releases = []
        for release in self.http.get_all_releases(singles=singles, eps=eps, albums=albums, podcasts=podcasts, limit=limit, skip=skip)['results']:
            releases.append(Release(**release))
        return releases

    def get_all_tracks(self, *, limit: int = None, skip: int = None) -> List[Track]:
        """Retrieves every track the client can access.

        Parameters
        ----------
        limit: int
           The limit for how many tracks are supposed to be shown.
        skip: int
           Number of tracks that are skipped to be shown.
        """
        tracks = []
        for track in self.http.get_all_tracks(limit=limit, skip=skip)['results']:
            tracks.append(Track(**track))
        return tracks

    def get_all_artists(self, *, year: int = None, limit: int = None, skip: int = None) -> List[Artist]:
        """Retrieves every artist the client can access.

        Parameters
        ----------
        year: int
           The artists from the year specified that are to be shown.
        limit: int
           The limit for how many artists are supposed to be shown.
        skip: int
           Number of artists that are skipped to be shown.
        """
        artists = []
        for artist in self.http.get_all_artists(year=year, limit=limit, skip=skip)['results']:
            artists.append(Artist(**artist))
        return artists

    def get_all_playlists(self, *, limit: int = None, skip: int = None) -> List[Playlist]:
        """Retrieves every playlist the client can access.

        Raises
        ------
        Unauthorized
            The client isn't signed in.
        """
        playlists = []
        for playlist in self.http.get_all_playlists(limit=limit, skip=skip)['results']:
            playlists.append(Playlist(**playlist))
        return playlists

    def get_browse_entries(self, *, types: List[str] = None, genres: List[str] = None, tags: List[str] = None, limit: int = None, skip: int = None) -> List[BrowseEntry]:
        # I can't think of a better way to name this function...
        """Searches for a release.

        Parameters
        ----------
        types: List[str]

        genres: List[str]

        tags: List[str]

        limit: int
            The limit for how many releases are supposed to be shown.
        skip: int
            Number of releases that are skipped to be shown.

        Raises
        ------
        NotFound
            The client couldn't find any releases.
        """
        entries = []
        for entry in self.http.get_browse_entries(types=types, genres=genres, tags=tags, limit=limit, skip=skip)['results']:
            entries.append(BrowseEntry(**entry))
        if not entries:
            raise NotFound('No browse entry was found.')
        else:
            return entries

    def search_release(self, term: str, *, limit: int = None, skip: int = None) -> List[Release]:
        """Searches for a release.

        Parameters
        ----------
        term: str
           The release name that is searched.
        limit: int
           The limit for how many releases are supposed to be shown.
        skip: int
           Number of releases that are skipped to be shown.

        Raises
        ------
        NotFound
            The client couldn't find any releases.
        """
        releases = []
        for release in self.http.get(f'{self.http.RELEASE}?fuzzyOr=title,{quote(term)},renderedArtists,{quote(term)}&limit={limit}&skip={skip}')['results']:
            releases.append(Release(**release))
        if not releases:
            raise NotFound('No release was found.')
        else:
            return releases

    def search_release_advanced(self, title: str, artists: str, *, limit: int = None, skip: int = None) -> List[Release]:
        """Searches for a release in a more advanced way.

        Parameters
        ----------
        title: str
           The release title that is searched.
        artists: str
           The release artists that are searched.
        limit: int
           The limit for how many releases are supposed to be shown.
        skip: int
           Number of releases that are skipped to be shown.

        Raises
        ------
        NotFound
            The client couldn't find any releases.
        """
        releases = []
        for release in self.http.get(f'{self.http.RELEASE}?fuzzy=title,{quote(title)},renderedArtists,{quote(artists)}&limit={limit}&skip={skip}')['results']:
            releases.append(Release(**release))
        if not releases:
            raise NotFound('No release was found.')
        else:
            return releases

    def search_track(self, term: str, *, limit: int = None, skip: int = None) -> List[Track]:
        """Searches for a track.

        Parameters
        ----------
        term: str
           The track name that is searched.
        limit: int
           The limit for how many tracks are supposed to be shown.
        skip: int
           Number of tracks that are skipped to be shown.

        Raises
        ------
        NotFound
            The client couldn't find any tracks.
        """
        tracks = []
        for track in self.http.get(f'{self.http.TRACK}?fuzzyOr=title,{quote(term)},artistsTitle,{quote(term)}&limit={limit}&skip={skip}')['results']:
            tracks.append(Track(**track))
        if not tracks:
            raise NotFound('No track was found.')
        else:
            return tracks

    def search_track_advanced(self, title: str, artists: str, *, limit: int = None, skip: int = None) -> List[Track]:
        """Searches for a track in a more advanced way.

        Parameters
        ----------
        title: str
           The track title that is searched.
        artists: str
           The track artists that are searched.
        limit: int
           The limit for how many tracks are supposed to be shown.
        skip: int
           Number of tracks that are skipped to be shown.

        Raises
        ------
        NotFound
            The client couldn't find any tracks.
        """
        tracks = []
        for track in self.http.get(f'{self.http.TRACK}?fuzzy=title,{quote(title)},artistsTitle,{quote(artists)}&limit={limit}&skip={skip}')['results']:
            tracks.append(Track(**track))
        if not tracks:
            raise NotFound('No track was found.')
        else:
            return tracks

    def search_artist(self, term: str, *, year: int = None, limit: int = None, skip: int = None) -> List[Artist]:
        """Searches for a artist.

        Parameters
        ----------
        term: str
           The artist name that is searched.
        year: int
           The artists from the year specified that are to be shown.
        limit: int
           The limit for how many artists are supposed to be shown.
        skip: int
           Number of artists that are skipped to be shown.

        Raises
        ------
        NotFound
            The client couldn't find any artists.
        """
        artists = []
        base = f'{self.http.ARTIST}?limit={limit}&skip={skip}&fuzzyOr=name,{quote(term)}'
        if year:
            base.__add__(f',year,{year}')
        for artist in self.http.get(base)['results']:
            artists.append(Artist(**artist))
        if not artists:
            raise NotFound('No artist was found.')
        else:
            return artists

    def search_playlist(self, term: str, *, limit: int = None, skip: int = None) -> List[Playlist]:
        """Searches for a playlist.

        Parameters
        ----------
        term: str
           The playlist name that is searched.
        limit: int
           The limit for how many playlists are supposed to be shown.
        skip: int
           Number of playlists that are skipped to be shown.

        Raises
        ------
        Unauthorized
            The client isn't signed in.
        NotFound
            The client couldn't find any playlists.
        """
        playlists = []
        for playlist in self.http.get(f'{self.http.PLAYLIST}?fuzzyOr=name,{quote(term)}&limit={limit}&skip={skip}')['results']:
            playlists.append(Playlist(**playlist))
        if not playlists:
            raise NotFound('No playlist was found.')
        else:
            return playlists
