class PlTrack:
	location = None
	name = None
	artist = None
	length = None
	number = None
	album = None
	
class Playlist:
	name = None
	tracks = []
	def __init__(self,playListName=None):
		self.name = playListName

