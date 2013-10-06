pyItunes
Created by Liam Kaufman (liamkaufman.com)
Contributors by Liam Kaufman (liamkaufman.com), Steven Miller (copart), dpchu, selftext, z4r, pschorf
Date: October 5th 2013
Version 0.2


Before using pyItunes it is recommended that you backup your Itunes Library XML file. Use pyItunes at your own risk, there is no guarantee that it works or will not blow-up your computer!

Usage:
========
#DEPRECIATED LEGACY METHOD, still works for now
from pyItunes import *

pl = XMLLibraryParser("iTunes Music Library.xml")
l = Library(pl.dictionary)

for song in l.songs:
	if song.rating > 80:
		print song.name

#NEW since 0.2, aads ability to get playlists, however, the songs dictionary is keyed on TrackID (as codes in iTunes xml)

from pyItunes import *

l = Library("iTunes Music Library.xml")

for id,song in l.songs.items():
	if song.rating > 80:
		print song.name

playlists=l.getPlaylistNames()

for song in l.getPlaylist(playlists[0]).tracks:
	print "[%d] %s - %s" % (song.number,song.artist,song.name)


=======

Attributes of the Song class:
Song Attributes:
name (String)
artist (String)
album_artist (String)
composer = None (String)
album = None (String)
genre = None (String)
kind = None (String)
size = None (Integer)
total_time = None (Integer)
track_number = None (Integer)
year = None (Integer)
date_modified = None (Time)
date_added = None (Time)
bit_rate = None (Integer)
sample_rate = None (Integer)
comments = None (String)
rating = None (Integer)
album_rating = None (Integer)
play_count = None (Integer)
location = None (String)
compilation = None (Boolean)
grouping = None (String)
lastplayed = None (Time)
length = None (Integer)
