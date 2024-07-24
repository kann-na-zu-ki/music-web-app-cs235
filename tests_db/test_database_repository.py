from datetime import date, datetime

import pytest

import music.adapters.repository as repo
from music.adapters.database_repository import SqlAlchemyRepository
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList
from music.adapters.repository import RepositoryException

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User(2, 'Martin', '123456789'))

    user2 = repo.get_user('dave') 

    assert user2 == user and user2 is user

def test_repository_can_add_a_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = Track(0, 'Test Title')
    track.track_duration = 340
    track.track_url = 'website.com'
    track.album = Album(0, 'Album')
    repo.add_track(track)

    result = repo.get_track(0)

    assert track == result

def test_repository_can_add_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    a = Artist(0, 'Test Artist')
    repo.add_artist(a)
    result = repo.get_artist(0)
    assert a == result

def test_repository_can_get_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    track = repo.get_track(2)
    assert track.title == 'Food'
    assert track.artist.full_name == 'AWOL'

def test_repository_can_get_artists(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    artists = repo.get_artists()
    assert len(artists) == 5

def test_repository_can_get_albums(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    albums = repo.get_albums()
    assert len(albums) == 5

def test_repository_can_add_album(session_factory):
    a = Album(66, 'Test Album')
    repo = SqlAlchemyRepository(session_factory)
    repo.add_album(a)
    result = repo.get_album(66)
    assert a == result

def test_search_tracks(session_factory):
    searchstring = 'food'
    repo = SqlAlchemyRepository(session_factory)
    track = repo.get_track(2)
    result = repo.search_tracks(searchstring)
    assert [track] == result

def test_get_tracks(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    result = repo.get_tracks()
    assert len(result) == 10

def test_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    track = repo.get_track(1)
    review = Review(track, 'good song',5)
    repo.add_review(review)
    result = repo.get_reviews()
    assert review in result

def test_add_playlist_and_get_playlist_and_get_playlists(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    t1 = repo.get_track(2)
    t2 = repo.get_track(3)
    p = PlayList(1, 'Test Playlist')
    p.add_track(t1)
    p.add_track(t2)
    repo.add_playlist(p)
    assert p == repo.get_playlist(1)
    assert len(repo.get_playlist(1).tracks) == 2
    assert len(repo.get_playlists()) == 2

def test_empty_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    p = PlayList(1, 'Test Playlist')
    repo.add_playlist(p)
    result = repo.get_playlist(1)
    assert p == result
    assert result.tracks == []

def test_create_random_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    p = repo.create_random_playlist(10)
    assert repo.get_playlist(1) == p

def test_add_track_to_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    p = PlayList(1, 'Test Playlist')
    t1 = repo.get_track(2)

    repo.add_playlist(p)
    repo.add_track_to_playlist(p.playlist_id, t1.track_id)
    
    result = repo.get_playlist(1)
    assert len(result.tracks)==1

def test_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    p = PlayList(1, 'Test Playlist')
    t1 = repo.get_track(2)
    r = Review(t1, 'Test Review', 5)
    repo.add_review(r)
    result = repo.get_reviews(t1)
    assert [r] == result
def test_get_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User(1, 'Dave', '123456789')
    repo.add_user(user)
    user_get = repo.get_user('dave')
    assert user == user_get

def test_get_number_of_tracks(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    tracks_number = repo.get_number_of_tracks()
    assert tracks_number == 10

def test_get_tracks_by_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    artist = Artist(1, 'AWOL')
    tracks = repo.get_tracks_by_artist(artist)
    assert len(tracks) == 4

def test_get_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    artist = repo.get_artist(1)
    assert artist == Artist(1, 'AWOL')

def test_add_genre_and_get_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genre = Genre(0, 'MyGenre')
    repo.add_genre(genre)
    assert genre in repo.get_genres()

def test_get_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    album = Album(0, 'MyAlbum')
    repo.add_album(album)
    assert album == repo.get_album(0)

def test_get_number_of_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genres_number = repo.get_number_of_genres()
    assert genres_number == 7

def test_get_number_of_albums(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    albums_number = repo.get_number_of_albums()
    assert albums_number == 5