import pytest

import datetime

from sqlalchemy.exc import IntegrityError
from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList
def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def test_loading_of_users(empty_session):
    insert_user(empty_session)
    expected = [
        User(1, "andrew", "1234"),
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session)
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User(2, "andrew", "111")
        empty_session.add(user)
        empty_session.commit()

def insert_track(empty_session):
    empty_session.execute(
        'INSERT INTO tracks(title, track_duration, track_url, artist_id, album_id) VALUES '
        '("Food", '
        '168, '
        '"http://freemusicarchive.org/music/AWOL/AWOL_-_A_Way_Of_Life/Food", '
        '1, '
        '1)'
    )
    row = empty_session.execute('SELECT track_id from tracks').fetchone()
    return row[0]

def insert_track_genre_associations(empty_session, track_key, genre_keys):
    stmt = 'INSERT INTO track_genre (track_id, genre_id) VALUES (:track_id, :genre_id)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {'track_id': track_key, 'genre_id': genre_key})

def test_loading_track(empty_session):
    track_key = insert_track(empty_session)
    expected_track = Track(1, "Food")
    fetched_track = empty_session.query(Track).one()
    assert expected_track == fetched_track
    assert track_key == fetched_track.track_id

def test_saving_of_track(empty_session):
    track = Track(1, 'Food')
    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT track_id, title FROM tracks'))
    assert rows == [(1, 'Food')]

def test_saving_of_album(empty_session):
    album = Album(4, 'Niris')
    empty_session.add(album)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT album_id, title FROM albums'))
    assert rows == [(4, 'Niris')]

def test_saving_of_artist(empty_session):
    artist = Artist(2, 'ME')
    empty_session.add(artist)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT artist_id, full_name FROM artists'))
    assert rows == [(2, 'ME')]

def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (genre_id, genre_name) VALUES(1, "Rock"), (2, "Pop")'
    )
    rows = list(empty_session.execute('SELECT genre_id from genres'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_track_genre_associations(empty_session, track_key, genre_keys):
    stmt = 'INSERT INTO track_genre (track_id, genre_id) VALUES (:track_id, :genre_id)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {'track_id': track_key, 'genre_id': genre_key})

def test_loading_of_genred_track(empty_session):
    track_key = insert_track(empty_session)
    genre_keys = insert_genres(empty_session)
    insert_track_genre_associations(empty_session, track_key, genre_keys)

    track = empty_session.query(Track).get(track_key)
    genres = [empty_session.query(Genre).get(key) for key in genre_keys]

    for genre in genres:
        assert track.is_genred_by(genre)

def test_saving_of_review(empty_session):
    track_key = insert_track(empty_session)

    rows = empty_session.query(Track).all()
    track = rows[0]

    review = Review(track, 'good song', 5)

    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT track_id, review_text FROM reviews'))

    assert rows == [(track_key, 'good song')]

def insert_playlist(empty_session):
    empty_session.execute(
        'INSERT INTO playlists (name) VALUES ("mylist")'
    )
    row = list(empty_session.execute('SELECT playlist_id FROM playlists'))
    return row[0]

def test_saving_of_playlist(empty_session):
    insert_playlist(empty_session)

    rows = list(empty_session.execute('SELECT name FROM playlists'))
    playlist = rows[0]

    assert playlist == ('mylist',)


