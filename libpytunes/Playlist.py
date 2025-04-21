from dataclasses import dataclass, field

from .Song import Song

@dataclass(kw_only=True)
class Playlist:
    is_folder: bool = False
    persistent_id: int = None
    parent_persistent_id: int = None
    distinguished_kind: str = None
    playlist_id: int = None
    name: str = None

    is_genius_playlist: bool = False
    is_smart_playlist: bool = False

    tracks: list[Song] = field(default_factory=lambda: [])
