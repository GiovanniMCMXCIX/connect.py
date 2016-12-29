BASE = "https://connect.monstercat.com"
SIGNIN = BASE + "/signin"
API_BASE = BASE + "/api"
CATALOG = API_BASE + "/catalog"
TRACK = CATALOG + "/track"
RELEASE = CATALOG + "/release"
ARTIST = CATALOG + "/artist"


class SearchSimple:
    def __init__(self, session):
        self.session = session

    def track(self, term, limit=None, skip=None, use_limit=False, use_skip=False):
        if use_limit and use_skip is True:
            search_url = TRACK + "?limit=" + limit + \
                         "&skip=" + skip + "&fuzzyOr=title%2C" + term + "%2CartistsTitle%2C" + term
            track_raw = self.session.get(search_url)
            _track = track_raw.json()
            return _track
        elif use_limit is True:
            search_url = TRACK + "?limit=" + limit + "&fuzzyOr=title%2C" + term + "%2CartistsTitle%2C" + term
            track_raw = self.session.get(search_url)
            _track = track_raw.json()
            return _track
        elif use_skip is True:
            search_url = TRACK + "?skip=" + skip + "&fuzzyOr=title%2C" + term + "%2CartistsTitle%2C" + term
            track_raw = self.session.get(search_url)
            _track = track_raw.json()
            return _track
        else:
            search_url = TRACK + "?fuzzyOr=title%2C" + term + "%2CartistsTitle%2C" + term
            _track_raw = self.session.get(search_url)
            _track = _track_raw.json()
            return _track

    def release(self, term, limit=None, skip=None, use_limit=False, use_skip=False):
        if use_limit and use_skip is True:
            search_url = RELEASE + "?limit=" + limit + \
                         "&skip=" + skip + "&fuzzyOr=title%2C" + term + "%2CrenderedArtists%2C" + term
            release_raw = self.session.get(search_url)
            _release = release_raw.json()
            return _release
        elif use_limit is True:
            search_url = RELEASE + "?limit=" + limit + "&fuzzyOr=title%2C" + term + "%2CrenderedArtists%2C" + term
            release_raw = self.session.get(search_url)
            _release = release_raw.json()
            return _release
        elif use_skip is True:
            search_url = RELEASE + "?skip=" + skip + "&fuzzyOr=title%2C" + term + "%2CrenderedArtists%2C" + term
            release_raw = self.session.get(search_url)
            _release = release_raw.json()
            return _release
        else:
            search_url = RELEASE + "?fuzzyOr=title%2C" + term + "%2CrenderedArtists%2C" + term
            release_raw = self.session.get(search_url)
            _release = release_raw.json()
            return _release

    def artist(self, term, limit: str = None, skip: str = None, use_limit=False, use_skip=False):
        if use_limit and use_skip is True:
            search_url = ARTIST + "?limit=" + limit + "&skip=" + skip + "fuzzyOr=name%2C" + term
            artist_raw = self.session.get(search_url)
            _artist = artist_raw.json()
            return _artist
        elif use_limit is True:
            search_url = ARTIST + "?limit=" + limit + "fuzzyOr=name%2C" + term
            artist_raw = self.session.get(search_url)
            _artist = artist_raw.json()
            return _artist
        elif use_skip is True:
            search_url = ARTIST + "?skip=" + skip + "fuzzyOr=name%2C" + term
            artist_raw = self.session.get(search_url)
            _artist = artist_raw.json()
            return _artist
        else:
            search_url = ARTIST + "?fuzzyOr=name%2C" + term
            artist_raw = self.session.get(search_url)
            _artist = artist_raw.json()
            return _artist


class SearchAdvanced:
    def __init__(self, session):
        self.session = session

    def track(self, title: str, artists: str, limit: str = None, skip: str = None, use_limit=False, use_skip=False):
        if use_limit and use_skip is True:
            search_url = TRACK + "?limit=" + limit + \
                         "&skip=" + skip + "&fuzzy=title%2C" + title + "%2CartistsTitle%2C" + artists
            track_raw = self.session.get(search_url)
            _track = track_raw.json()
            return _track
        elif use_limit is True:
            search_url = TRACK + "?limit=" + limit + "&fuzzy=title%2C" + title + "%2CartistsTitle%2C" + artists
            track_raw = self.session.get(search_url)
            _track = track_raw.json()
            return _track
        elif use_skip is True:
            search_url = TRACK + "?skip=" + skip + "&fuzzy=title%2C" + title + "%2CartistsTitle%2C" + artists
            track_raw = self.session.get(search_url)
            _track = track_raw.json()
            return _track
        else:
            search_url = TRACK + "?fuzzy=title%2C" + title + "%2CartistsTitle%2C" + artists
            _track_raw = self.session.get(search_url)
            _track = _track_raw.json()
            return _track

    def release(self, title: str, artists: str, limit: str = None, skip: str = None, use_limit=False, use_skip=False):
        if use_limit and use_skip is True:
            search_url = RELEASE + "?limit=" + limit + \
                         "&skip=" + skip + "&fuzzy=title%2C" + title + "%2CrenderedArtists%2C" + artists
            release_raw = self.session.get(search_url)
            _release = release_raw.json()
            return _release
        elif use_limit is True:
            search_url = RELEASE + "?limit=" + limit + "&fuzzy=title%2C" + title + "%2CrenderedArtists%2C" + artists
            release_raw = self.session.get(search_url)
            _release = release_raw.json()
            return _release
        elif use_skip is True:
            search_url = RELEASE + "?skip=" + skip + "&fuzzy=title%2C" + title + "%2CrenderedArtists%2C" + artists
            release_raw = self.session.get(search_url)
            _release = release_raw.json()
            return _release
        else:
            search_url = RELEASE + "?fuzzy=title%2C" + title + "%2CrenderedArtists%2C" + artists
            release_raw = self.session.get(search_url)
            _release = release_raw.json()
            return _release

    def artist(self, term: str, limit: str = None, skip: str = None, use_limit=False, use_skip=False):
        if use_limit and use_skip is True:
            search_url = ARTIST + "?limit=" + limit + "&skip=" + skip + "fuzzy=name%2C" + term
            artist_raw = self.session.get(search_url)
            _artist = artist_raw.json()
            return _artist
        elif use_limit is True:
            search_url = ARTIST + "?limit=" + limit + "fuzzy=name%2C" + term
            artist_raw = self.session.get(search_url)
            _artist = artist_raw.json()
            return _artist
        elif use_skip is True:
            search_url = ARTIST + "?skip=" + skip + "fuzzy=name%2C" + term
            artist_raw = self.session.get(search_url)
            _artist = artist_raw.json()
            return _artist
        else:
            search_url = ARTIST + "?fuzzy=name%2C" + term
            artist_raw = self.session.get(search_url)
            _artist = artist_raw.json()
            return _artist
