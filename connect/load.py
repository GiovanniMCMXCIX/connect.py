from pprint import pprint
import json

BASE = "https://connect.monstercat.com"
SIGNIN = BASE + "/signin"
API_BASE = BASE + "/api"
CATALOG = API_BASE + "/catalog"
PLAYLIST = API_BASE + "/playlist"
TRACK = CATALOG + "/track"
RELEASE = CATALOG + "/release"
ARTIST = CATALOG + "/artist"


class Load:
    def __init__(self, session):
        self.session = session

    def release(self, catalog_Id):
        album_raw = self.session.get(RELEASE + "/" + catalog_Id)

        if album_raw is None or album_raw.text is None:
            pprint(vars(album_raw))
            raise Exception("albums_raw or albums_raw.text is None!")

        album = json.loads(album_raw.text)
        return album

    def track(self, track_Id):
        track_raw = self.session.get(TRACK + "/" + track_Id)

        if track_raw is None or track_raw.text is None:
            pprint(vars(track_raw))
            raise Exception("albums_raw or albums_raw.text is None!")

        return json.loads(track_raw.text)

    def artist(self, vanityUri):
        artist_raw = self.session.get(ARTIST + "/" + vanityUri)

        if artist_raw is None or artist_raw.text is None:
            pprint(vars(artist_raw))
            raise Exception("albums_raw or albums_raw.text is None!")

        return json.loads(artist_raw.text)

    def artist_releases(self, vanityUri):
        releases_raw = self.session.get(ARTIST + "/" + vanityUri + "/releases")

        if releases_raw is None or releases_raw.text is None:
            pprint(vars(releases_raw))
            raise Exception("albums_raw or albums_raw.text is None!")

        return json.loads(releases_raw.text)

    def playlist(self, playlist_Id):
        playlist_raw = self.session.get(PLAYLIST + "/" + playlist_Id)

        if playlist_raw is None or playlist_raw.text is None:
            pprint(vars(playlist_raw))
            raise Exception("albums_raw or albums_raw.text is None!")

        return json.loads(playlist_raw.text)

    def track_list(self, release_Id):
        tracklist_raw = self.session.get(RELEASE + "/" + release_Id + "/tracks")

        if tracklist_raw is None or tracklist_raw.text is None:
            pprint(vars(tracklist_raw))
            raise Exception("albums_raw or albums_raw.text is None!")

        return json.loads(tracklist_raw.text)

    def release_list(self):
        albums_raw = self.session.get(RELEASE)

        if albums_raw is None or albums_raw.text is None:
            pprint(vars(albums_raw))
            raise Exception("albums_raw or albums_raw.text is None!")

        return json.loads(albums_raw.text)

    def playlist_list(self):
        playlists_raw = self.session.get(PLAYLIST)

        if playlists_raw is None or playlists_raw.text is None:
            pprint(vars(playlists_raw))
            raise Exception("albums_raw or albums_raw.text is None!")

        return json.loads(playlists_raw.text)
