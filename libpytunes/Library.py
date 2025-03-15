import logging
import plistlib
from six.moves.urllib import parse as urlparse
import datetime
import time

from libpytunes.Song import Song
from libpytunes.Playlist import Playlist


logger = logging.getLogger(__name__)

try:
    import xspf
    xspfAvailable = True
except ImportError:
    xspfAvailable = False
    pass


class Library:
    def __init__(self, itunesxml, musicPathXML=None, musicPathSystem=None, filesOnly=False):
        # musicPathXML and musicPathSystem will do path conversion
        # when xml is being processed on different OS then iTunes
        self.musicPathXML = musicPathXML
        self.musicPathSystem = musicPathSystem
        self.filesOnly = filesOnly
        with open(itunesxml, 'rb') as f:
            self.il = plistlib.load(f)
        self.songs = {}
        self.getSongs()

    def _ms_to_time_str(self, ms):
        return str(datetime.timedelta(milliseconds=ms))

    def getSongs(self):
        dt_format = r"%Y-%m-%d %H:%M:%S"
        for trackid, attributes in self.il['Tracks'].items():
            location = None
            location_escaped = None
            if attributes.get('Location'):
                location_escaped = attributes.get('Location')
                location = location_escaped
                location = urlparse.unquote(urlparse.urlparse(attributes.get('Location')).path)
                location = location
                if (self.musicPathXML is not None and self.musicPathSystem is not None):
                    location = location.replace(self.musicPathXML, self.musicPathSystem)
            
            s = Song(
                name = attributes.get('Name'),

                # Support classical music naming (Work+Movement Number+Movement Name) since iTunes 12.5
                work = attributes.get('Work'),
                movement_number = int(attributes.get('Movement Number')) if attributes.get('Movement Number') else None,
                movement_count = int(attributes.get('Movement Count')) if attributes.get('Movement Count') else None,
                movement_name = attributes.get('Movement Name'),

                track_id = int(attributes.get('Track ID')) if attributes.get('Track ID') else None,
                artist = attributes.get('Artist'),
                album_artist = attributes.get('Album Artist'),
                composer = attributes.get('Composer'),
                album = attributes.get('Album'),
                genre = attributes.get('Genre'),
                kind = attributes.get('Kind'),
                size = int(attributes.get('Size')) if attributes.get('Size') else None,
                total_time = self._ms_to_time_str(attributes.get('Total Time')) if attributes.get('Total Time') else None,
                start_time = self._ms_to_time_str(attributes.get('Start Time')) if attributes.get('Start Time') else None,
                stop_time = self._ms_to_time_str(attributes.get('Stop Time')) if attributes.get('Stop Time') else None,
                track_number = int(attributes.get('Track Number')) if attributes.get('Track Number') else None,
                track_count = int(attributes.get('Track Count')) if attributes.get('Track Count') else None,
                disc_number = int(attributes.get('Disc Number')) if attributes.get('Disc Number') else None,
                disc_count = int(attributes.get('Disc Count')) if attributes.get('Disc Count') else None,
                year = int(attributes.get('Year')) if attributes.get('Year') else None,
                date_modified = time.strptime(str(attributes.get('Date Modified')), dt_format) if attributes.get('Date Modified') else None,
                date_added = time.strptime(str(attributes.get('Date Added')), dt_format) if attributes.get('Date Added') else None,
                bit_rate = int(attributes.get('Bit Rate')) if attributes.get('Bit Rate') else None,
                sample_rate = int(attributes.get('Sample Rate')) if attributes.get('Sample Rate') else None,
                comments = attributes.get("Comments"),
                rating = int(attributes.get('Rating')) if attributes.get('Rating') else None,
                rating_computed = 'Rating Computed' in attributes,
                play_count = int(attributes.get('Play Count')) if attributes.get('Play Count') else None,
                album_rating = attributes.get('Album Rating'),
                album_rating_computed = 'Album Rating Computed' in attributes,
                persistent_id = attributes.get('Persistent ID'),

                compilation = 'Compilation' in attributes,
                lastplayed = time.strptime(str(attributes.get('Play Date UTC')), dt_format) if attributes.get('Play Date UTC') else None,
                skip_count = int(attributes.get('Skip Count')) if attributes.get('Skip Count') else None,
                skip_date = time.strptime(str(attributes.get('Skip Date')), dt_format) if attributes.get('Skip Date') else None,
                length = int(attributes.get('Total Time')) if attributes.get('Total Time') else None,
                
                track_type = attributes.get('Track Type'),
                grouping = attributes.get('Grouping'),
                podcast = 'Podcast' in attributes,
                movie = 'Movie' in attributes,
                has_video = 'Has Video' in attributes,
                loved = 'Loved' in attributes,
                album_loved = 'Album Loved' in attributes,
                playlist_only = 'Playlist Only' in attributes,
                apple_music = 'Apple Music' in attributes,
                protected = 'Protected' in attributes,
                disabled = 'Disabled' in attributes,
                release_date = time.strptime(str(attributes.get('Release Date')), dt_format) if attributes.get('Release Date') else None,
            
                location_escaped = location_escaped,
                location = location
            )

            self.songs[int(trackid)] = s

    def getPlaylistNames(self, ignoreList=[
        "Library", "Music", "Movies", "TV Shows", "Purchased", "iTunes DJ", "Podcasts"
    ]):
        playlists = []
        for playlist in self.il['Playlists']:
            if playlist['Name'] not in ignoreList:
                playlists.append(playlist['Name'])
        return playlists

    def getPlaylist(self, playlistName):
        for playlist in self.il['Playlists']:
            if playlist['Name'] == playlistName:
                # id 	playlist_id 	track_num 	url 	title 	album 	artist 	length 	uniqueid
                # breakpoint()
                p = Playlist(
                    name = playlistName,
                    playlist_id = playlist['Playlist ID'],
                    is_folder = playlist.get('Folder', False),
                    persistent_id = playlist.get('Playlist Persistent ID'),
                    parent_persistent_id = playlist.get('Parent Persistent ID'),
                    distinguished_kind = playlist.get('Distinguished Kind'),
                    is_genius_playlist = True if playlist.get('Genius Track ID') else False,
                    is_smart_playlist = True if playlist.get('Smart Info') and not playlist.get('Folder', False) else False
                )
                tracknum = 1
                # Make sure playlist was not empty
                if 'Playlist Items' in playlist:
                    for track in playlist['Playlist Items']:
                        id = int(track['Track ID'])
                        t = self.songs[id]
                        t.playlist_order = tracknum
                        tracknum += 1
                        p.tracks.append(t)
                return p

    def getPlaylistxspf(self, playlistName):
        global xspfAvailable
        if (xspfAvailable):
            x = xspf.Xspf()
            for playlist in self.il['Playlists']:
                if playlist['Name'] == playlistName:
                    x.title = playlistName
                    x.info = ""
                    for track in playlist['Playlist Items']:
                        id = int(track['Track ID'])
                        x.add_track(title=self.songs[id].name, creator="", location=self.songs[id].location)
                    return x.toXml()
        else:
            logger.warning("xspf library missing, go to https://github.com/alastair/xspf to install.")
            return None
