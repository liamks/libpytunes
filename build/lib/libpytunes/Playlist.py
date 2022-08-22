from six import iteritems

class Playlist:
    is_folder = False
    playlist_persistent_id = None
    parent_persistent_id = None
    distinguished_kind = None
    playlist_id = None

    def __init__(self, playListName=None):
        self.name = playListName
        self.tracks = []

    def __iter__(self):
        for attr, value in iteritems(self.__dict__):
            yield attr, value

    def ToDict(self):
        return {key: value for (key, value) in self}
