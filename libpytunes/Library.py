import logging
import plistlib
from six import PY2
from six.moves.urllib import parse as urlparse
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
        self.il = plistlib.readPlist(itunesxml)  # Much better support of xml special characters
        self.songs = {}
        self.getSongs()

    def getSongs(self):
        format = "%Y-%m-%d %H:%M:%S"
        for trackid, attributes in self.il['Tracks'].items():
            s = Song()
            s.name = attributes.get('Name')

            # Support classical music naming (Work+Movement Number+Movement Name) since iTunes 12.5
            s.work = attributes.get('Work')
            s.movement_number = attributes.get('Movement Number')
            s.movement_count = attributes.get('Movement Count')
            s.movement_name = attributes.get('Movement Name')

            s.track_id = int(attributes.get('Track ID')) if attributes.get('Track ID') else None
            s.artist = attributes.get('Artist')
            s.album_artist = attributes.get('Album Artist')
            s.composer = attributes.get('Composer')
            s.album = attributes.get('Album')
            s.genre = attributes.get('Genre')
            s.kind = attributes.get('Kind')
            s.size = int(attributes.get('Size')) if attributes.get('Size') else None
            s.total_time = attributes.get('Total Time')
            s.track_number = attributes.get('Track Number')
            s.track_count = int(attributes.get('Track Count')) if attributes.get('Track Count') else None
            s.disc_number = int(attributes.get('Disc Number')) if attributes.get('Disc Number') else None
            s.disc_count = int(attributes.get('Disc Count')) if attributes.get('Disc Count') else None
            s.year = int(attributes.get('Year')) if attributes.get('Year') else None
            s.date_modified = time.strptime(str(attributes.get('Date Modified')), format) if attributes.get('Date Modified') else None
            s.date_added = time.strptime(str(attributes.get('Date Added')), format) if attributes.get('Date Added') else None
            s.bit_rate = int(attributes.get('Bit Rate')) if attributes.get('Bit Rate') else None
            s.sample_rate = int(attributes.get('Sample Rate')) if attributes.get('Sample Rate') else None
            s.comments = attributes.get("Comments")
            s.rating = int(attributes.get('Rating')) if attributes.get('Rating') else None
            s.rating_computed = 'Rating Computed' in attributes
            s.play_count = int(attributes.get('Play Count')) if attributes.get('Play Count') else None
            s.album_rating = attributes.get('Album Rating')
            s.album_rating_computed = 'Album Rating Computed' in attributes
            s.persistent_id = attributes.get('Persistent ID')

            if attributes.get('Location'):
                s.location_escaped = attributes.get('Location')
                s.location = s.location_escaped
                s.location = urlparse.unquote(urlparse.urlparse(attributes.get('Location')).path[1:])
                s.location = s.location.decode('utf-8') if PY2 else s.location  # fixes bug #19
                if (self.musicPathXML is not None and self.musicPathSystem is not None):
                    s.location = s.location.replace(self.musicPathXML, self.musicPathSystem)

            s.compilation = 'Compilation' in attributes
            s.lastplayed = time.strptime(str(attributes.get('Play Date UTC')), format) if attributes.get('Play Date UTC') else None
            s.skip_count = int(attributes.get('Skip Count')) if attributes.get('Skip Count') else None
            s.skip_date = time.strptime(str(attributes.get('Skip Date')), format) if attributes.get('Skip Date') else None
            s.length = int(attributes.get('Total Time')) if attributes.get('Total Time') else None
            s.track_type = attributes.get('Track Type')
            s.grouping = attributes.get('Grouping')
            s.podcast = 'Podcast' in attributes
            s.movie = 'Movie' in attributes
            s.has_video = 'Has Video' in attributes
            s.loved = 'Loved' in attributes
            s.album_loved = 'Album Loved' in attributes

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
                p = Playlist(playlistName)
                p.is_folder = True if 'Folder' in playlist and playlist['Folder'] else False
                if 'Playlist Persistent ID' in playlist:
                    p.playlist_persistent_id = playlist['Playlist Persistent ID']
                if 'Parent Persistent ID' in playlist:
                    p.parent_persistent_id = playlist['Parent Persistent ID']
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
