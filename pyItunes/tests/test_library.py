import unittest
from libpytunes.Library import Library

class TestLibrary(unittest.TestCase):

    def setUp(self):

        self.it_library = Library("./Test Library.xml")

    def test_songs(self):

        for id, song in self.it_library.songs.items():
            assert(hasattr(song, 'name') == True)

    def test_playlists(self):

        playlists = self.it_library.getPlaylistNames()

        for song in self.it_library.getPlaylist(playlists[0]).tracks:
            assert(hasattr(song, 'track_number'))
            assert(hasattr(song, 'artist'))
            assert(hasattr(song, 'name'))

if __name__ == '__main__':
    unittest.main()
