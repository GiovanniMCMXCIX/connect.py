from .load import Load
import json

BASE = "https://connect.monstercat.com"
API_BASE = BASE + "/api"


class Get:
    def __init__(self, session=None):
        self.data = None
        self.session = session

    def Id(self, json_data):
        _json = json.dumps(json_data)
        self.data = json.loads(_json)
        return self.data.get('_id')

    def release_Id(self, Id=None, track=False, release=True, json_data=None, use_json=False):
        if use_json is True:
            _json = json.dumps(json_data)
            self.data = json.loads(_json)
        else:
            if track is False:
                self.data = Load(self.session).release(Id)
            if release is False:
                self.data = Load(self.session).track(Id)

        return self.data.get('_id')

    def catalog_Id(self, album_Id=None, json_data=None, use_json=False):
        if use_json is True:
            _json = json.dumps(json_data)
            self.data = json.loads(_json)
        else:
            self.data = Load(self.session).release(album_Id)

        return self.data.get('catalogId')

    def song_artist(self, Id=None, track=False, release=True, json_data=None, use_json=False):
        if use_json is True:
            _json = json.dumps(json_data)
            self.data = json.loads(_json)
        else:
            if track is False:
                self.data = Load(self.session).release(Id)
            if release is False:
                self.data = Load(self.session).track(Id)

        if track is False:
            return self.data.get('renderedArtists')
        if release is False:
            return self.data.get('artistsTitle')

    def artist_name(self, vanityUri=None, json_data=None, use_json=False):
        if use_json is True:
            _json = json.dumps(json_data)
            self.data = json.loads(_json)
        else:
            self.data = Load(self.session).artist(vanityUri)

        return self.data.get('name')

    def artist_vanityUri(self, json_data):
        _json = json.dumps(json_data)
        self.data = json.loads(_json)
        return self.data.get('vanityUri')

    def artist_releases(self, vanityUri):
        return Load(self.session).artist_releases(vanityUri)

    def song_title(self, Id=None, track=False, release=True, json_data=None, use_json=False):
        if use_json is True:
            _json = json.dumps(json_data)
            self.data = json.loads(_json)
        else:
            if track is False:
                self.data = Load(self.session).release(Id)
            if release is False:
                self.data = Load(self.session).track(Id)

            return self.data.get('title')

    def duration(self, track_Id=None, json_data=None, use_json=False):
        if use_json is True:
            _json = json.dumps(json_data)
            self.data = json.loads(_json)
        else:
            self.data = Load(self.session).track(track_Id)

        return round(self.data.get('duration'))

    def bpm(self, track_Id=None, json_data=None, use_json=False):
        if use_json is True:
            _json = json.dumps(json_data)
            self.data = json.loads(_json)
        else:
            self.data = Load(self.session).track(track_Id)

        return round(self.data.get('bpm'))

    def streamHash(self, track_Id=None, json_data=None, use_json=False):
        if use_json is True:
            _json = json.dumps(json_data)
            self.data = json.loads(_json)
        else:
            self.data = Load(self.session).track(track_Id)

        albums = self.data.get('albums')
        if albums[0]['streamHash'] == "":
            return albums[1]['streamHash']
        else:
            return albums[0]['streamHash']

    def imageHash(self, album_Id=None, json_data=None, use_json=False):
        if use_json is True:
            _json = json.dumps(json_data)
            self.data = json.loads(_json)
        else:
            self.data = Load(self.session).release(album_Id)

        return self.data.get('imageHashSum')

    def urls(self, album_Id=None, json_data=None, use_json=False):
        if use_json is True:
            _json = json.dumps(json_data)
            self.data = json.loads(_json)
        else:
            self.data = Load(self.session).release(album_Id)

        return self.data.get('urls')


class DownloadLink:
    def __init__(self):
        self.url = None

    def track(self, album_Id, track_Id, mp3_320=False, mp3_128=False, mp3_v0=False, mp3_v2=False, wav=False,
              flac=False):
        if mp3_320 is True:
            self.url = API_BASE + "/release/" + album_Id + \
                       "/download?method=download&type=mp3_320&track=" + track_Id
            return self.url

        elif mp3_128 is True:
            self.url = API_BASE + "/release/" + album_Id + \
                       "/download?method=download&type=mp3_128&track=" + track_Id
            return self.url

        elif mp3_v0 is True:
            self.url = API_BASE + "/release/" + album_Id + \
                       "/download?method=download&type=mp3_v0&track=" + track_Id
            return self.url

        elif mp3_v2 is True:
            self.url = API_BASE + "/release/" + album_Id + \
                       "/download?method=download&type=mp3_v2&track=" + track_Id
            return self.url

        elif wav is True:
            self.url = API_BASE + "/release/" + album_Id + \
                       "/download?method=download&type=wav&track=" + track_Id
            return self.url

        elif flac is True:
            self.url = API_BASE + "/release/" + album_Id + \
                       "/download?method=download&type=flac&track=" + track_Id
            return self.url

    def release(self, album_Id, mp3_320=False, mp3_128=False, mp3_v0=False, mp3_v2=False, wav=False, flac=False):
        if mp3_320 is True:
            self.url = API_BASE + "/release/" + album_Id + "/download?method=download&type=mp3_320"
            return self.url

        elif mp3_128 is True:
            self.url = API_BASE + "/release/" + album_Id + "/download?method=download&type=mp3_128"
            return self.url

        elif mp3_v0 is True:
            self.url = API_BASE + "/release/" + album_Id + "/download?method=download&type=mp3_v0"
            return self.url

        elif mp3_v2 is True:
            self.url = API_BASE + "/release/" + album_Id + "/download?method=download&type=mp3_v2"
            return self.url

        elif wav is True:
            self.url = API_BASE + "/release/" + album_Id + "/download?method=download&type=wav"
            return self.url

        elif flac is True:
            self.url = API_BASE + "/release/" + album_Id + "/download?method=download&type=flac"
            return self.url
