from pyItunes.Song import Song
from pyItunes.Playlist import Playlist
import time
import plistlib
from six.moves.urllib import parse as urlparse
from six import PY2
import urllib
import logging

logger = logging.getLogger(__name__)

try:
	import xspf
	xspfAvailable = True
except ImportError:
	xspfAvailable = False
	pass

class Library:
	def __init__(self,itunesxml,musicPathXML=None,musicPathSystem=None,filesOnly=False):
		#musicPathXML and musicPathSystem will do path conversion for when xml is being processed on different OS then iTunes
		self.musicPathXML = musicPathXML
		self.musicPathSystem = musicPathSystem
		self.filesOnly = filesOnly
		if type(itunesxml) == str:
			self.il = plistlib.readPlist(itunesxml) #Much better support of xml special characters
			self.legacymode = False
			self.songs = {}
		else:
			self.il = {}
			self.il['Tracks'] = itunesxml
			self.legacymode = True
			self.songs = []
		self.getSongs()

	def getSongs(self):
		format = "%Y-%m-%d %H:%M:%S"
		for trackid,attributes in self.il['Tracks'].items():
			s = Song()
			s.name = attributes.get('Name')
			s.track_id = int(attributes.get('Track ID'))
			s.artist = attributes.get('Artist')
			s.album_artist = attributes.get('Album Artist')
			s.composer = attributes.get('Composer')
			s.album = attributes.get('Album')
			s.genre = attributes.get('Genre')
			s.kind = attributes.get('Kind')
			if attributes.get('Size'):
				s.size = int(attributes.get('Size'))
			s.total_time = attributes.get('Total Time')
			s.track_number = attributes.get('Track Number')
			if attributes.get('Track Count'):
				s.track_count = int(attributes.get('Track Count'))
			if attributes.get('Disc Number'):
				s.disc_number = int(attributes.get('Disc Number'))
			if attributes.get('Disc Count'):
				s.disc_count = int(attributes.get('Disc Count'))
			if attributes.get('Year'):
				s.year = int(attributes.get('Year'))
			if attributes.get('Date Modified'):
				s.date_modified = time.strptime(str(attributes.get('Date Modified')),format)
			if attributes.get('Date Added'):
				s.date_added = time.strptime(str(attributes.get('Date Added')),format)
			if attributes.get('Bit Rate'):
				s.bit_rate = int(attributes.get('Bit Rate'))
			if attributes.get('Sample Rate'):
				s.sample_rate = int(attributes.get('Sample Rate'))
			s.comments = attributes.get("Comments")
			if attributes.get('Rating'):
				s.rating = int(attributes.get('Rating'))
			s.rating_computed = 'Rating Computed' in attributes
			if attributes.get('Play Count'):
				s.play_count = int(attributes.get('Play Count'))
			if attributes.get('Location'):
				s.location = attributes.get('Location')
				s.location = urlparse.unquote(urlparse.urlparse(attributes.get('Location')).path[1:])
				s.location = s.location.decode('utf-8') if PY2 else s.location # fixes bug #19
				if ( self.musicPathXML is not None and self.musicPathSystem is not None ):
					s.location = s.location.replace(self.musicPathXML,self.musicPathSystem)
			s.compilation = 'Compilation' in attributes
			if attributes.get('Play Date UTC'):
				s.lastplayed = time.strptime(str(attributes.get('Play Date UTC')),format)
			if attributes.get('Skip Count'):
				s.skip_count = int(attributes.get('Skip Count'))
			if attributes.get('Skip Date'):
				s.skip_date = time.strptime(str(attributes.get('Skip Date')),format)
			if attributes.get('Total Time'):
				s.length = int(attributes.get('Total Time'))
			if attributes.get('Grouping'):
				s.grouping = attributes.get('Grouping')
			if self.filesOnly==True and attributes.get('Track Type') == 'File':
				if self.legacymode:
					self.songs.append(s)
				else:
					self.songs[int(trackid)] = s
			elif self.filesOnly==False:
				if self.legacymode:
					self.songs.append(s)
				else:
					self.songs[int(trackid)] = s

	def getPlaylistNames(self,ignoreList=("Library","Music","Movies","TV Shows","Purchased","iTunes DJ","Podcasts")):
		if (self.legacymode):
			logger.info("getPlaylistNames is disabled in legacy mode.")
			return []
		else:
			playlists = []
			for playlist in self.il['Playlists']:
				if playlist['Name'] not in ignoreList:
					playlists.append(playlist['Name'])
			return playlists

	def getPlaylist(self,playlistName):
		if (self.legacymode):
			logger.info("getPlaylist is disabled in legacy mode.")
			return Playlist(playlistName)
		else:
			for playlist in self.il['Playlists']:
				if playlist['Name'] == playlistName:
					#id 	playlist_id 	track_num 	url 	title 	album 	artist 	length 	uniqueid
					p = Playlist(playlistName)
					p.is_folder = True if 'Folder' in playlist and playlist['Folder'] == True else False
					if 'Playlist Persistent ID' in playlist:
						p.playlist_persistent_id = playlist['Playlist Persistent ID']
					if 'Parent Persistent ID' in playlist:
						p.parent_persistent_id = playlist['Parent Persistent ID']
					tracknum=1
					#Make sure playlist was not empty
					if 'Playlist Items' in playlist:
						for track in playlist['Playlist Items']:
							id=int(track['Track ID'])
							t = self.songs[id]
							t.playlist_order = tracknum
							tracknum+=1
							p.tracks.append(t)
					return p

	def getPlaylistxspf(self,playlistName):
		global xspfAvailable
		if ( xspfAvailable ):
			x = xspf.Xspf()
			for playlist in self.il['Playlists']:
				if playlist['Name'] == playlistName:
					x.title = playlistName
					x.info = ""
					for track in playlist['Playlist Items']:
						id=int(track['Track ID'])
						x.add_track(title=self.songs[id].name, creator="",location=self.songs[id].location)
					return x.toXml()
		else:
			logger.warning("xspf library missing, go to https://github.com/alastair/xspf to install.")
			return None
