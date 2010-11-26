pyItunes
created by Liam Kaufman
liamkaufman.com
Date: March 15th 2009
Version 0.1


Before using pyItunes it is recommended that you backup your Itunes Library XML file. Use pyItunes at your own risk, there is no guarantee that it works or will not blow-up your computer!

Usage:
========
from pyItunes import *

pl = XMLLibraryParser("iTunes Music Library.xml")
l = Library(pl.dictionary)

for song in l.songs:
	if song.rating > 80:
		print song.name
	
=======

Attributes of the Song class:
Song Attributes:
name (String)
artist (String)
album_arist (String)
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
