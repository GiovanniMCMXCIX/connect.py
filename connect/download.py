from .get import DownloadLink

import re


class Download:
    def __init__(self, session, path, album_Id, track_Id=None, audio_format="mp3 320", get_track=False):
        self.session = session
        self.url = None
        self.download(path, album_Id, track_Id, audio_format, get_track)

    def download(self, path, album_Id, track_Id, audio_format, get_track):
        chunk_size = 8192

        if get_track is False:
            if audio_format == "mp3 320":
                self.url = DownloadLink().release(album_Id=album_Id, mp3_320=True)
            elif audio_format == "mp3 128":
                self.url = DownloadLink().release(album_Id=album_Id, mp3_128=True)
            elif audio_format == "mp3 v0":
                self.url = DownloadLink().release(album_Id=album_Id, mp3_v0=True)
            elif audio_format == "mp3 v2":
                self.url = DownloadLink().release(album_Id=album_Id, mp3_v2=True)
            elif audio_format == "flac":
                self.url = DownloadLink().release(album_Id=album_Id, flac=True)
            elif audio_format == "wav":
                self.url = DownloadLink().release(album_Id=album_Id, wav=True)
        else:
            if audio_format == "mp3 320":
                self.url = DownloadLink().track(album_Id=album_Id, track_Id=track_Id, mp3_320=True)
            elif audio_format == "mp3 128":
                self.url = DownloadLink().track(album_Id=album_Id, track_Id=track_Id, mp3_128=True)
            elif audio_format == "mp3 v0":
                self.url = DownloadLink().track(album_Id=album_Id, track_Id=track_Id, mp3_v0=True)
            elif audio_format == "mp3 v2":
                self.url = DownloadLink().track(album_Id=album_Id, track_Id=track_Id, mp3_v2=True)
            elif audio_format == 'flac':
                self.url = DownloadLink().track(album_Id=album_Id, track_Id=track_Id, flac=True)
            elif audio_format == "wav":
                self.url = DownloadLink().track(album_Id=album_Id, track_Id=track_Id, wav=True)

        r = self.session.get(self.url, stream=True)
        filename = str.replace(re.findall("filename=(.+)", r.headers['content-disposition'])[0], "\"", "")
        full_path = path + "/" + filename

        with open(full_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
        return True
