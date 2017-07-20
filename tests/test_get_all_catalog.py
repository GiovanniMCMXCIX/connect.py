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

import unittest
import connect

client = connect.Client()


class TestGetAllCatalog(unittest.TestCase):
    @connect.utils.ignore_warnings
    def test_release(self):
        print('\n[connect.Client.get_all_releases]')
        releases = []
        for release in client.get_all_releases():
            releases.append((str(release), len(release.tracks)))
        print('There are {} total releases. (Normal Releases + Podcasts)'.format(len(releases)))

    @connect.utils.ignore_warnings
    def test_track(self):
        print('\n[connect.Client.get_all_tracks]')
        tracks = []
        for track in client.get_all_tracks():
            tracks.append((str(track), len(track.albums)))
        print('There are {} total tracks.'.format(len(tracks)))

    @connect.utils.ignore_warnings
    def test_artist(self):
        print('\n[connect.Client.get_all_artists]')
        artists = []
        for artist in client.get_all_artists():
            artists.append((str(artist), len(artist.releases)))
        print('There are {} total artists.'.format(len(artists)))
