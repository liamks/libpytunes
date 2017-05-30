from six import iteritems


class Song:
    """
    Song Attributes:
    name (String)
    track_id (Integer)
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
    rating_computed = False (Boolean)
    album_rating = None (Integer)
    play_count = None (Integer)
    location = None (String)
    location_escaped = None (String)
    compilation = False (Boolean)
    grouping = None (String)
    lastplayed = None (Time)
    skip_count = None (Integer)
    skip_date = None (Time)
    length = None (Integer)
    persistent_id = None (String)
    album_rating_computed = False (Boolean)
    work = None (String)
    movement_name = None (String)
    movement_number = None (Integer)
    movement_count = None (Integer)
    """
    name = None
    track_id = None
    artist = None
    album_artist = None
    composer = None
    album = None
    genre = None
    kind = None
    size = None
    total_time = None
    track_number = None
    track_count = None
    disc_number = None
    disc_count = None
    year = None
    date_modified = None
    date_added = None
    bit_rate = None
    sample_rate = None
    comments = None
    rating = None
    rating_computed = None
    album_rating = None
    play_count = None
    skip_count = None
    skip_date = None
    location = None
    location_escaped = None
    compilation = None
    grouping = None
    lastplayed = None
    length = None
    persistent_id = None
    album_rating_computed = None
    work = None
    movement_name = None
    movement_number = None
    movement_count = None

    def __iter__(self):
        for attr, value in iteritems(self.__dict__):
            yield attr, value

    def ToDict(self):
        return {key: value for (key, value) in self}
