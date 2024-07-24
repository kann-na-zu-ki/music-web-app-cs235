from sqlalchemy import select, inspect

from music.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['albums', 'artists', 'genres', 'playlists', 'reviews', 'track_genre', 'track_playlist', 'tracks',  'users']

def test_database_populate_select_all_tracks(database_engine):
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables['tracks']])
        result = connection.execute(select_statement)

        tracks = []
        for row in result:
            tracks.append((row['track_id'], row['title']))

        print(tracks)

        nr_tracks = len(tracks)
        assert nr_tracks == 10

def test_database_populate_select_all_artists(database_engine):
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables['artists']])
        result = connection.execute(select_statement)

        artists = []
        for row in result:
            artists.append((row['artist_id'], row['full_name']))

        print(artists)

        nr = len(artists)
        assert nr == 5

def test_database_populate_select_all_albums(database_engine):
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables['albums']])
        result = connection.execute(select_statement)

        albums = []
        for row in result:
            albums.append((row['album_id'], row['title']))

        print(albums)

        nr = len(albums)
        assert nr == 5

def test_database_populate_select_all_genres(database_engine):
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables['genres']])
        result = connection.execute(select_statement)

        genres = []
        for row in result:
            genres.append((row['genre_id'], row['genre_name']))

        print(genres)

        nr = len(genres)
        assert nr == 7

def test_database_populate_select_all_playlists(database_engine):
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables['playlists']])
        result = connection.execute(select_statement)
        playlists = []
        for row in result:
            playlists.append((row['playlist_id'], row['name']))

        print(playlists)

        nr = len(playlists)
        assert nr == 1
