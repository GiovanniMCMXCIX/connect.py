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

import requests
import json
import sys
import re

from .errors import HTTPSException, Unauthorized, Forbidden, NotFound
from . import utils, __version__


class HTTPClient:
    BASE = 'https://connect.monstercat.com'
    SIGN_IN = BASE + '/signin'
    SIGN_OUT = BASE + '/signout'
    API_BASE = BASE + '/api'
    SELF = API_BASE + '/self'
    CATALOG = API_BASE + '/catalog'
    PLAYLIST = API_BASE + '/playlist'
    TRACK = CATALOG + '/track'
    RELEASE = CATALOG + '/release'
    ARTIST = CATALOG + '/artist'
    BROWSE = CATALOG + '/browse'

    def __init__(self):
        self.session = requests.Session()
        self.download_link_gen = utils.DownloadLinkGenerator()

        user_agent = 'ConnectBot (https://github.com/GiovanniMCMXCIX/connect.py {0}) ' \
                     'Python/{1[0]}.{1[1]} requests/{2}'
        self.user_agent = user_agent.format(__version__, sys.version_info, requests.__version__)

    def request(self, method, url, **kwargs):
        headers = {
            'User-Agent': self.user_agent
        }

        if 'json' in kwargs:
            headers['Content-Type'] = 'application/json'
            kwargs['data'] = utils.to_json(kwargs.pop('json'))

        kwargs['headers'] = headers
        response = self.session.request(method, url, **kwargs)
        try:
            if 'stream' in kwargs:
                def raise_error(error, use_response=False):
                    try:
                        if use_response:
                            raise error(json.loads(response.text).pop('message', 'Unknown error'), response)
                        else:
                            raise error(json.loads(response.text).pop('message', 'Unknown error'))
                    except json.decoder.JSONDecodeError:
                        if use_response:
                            raise error({'message': response.text} if response.text else 'Unknown error', response)
                        else:
                            raise error({'message': response.text} if response.text else 'Unknown error')

                if 300 > response.status_code >= 200:
                    return response
                elif response.status_code == 401:
                    raise_error(Unauthorized)
                elif response.status_code == 403:
                    raise_error(Forbidden)
                elif response.status_code == 404:
                    raise_error(NotFound)
                else:
                    raise_error(HTTPSException, True)
            else:
                try:
                    data = json.loads(response.text)
                except json.decoder.JSONDecodeError:
                    data = {'message': response.text} if response.text else None

                if 300 > response.status_code >= 200:
                    return data
                elif response.status_code == 401:
                    raise Unauthorized(data.pop('message', 'Unknown error'))
                elif response.status_code == 403:
                    raise Forbidden(data.pop('message', 'Unknown error'))
                elif response.status_code == 404:
                    raise NotFound(data.pop('message', 'Unknown error'))
                else:
                    raise HTTPSException(data.pop('message', 'Unknown error'), response)
        except Exception as e:
            raise e

    def get(self, *args, **kwargs):
        return self.request('GET', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.request('PUT', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.request('PATCH', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.request('DELETE', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request('POST', *args, **kwargs)

    def email_sign_in(self, email, password):
        payload = {
            'email': email,
            'password': password
        }
        self.post(self.SIGN_IN, json=payload)

    def two_feature_sign_in(self, email, password, token):
        payload = {
            'token': token
        }
        self.email_sign_in(email, password)
        self.post('{0.SIGN_IN}/token'.format(self), json=payload)

    def is_singed_in(self):
        response = self.get('{0.SELF}/session'.format(self))
        if not response.get('user'):
            return False
        if response.get('user').get('subscriber', False) is True:
            return True

    def sign_out(self):
        self.post(self.SIGN_OUT)

    def self(self):
        return self.get(self.SELF)

    def create_playlist(self, name, *, public=False, entries=None):
        payload = {
            'name': name,
            'public': public
        }
        if entries:
            payload['tracks'] = entries
        return self.post('{0.PLAYLIST}'.format(self), json=payload)

    def edit_profile(self, *, name=None, real_name=None, location=None, password=None):
        payload = {}
        if name:
            payload['name'] = name
        if real_name:
            payload['realName'] = real_name
        if location:
            payload['location'] = location
        if password:
            payload['password'] = password
        return self.patch(self.SELF, json=payload)

    def edit_playlist(self, playlist_id, *, name=None, public=False):
        payload = {}
        if name:
            payload['name'] = name
        if public:
            payload['public'] = public
        return self.patch('{0.PLAYLIST}/{1}'.format(self, playlist_id), json=payload)

    def add_playlist_track(self, playlist_id, track_id, release_id):
        playlist = self.get_playlist(playlist_id)
        playlist['tracks'].append({'trackId': track_id, 'releaseId': release_id})
        return self.put('{0.PLAYLIST}/{1}'.format(self, playlist_id), json=playlist)

    def add_playlist_tracks(self, playlist_id, entries):
        playlist = self.get_playlist(playlist_id)
        for entry in entries:
            playlist['tracks'].append(entry)
        return self.put('{0.PLAYLIST}/{1}'.format(self, playlist_id), json=playlist)

    def add_reddit_username(self, username):
        payload = {
            'redditUsername': username
        }
        self.post('{0.SELF}/update-reddit'.format(self), json=payload)

    def delete_playlist(self, playlist_id):
        return self.delete('{0.PLAYLIST}/{1}'.format(self, playlist_id))

    def delete_playlist_track(self, playlist_id, track_id):
        playlist = self.get_playlist(playlist_id)
        track = [item for item in playlist['tracks'] if item['trackId'] == track_id][0]
        del playlist['tracks'][playlist['tracks'].index(track)]
        return self.put('{0.PLAYLIST}/{1}'.format(self, playlist_id), json=playlist)

    def download_release(self, album_id, path, audio_format):
        r = self.get(self.download_link_gen.release(album_id, audio_format), stream=True)
        filename = str.replace(re.findall("filename=(.+)", r.headers['content-disposition'])[0], "\"", "")
        full_path = path + "/" + filename

        with open(full_path, 'wb') as file:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        return True

    def download_track(self, album_id, track_id, path, audio_format):
        r = self.get(self.download_link_gen.track(album_id, track_id, audio_format), stream=True)
        filename = str.replace(re.findall("filename=(.+)", r.headers['content-disposition'])[0], "\"", "")
        full_path = path + "/" + filename

        with open(full_path, 'wb') as file:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        return True

    def download_playlist(self, playlist_id, page, path, audio_format):
        r = self.get(self.download_link_gen.playlist(playlist_id, audio_format, page), stream=True)
        filename = str.replace(re.findall("filename=(.+)", r.headers['content-disposition'])[0], "\"", "")
        full_path = path + "/" + filename

        with open(full_path, 'wb') as file:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        return True

    def get_discord_invite(self):
        return self.get('{0.SELF}/discord/gold'.format(self))

    def get_release(self, catalog_id):
        return self.get('{0.RELEASE}/{1}'.format(self, catalog_id))

    def get_release_tracklist(self, release_id):
        return self.get('{0.RELEASE}/{1}/tracks'.format(self, release_id))

    def get_track(self, track_id):
        return self.get('{0.TRACK}/{1}'.format(self, track_id))

    def get_artist(self, artist_id):
        return self.get('{0.ARTIST}/{1}'.format(self, artist_id))

    def get_artist_releases(self, artist_id):
        return self.get('{0.ARTIST}/{1}/releases'.format(self, artist_id))

    def get_playlist(self, playlist_id):
        return self.get('{0.PLAYLIST}/{1}'.format(self, playlist_id))

    def get_playlist_tracklist(self, playlist_id):
        return self.get('{0.PLAYLIST}/{1}/tracks'.format(self, playlist_id))

    def get_browse_entries(self, *, types=None, genres=None, tags=None, limit=None, skip=None):
        query = []
        if types:
            query.append('&types={}'.format(','.join(types)))
        if genres:
            query.append('&genres={}'.format(','.join(genres)))
        if tags:
            query.append('&tags={}'.format(','.join(tags)))
        return self.get('{0.BROWSE}?limit={1}&skip={2}{3}'.format(self, limit, skip, ''.join(query)))

    def get_all_releases(self, *, singles=True, eps=True, albums=True, podcasts=False, limit=None, skip=None):
        query = []
        if singles:
            query.append('type,Single')
        if eps:
            query.append('type,EP')
        if albums:
            query.append('type,Album')
        if podcasts:
            query.append('type,Podcast')
        if not singles and not eps and not albums and not podcasts:
            return self.get('{0.RELEASE}?fuzzyOr=type,None'.format(self))
        else:
            return self.get('{0.RELEASE}?fuzzyOr={1}&limit={2}&skip={3}'.format(self, ','.join(query), limit, skip))

    def get_all_tracks(self, limit=None, skip=None):
        return self.get('{0.TRACK}?limit={1}&skip{2}'.format(self, limit, skip))

    def get_all_artists(self, year=None, limit=None, skip=None):
        base = '{0.ARTIST}?limit={1}&skip={2}'.format(self, limit, skip)
        if year:
            base.__add__('&fuzzy=year,{}'.format(year))
        return self.get(base)

    def get_all_playlists(self, *, limit=None, skip=None):
        return self.get('{0.PLAYLIST}?limit={1}&skip={2}'.format(self, limit, skip))
