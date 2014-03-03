from pyItunes.Song import Song
from pyItunes.Playlist import Playlist,PlTrack
import time
import plistlib
import urlparse
import time
import urllib

try:
	import xspf
	xspfAvailable = True
except ImportError:
	xspfAvailable = False
	pass

class Library:
	def __init__(self,itunesxml,musicPathXML=None,musicPathSystem=None):
		#musicPathXML and musicPathSystem will do path conversion for when xml is being processed on different OS then iTunes
		self.musicPathXML = musicPathXML
		self.musicPathSystem = musicPathSystem
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
		for trackid,attributes in self.il['Tracks'].iteritems():
			s = Song()
			s.name = attributes.get('Name')
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
			s.comments = attributes.get("Comments	")
			if attributes.get('Rating'):
				s.rating = int(attributes.get('Rating'))
			if attributes.get('Play Count'):
				s.play_count = int(attributes.get('Play Count'))
			if attributes.get('Location'):
				if ( self.musicPathXML is None or self.musicPathSystem is None ):
					s.location = unicode(urlparse.unquote(urlparse.urlparse(attributes.get('Location')).path[1:]),"utf8")
				else:
					s.location = unicode(urlparse.unquote(urlparse.urlparse(attributes.get('Location')).path[1:]).replace(self.musicPathXML,self.musicPathSystem),"utf8")
			s.compilation = 'Compilation' in attributes
			if attributes.get('Play Date UTC'):
				s.lastplayed = time.strptime(str(attributes.get('Play Date UTC')),format)
			if attributes.get('Total Time'):
				s.length = int(attributes.get('Total Time'))
			if attributes.get('Grouping'):
				s.grouping = attributes.get('Grouping')
			if self.legacymode:
				self.songs.append(s)
			else:
				self.songs[int(trackid)] = s
	
	def getPlaylistNames(self,ignoreList=("Library","Music","Movies","TV Shows","Purchased","iTunes DJ","Podcasts")):
		if (self.legacymode):
			print "getPlaylistNames is disabled in legacy mode."
			return []
		else:
			playlists = []
			for playlist in self.il['Playlists']:
				if playlist['Name'] not in ignoreList:
					playlists.append(playlist['Name'])
			return playlists
	
	def getPlaylist(self,playlistName):
		if (self.legacymode):
			print "getPlaylist is disabled in legacy mode."
			return Playlist(playlistName)
		else:
			for playlist in self.il['Playlists']:
				if playlist['Name'] == playlistName:
					#id 	playlist_id 	track_num 	url 	title 	album 	artist 	length 	uniqueid
					p = Playlist(playlistName)
					tracknum=1
					#Make sure playlist was not empty
					if 'Playlist Items' in playlist:
						for track in playlist['Playlist Items']:
							id=int(track['Track ID'])
							t = PlTrack()
							t.number = tracknum
							t.name = self.songs[id].name
							t.artist = self.songs[id].artist
							t.album = self.songs[id].album
							t.length = self.songs[id].length
							t.location = self.songs[id].location
							#album
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
			print "xspf library missing, go to https://github.com/alastair/xspf to install."
			return None

