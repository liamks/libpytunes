from dataclasses import dataclass

@dataclass(eq=True, kw_only=True)
class Song:
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

    def __repr__(self):
        return f'Song(name={self.name!r}, artist={self.artist!r}, track_id={self.track_id!r})'
