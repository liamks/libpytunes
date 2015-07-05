# pyItunes

Created by Liam Kaufman (liamkaufman.com)

Contributions by Liam Kaufman (liamkaufman.com), Steven Miller (copart), dpchu, selftext, z4r, pschorf, Mathew Bramson (mbramson), Roger Filmyer (rfilmyer)

**Before using pyItunes it is recommended that you backup your Itunes Library XML file. Use pyItunes at your own risk - there is no guarantee that it works or will not blow-up your computer!**

## Usage:

```
from pyItunes import *

l = Library("iTunes Music Library.xml")

for id, song in l.songs.items():
	if song.rating > 80:
		print song.name

playlists=l.getPlaylistNames()

for song in l.getPlaylist(playlists[0]).tracks:
	print "[%d] %s - %s" % (song.number, song.artist, song.name)
```

See below for available song attributes.

There is also a deprecated legacy method, which still works for now:

```
from pyItunes import *

pl = XMLLibraryParser("iTunes Music Library.xml")
l = Library(pl.dictionary)

for song in l.songs:
	if song.rating > 80:
		print song.name
```


## Notes

Track counts may not match those shown in iTunes. e.g.:

```
l = Library("iTunes Music Library.xml")
len(l.songs)
```

May report a higher number than the song count shown in iTunes itself. This is because
iTunes does not count things like Podcasts and Voice Memos as "Music," whereas
pyitunes counts **all** tracks.

Version 0.2 adds the ability to get playlists. However, the songs dictionary is keyed on TrackID (as coded in iTunes xml).
Playlists are lists of Song objects, with their order noted as a `playlist_order` attribute.
(note that previously, playlists were lists of PlTrack objects, with their order noted as a `number` attribute. 
PlTracks have been removed in favor of modified Songs.)

### Attributes of the Song class:

```
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
track_count = None (Integer)
disc_number = None (Integer)
disc_count = None (Integer)
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
```

Songs retrieved as part of a playlist have an additional attribute:
```
playlist_order = None (Integer)
```


Song object attributes can be iterated through like this:
```
for key,value in SongItem:
	<interact with specific key,value pair>.
```

You can also convert songs directly to Dictionaries with the ToDict() Method.
```
SongDictionary = SongItem.ToDict()
```