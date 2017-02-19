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
from .release import Release
from .track import Track
from .artist import Artist
from .playlist import Playlist


class Client:
    def __init__(self):
        self.http = HTTPClient()

    def signin(self, email: str, password: str, token: int=None):
        if not token:
            self.http.email_signin(email, password)
        else:
            self.http.two_feature_signin(email, password, token)

    @property
    def is_signed_in(self):
        return self.http.is_singed_in()

    def signout(self):
        self.http.signout()

    def edit_profile(self, *, name: str=None, real_name: str=None, location: str=None, password: str=None):
        self.http.edit_profile(name=name, real_name=real_name, location=location, password=password)

    def add_reddit_username(self, username: str):
        self.http.add_reddit_username(username)

    def get_discord_gold_invite(self):
        return self.http.get_discord_gold_invite()

    def get_release(self, catalog_id: str):
        data = self.http.get_release(catalog_id)
        return Release(**data)

    def get_track(self, track_id: str):
        data = self.http.get_track(track_id)
        return Track(**data)

    def get_artist(self, artist_id: str):
        data = self.http.get_artist(artist_id)
        return Artist(**data)

    def get_playlist(self, playlist_id: str):
        data = self.http.get_playlist(playlist_id)
        return Playlist(**data)

    def get_all_releases(self):
        releases = []
        for release in self.http.get_release_list()['results']:
            releases.append(Release(**release))
        return releases

    def get_all_tracks(self):
        tracks = []
        for track in self.http.get_track_list()['results']:
            tracks.append(Track(**track))
        return tracks

    def get_all_artists(self):
        artists = []
        for artist in self.http.get_artist_list()['results']:
            artists.append(Artist(**artist))
        return artists

    def get_all_playlists(self):
        playlists = []
        for playlist in self.http.get_playlist_list()['results']:
            playlists.append(Playlist(**playlist))
        return playlists

    def search_release(self, term: str, limit=None, skip=None):
        releases = []
        for release in self.http.search_release(term, limit, skip)['results']:
            releases.append(Release(**release))
        return releases

    def search_release_advanced(self, title: str, artists: str, limit=None, skip=None):
        releases = []
        for release in self.http.search_release_advanced(title, artists, limit, skip)['results']:
            releases.append(Release(**release))
        return releases

    def search_track(self, term: str, limit=None, skip=None):
        tracks = []
        for track in self.http.search_track(term, limit, skip)['results']:
            tracks.append(Track(**track))
        return tracks

    def search_track_advanced(self, title: str, artists: str, limit=None, skip=None):
        tracks = []
        for track in self.http.search_track_advanced(title, artists, limit, skip)['results']:
            tracks.append(Track(**track))
        return tracks

    def search_artist(self, term: str, limit=None, skip=None):
        artists = []
        for artist in self.http.search_artist(term, limit, skip)['results']:
            artists.append(Artist(**artist))
        return artists

    def search_playlist(self, term: str, limit=None, skip=None):
        playlists = []
        for playlist in self.http.search_playlist(term, limit, skip)['results']:
            playlists.append(Playlist(**playlist))
        return playlists
