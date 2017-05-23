class Playlist:
    def __init__(self, playListName=None):
        self.name = playListName
        self.tracks = []
        self.is_folder = False
        self.playlist_persistent_id = None
        self.parent_persistent_id = None
