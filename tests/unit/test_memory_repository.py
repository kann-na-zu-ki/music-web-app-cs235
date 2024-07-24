from datetime import date, datetime
from typing import List

import pytest

from music.adapters.repository import AbstractRepository, RepositoryException

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList


def test_repository_can_add_a_user(in_memory_repo):
    user = User(1, 'dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = User(2, 'fmercury', '8734gfe2058v')
    in_memory_repo.add_user(user)
    user = in_memory_repo.get_user('fmercury')
    assert user == User(2, 'fmercury', '8734gfe2058v')


def test_repository_can_add_track(in_memory_repo):
    track = Track(1, 'Test song')
    in_memory_repo.add_track(track)

    assert in_memory_repo.get_track(1) is track


def test_repository_can_retrieve_track(in_memory_repo):
    track = in_memory_repo.get_track(2)
    assert track == Track(2, 'Food')


def test_number_of_tracks(in_memory_repo):
    n = in_memory_repo.get_number_of_tracks()
    assert n == 2000


def test_get_tracks_by_artist(in_memory_repo):
    artist = Artist(53, 'Airway')
    t1 = Track(137, 'Live at LACE')
    t2 = Track(138, 'Live at LACE')
    test_list = in_memory_repo.get_tracks_by_artist(artist)
    assert test_list == [t1, t2]


def test_get_tracks(in_memory_repo):
    tracks = in_memory_repo.get_tracks()
    assert len(tracks) == 2000


def test_repository_get_track_ids_by_genre(in_memory_repo):
    track_ids = in_memory_repo.get_track_ids_by_genre('Jazz')
    assert len(track_ids) == 31


def test_repository_get_tracks_by_ids(in_memory_repo):
    tracks = in_memory_repo.get_tracks_by_ids([2, 3])
    assert len(tracks) == 2


def test_search_tracks(in_memory_repo):
    album_input = 'amoebiasis'
    t1 = in_memory_repo.get_track(144)
    t2 = in_memory_repo.get_track(145)
    byalbum = in_memory_repo.search_tracks(album_input)
    assert byalbum == [t1, t2]


def test_add_review(in_memory_repo):
    t1 = in_memory_repo.get_track(144)
    t2 = in_memory_repo.get_track(145)
    r1 = Review(t1, 'Average', 3)
    r2 = Review(t2, 'Amazing', 5)

    in_memory_repo.add_review(r1)
    in_memory_repo.add_review(r2)
    assert in_memory_repo.get_reviews(t1) == [r1]
    assert in_memory_repo.get_reviews(t1)[0].rating == 3
    assert in_memory_repo.get_reviews(t2) == [r2]


def test_add_playlist(in_memory_repo):
    playlist1 = PlayList(1, 'Mixtape')
    in_memory_repo.add_playlist(playlist1)
    assert in_memory_repo.get_playlist(1) == playlist1


def test_get_playlists(in_memory_repo):
    playlist1 = PlayList(1, 'Mixtape')
    playlist2 = PlayList(2, 'Mixtape2')
    in_memory_repo.add_playlist(playlist1)
    in_memory_repo.add_playlist(playlist2)

    assert len(in_memory_repo.get_playlists()) == 3


def test_add_track_to_playlist(in_memory_repo):
    playlist1 = PlayList(1, 'Mixtape')
    t1 = in_memory_repo.get_track(144)
    in_memory_repo.add_playlist(playlist1)
    in_memory_repo.add_track_to_playlist(playlist1, t1)
    assert in_memory_repo.get_playlist(1).tracks == [t1]


def test_create_random_playlist(in_memory_repo):
    p = in_memory_repo.create_random_playlist(10)
    assert len(p.tracks) == 10


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_add_artist_get_artists(in_memory_repo):
    artist = Artist(1701, 'artist1701')
    in_memory_repo.add_artist(artist)
    assert artist in in_memory_repo.get_artists()


def test_repository_can_add_genre_get_genres(in_memory_repo):
    genre = Genre(1300, 'Chinese Style')
    in_memory_repo.add_genre(genre)
    assert genre in in_memory_repo.get_genres()


def test_repository_can_add_album_get_albums(in_memory_repo):
    album = Album(5000, 'Galway Girl')
    in_memory_repo.add_album(album)
    assert album in in_memory_repo.get_albums()
    assert len(in_memory_repo.get_albums()) == 428
