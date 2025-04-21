![Travis CI Master branch](https://travis-ci.org/liamks/libpytunes.svg?branch=master)

# libpytunes

Created by Liam Kaufman (liamkaufman.com)

Contributions by Liam Kaufman (liamkaufman.com), Steven Miller (copart), dpchu, selftext, z4r, pschorf, Mathew Bramson (mbramson), Roger Filmyer (rfilmyer), cktse, Scot Hacker (shacker)

**Before using libpytunes it is recommended that you backup your Itunes Library XML file. Use libpytunes at your own risk - there is no guarantee that it works or will not blow-up your computer!**

If you don't see an .xml library file in `~/Music/iTunes`, you probably started using iTunes after version 12.2, and have never enabled sharing between iTunes and other apps. To generate one, go to iTunes Preferences | Advanced and select "Share iTunes Library XML with other applications." ([Apple docs](https://support.apple.com/en-us/HT201610))

## Installation
To install the libpytunes library, follow these steps:

1. Clone the repository:
```
git clone https://github.com/liamks/libpytunes.git
```
2. Navigate to the project directory:
```
cd libpytunes
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Install the library:
```
python setup.py install
```
These steps will install the library libpytunes using github page repository and can be used through imports in python projects

## Usage:

```
from libpytunes import Library

l = Library("/path/to/iTunes Library.xml")

for id, song in l.songs.items():
    if song and song.rating:
        if song.rating > 80:
            print(song.name, song.rating)

playlists=l.getPlaylistNames()

for song in l.getPlaylist(playlists[0]).tracks:
	print("[{t}] {a} - {n}".format(t=song.track_number, a=song.artist, n=song.name))
```

See below for available song attributes.

If your library is very large, reading the XML into memory could be quite slow. If you need to access the library repeatedly, Python's "pickle" can save a binary representation of the XML object to disk for much faster access (up to 10x faster). To use a pickled version, do something like this:

```
import os.path
import pickle
import time
from libpytunes import Library

lib_path = "/Users/[username]/Music/iTunes/iTunes Library.xml"
pickle_file = "itl.p"
expiry = 60 * 60  # Refresh pickled file if older than
epoch_time = int(time.time())  # Now

# Generate pickled version of database if stale or doesn't exist
if not os.path.isfile(pickle_file) or os.path.getmtime(pickle_file) + expiry < epoch_time:
    itl_source = Library(lib_path)
    pickle.dump(itl_source, open(pickle_file, "wb"))

itl = pickle.load(open(pickle_file, "rb"))

for id, song in itl.songs.items():
    if song and song.rating:
        if song.rating > 80:
            print("{n}, {r}".format(n=song.name, r=song.rating))
```

## Notes

Track counts may not match those shown in iTunes. e.g. This may report a higher number than the song count shown in iTunes itself. :

```
l = Library("iTunes Library.xml")
len(l.songs)
```

This is because iTunes does not count things like Podcasts and Voice Memos as "Music," whereas libpytunes counts **all** tracks.

The songs dictionary is keyed on TrackID (as coded in iTunes xml). Playlists are lists of Song objects, with their order noted as a `playlist_order` attribute.

### Attributes of the Song class:

```
name: str = None
track_id: int = None
artist: str = None
album_artist: str = None
composer: str = None
album: str = None
genre: str = None
kind: str = None
size: int = None
total_time: int = None
start_time: int = None
stop_time: int = None
track_number: int = None
track_count: int = None
disc_number: int = None
disc_count: int = None
year: int = None
date_modified: str = None  # (Time)
date_added: str = None  # (Time)
bit_rate: int = None
sample_rate: int = None
comments: str = None
rating: int = None
rating_computed: bool = False
album_rating: int = None
play_count: int = None
skip_count: int = None
skip_date: str = None  # (Time)
location: str = None
location_escaped: str = None
compilation: bool = False
grouping: str = None
lastplayed: str = None  # (Time)
length: int = None
track_type: str = None
podcast: bool = False
movie: bool = False
has_video: bool = False
loved: bool = False
album_loved: bool = False
persistent_id: str = None
album_rating_computed: bool = False
work: str = None
movement_name: str = None
movement_number: int = None
movement_count: int = None
playlist_only: bool = None
apple_music: bool = None
protected: bool = None
disabled: bool = False
release_date: str = None  # (Time)
```

Songs retrieved as part of a playlist have an additional attribute:
```
playlist_order = None (Integer)
```


Song object attributes can be iterated through like this:
```
for key, value in SongItem:
	<interact with specific key,value pair>.
```


### Attributes of the Playlist class:
```
is_folder: bool = False
persistent_id: int = None
parent_persistent_id: int = None
distinguished_kind = None
playlist_id: int = None
name: str = None

is_genius_playlist: bool = False
is_smart_playlist: bool = False

tracks: list[Song] = []
```

### Legacy Mode
Support for `legacymode` has been removed with version 1.5
