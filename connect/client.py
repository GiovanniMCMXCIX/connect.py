import requests
import json

from .download import Download
from .get import Get, DownloadLink
from .load import Load
from .search import SearchSimple, SearchAdvanced


class Client:
    def __init__(self):
        self.session = requests.Session()
        self.email = None
        self.password = None

    def login(self, email, password):
        self.email = email
        self.password = password

    def connect(self):
        payload = {"email": self.email, "password": self.password}

        response_raw = self.session.post("https://connect.monstercat.com/signin", data=payload)
        response = json.loads(response_raw.text)

        if len(response) > 0:
            raise Exception("Sign-In Error: " + response.get("message", "Unknown error"))

    def start(self, email, password):
        self.login(email, password)
        self.connect()

    def download(self, path, album_Id, track_Id=None, audio_format="mp3 320", get_track=False):
        if audio_format == "mp3 320":
            Download(self.session, path, album_Id, track_Id, "mp3 320", get_track)
        elif audio_format == "mp3 128":
            Download(self.session, path, album_Id, track_Id, "mp3 128", get_track)
        elif audio_format == "mp3 v0":
            Download(self.session, path, album_Id, track_Id, "mp3 v0", get_track)
        elif audio_format == "mp3 v2":
            Download(self.session, path, album_Id, track_Id, "mp3 v2", get_track)
        elif audio_format == 'flac':
            Download(self.session, path, album_Id, track_Id, "flac", get_track)
        elif audio_format == "wav":
            Download(self.session, path, album_Id, track_Id, "wav", get_track)

    def search_track(self, song: str, artist: str=None, limit: str=None, skip: str=None, use_limit=False, use_skip=False, simple=True, advanced=False):
        if advanced is True and simple is False:
            return SearchAdvanced(self.session).track(song, artist, limit, skip, use_limit, use_skip)
        if simple is True and advanced is False:
            return SearchSimple(self.session).track(song, limit, skip, use_limit, use_skip)

    def search_release(self, song: str, artist: str=None, limit: str=None, skip: str=None, use_limit=False, use_skip=False, simple=True, advanced=False):
        if advanced is True and simple is False:
            return SearchAdvanced(self.session).release(song, artist, limit, skip, use_limit, use_skip)
        if simple is True and advanced is False:
            return SearchSimple(self.session).release(song, limit, skip, use_limit, use_skip)

    def search_artist(self, artist: str=None, limit: str=None, skip: str=None, use_limit=False, use_skip=False, simple=True, advanced=False):
        if advanced is True and simple is False:
            return SearchAdvanced(self.session).artist(artist, limit, skip, use_limit, use_skip)
        if simple is True and advanced is False:
            return SearchSimple(self.session).artist(artist, limit, skip, use_limit, use_skip)

    def get_song_artist(self, Id=None, track=False, release=True, json_data=None, use_json=False):
        return Get(self.session).song_artist(Id, track, release, json_data, use_json)

    def get_artist_name(self, vanityUri=None, json_data=None, use_json=False):
        return Get(self.session).artist_name(vanityUri, json_data, use_json)

    @staticmethod
    def get_artist_vanityUri(json_data):
        return Get().artist_vanityUri(json_data)

    def get_artist_releases(self, vanityUri):
        return Get(self.session).artist_releases(vanityUri)

    def get_song_title(self, Id=None, track=False, release=True, json_data=None, use_json=False):
        return Get(self.session).song_title(Id, track, release, json_data, use_json)

    def get_streamHash(self, track_Id=None, json_data=None, use_json=False):
        return Get(self.session).streamHash(track_Id, json_data, use_json)

    def get_imageHash(self, album_Id=None, json_data=None, use_json=False):
        return Get(self.session).imageHash(album_Id, json_data, use_json)

    def get_release_Id(self, Id=None, track=False, release=True, json_data=None, use_json=False):
        return Get(self.session).release_id(Id, track, release, json_data, use_json)

    def get_Id(self, json_data):
        return Get(self.session).id(json_data)

    def get_all_releases(self):
        return Load(self.session).release_list()

    def get_all_playlists(self):
        return Load(self.session).playlist_list()

    def get_tracklist(self, release_Id):
        return Load(self.session).track_list(release_Id)

    def load_release(self, release_Id):
        return Load(self.session).release(release_Id)

    def load_track(self, track_Id):
        return Load(self.session).track(track_Id)

    def load_artist(self, vanityUri):
        return Load(self.session).artist(vanityUri)

    def load_playlist(self, playlist_Id):
        return Load(self.session).playlist(playlist_Id)

    @staticmethod
    def get_download_link(album_Id, track_Id=None, audio_format="mp3 320", get_track=False):
        if get_track is False:
            if audio_format == "mp3 320":
                return DownloadLink().release(album_Id=album_Id, mp3_320=True)
            elif audio_format == "mp3 128":
                return DownloadLink().release(album_Id=album_Id, mp3_128=True)
            elif audio_format == "mp3 v0":
                return DownloadLink().release(album_Id=album_Id, mp3_v0=True)
            elif audio_format == "mp3 v2":
                return DownloadLink().release(album_Id=album_Id, mp3_v2=True)
            elif audio_format == "flac":
                return DownloadLink().release(album_Id=album_Id, flac=True)
            elif audio_format == "wav":
                return DownloadLink().release(album_Id=album_Id, wav=True)
        else:
            if audio_format == "mp3 320":
                return DownloadLink().track(album_Id=album_Id, track_Id=track_Id, mp3_320=True)
            elif audio_format == "mp3 128":
                return DownloadLink().track(album_Id=album_Id, track_Id=track_Id, mp3_128=True)
            elif audio_format == "mp3 v0":
                return DownloadLink().track(album_Id=album_Id, track_Id=track_Id, mp3_v0=True)
            elif audio_format == "mp3 v2":
                return DownloadLink().track(album_Id=album_Id, track_Id=track_Id, mp3_v2=True)
            elif audio_format == 'flac':
                return DownloadLink().track(album_Id=album_Id, track_Id=track_Id, flac=True)
            elif audio_format == "wav":
                return DownloadLink().track(album_Id=album_Id, track_Id=track_Id, wav=True)
