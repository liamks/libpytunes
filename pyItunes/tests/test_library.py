import unittest
from pyItunes.Library import Library

class TestLibrary(unittest.TestCase):

    def test_read_library(self):

        it_library = Library("./Test Library.xml")
        
        for id, song in it_library.songs.items():
            assert(hasattr(song, 'name') == True)
            
        playlists = it_library.getPlaylistNames()

        for song in it_library.getPlaylist(playlists[0]).tracks:
            assert(hasattr(song, 'track_number'))
            assert(hasattr(song, 'artist'))
            assert(hasattr(song, 'name'))

if __name__ == '__main__':
    unittest.main()