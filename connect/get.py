from .load import Load
import json

BASE = "https://connect.monstercat.com"
API_BASE = BASE + "/api"
CATALOG = API_BASE + "/catalog"
RELEASE = CATALOG + "/release"


class Get:
    def __init__(self, session=None):
        self.data = None
        self.session = session

    def release_id(self, Id=None, track=False, release=True, json_data=None, use_json=False):
        if use_json is True:
            _json = json.dumps(json_data)
            self.data = json.loads(_json)
        else:
            if track is False:
                self.data = Load(self.session).release(Id)
            if release is False:
                self.data = Load(self.session).track(Id)

        release_id = self.data.get('_id')
        return release_id

    def id(self, json_data):
        _json = json.dumps(json_data)
        self.data = json.loads(_json)

        release_id = self.data.get('_id')
        return release_id

    def artist(self, Id=None, track=False, release=True, json_data=None, use_json=False):
        if use_json is True:
            _json = json.dumps(json_data)
            self.data = json.loads(_json)
        else:
            if track is False:
                self.data = Load(self.session).release(Id)
            if release is False:
                self.data = Load(self.session).track(Id)

        if track is False:
            return self.data.get("renderedArtists")
        if release is False:
            return self.data.get("artistsTitle")

    def title(self, Id=None, track=False, release=True, json_data=None, use_json=False):
        if use_json is True:
            _json = json.dumps(json_data)
            self.data = json.loads(_json)
        else:
            if track is False:
                self.data = Load(self.session).release(Id)
            if release is False:
                self.data = Load(self.session).track(Id)

        if track is False:
            return self.data.get("title")
        if release is False:
            return self.data.get("title")

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
            self.data = Load(self.session).track(album_Id)

        return self.data.get("imageHashSum")


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
