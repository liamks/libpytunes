from pyItunes.Song import Song
import time
import plistlib
import urlparse
import time

class Library:
	def __init__(self,itunesxml,keyByTrackID=False,musicPathXML=None,musicPathSystem=None):
		if type(itunesxml) == str:
			self.il = plistlib.readPlist(itunesxml) #Much better support of xml special characters
		else:
			self.il = {}
			self.il['Tracks'] = itunesxml
		self.keyByTrackID = keyByTrackID
		if keyByTrackID:
			self.songs = {}
		else:
			self.songs = []
		self.musicPathXML = musicPathXML
		self.musicPathSystem = musicPathSystem
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
					s.location = urlparse.unquote(urlparse.urlparse(attributes.get('Location')).path[1:])
				else:
					s.location = urlparse.unquote(urlparse.urlparse(attributes.get('Location')).path[1:]).replace(self.musicPathXML,self.musicPathSystem)
			s.compilation = 'Compilation' in attributes
			if attributes.get('Play Date UTC'):
				s.lastplayed = time.strptime(str(attributes.get('Play Date UTC')),format)
			if attributes.get('Total Time'):
				s.length = int(attributes.get('Total Time'))
			if attributes.get('Grouping'):
				s.grouping = attributes.get('Grouping')
			if self.keyByTrackID:
				self.songs[trackid] = s
			else:
				self.songs.append(s)
