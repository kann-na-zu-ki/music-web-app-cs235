from music.tracks import services as tracks_services
from music.tracks.services import NonExistentTrackException
from music.domainmodel.track import Track
from music.domainmodel.artist import Artist
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList
from music.authentication import service as auth_services
from music.authentication.service import AuthenticationException
import pytest
from flask import url_for


def test_can_get_track(in_memory_repo):
    track_id = 2
    test_track = tracks_services.get_track_by_id(track_id, in_memory_repo)

    assert test_track['title'] == 'Food'


def test_can_get_tracks(in_memory_repo):
    tracks = tracks_services.get_tracks(in_memory_repo)
    assert len(tracks) == 2000


def test_can_get_tracks_by_genre(in_memory_repo):
    tracks = tracks_services.get_track_by_genre('Jazz', in_memory_repo)
    assert len(tracks) == 31


def test_get_tracks_by_artist(in_memory_repo):
    artist = Artist(53, 'Airway')
    t1 = Track(137, 'Live at LACE')
    t2 = Track(138, 'Live at LACE')
    test_list = tracks_services.get_tracks_by_artist(artist, in_memory_repo)
    assert test_list[0]['track_id'] == 137
    assert test_list[1]['track_id'] == 138


def test_get_artist_by_id(in_memory_repo):
    artist = tracks_services.get_artist_by_id(1, in_memory_repo)
    assert artist.full_name == 'AWOL'


def test_search_tracks(in_memory_repo):
    tracks = tracks_services.search_tracks('Amoebiasis', in_memory_repo)
    t1 = in_memory_repo.get_track(144)
    t2 = in_memory_repo.get_track(145)
    assert tracks[0]['track_id'] == 144
    assert tracks[1]['track_id'] == 145


def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = 'thorke'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)
    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_can_add_user(in_memory_repo):
    new_user_name = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)


def test_add_review(in_memory_repo):
    track = tracks_services.get_track_by_id(2, in_memory_repo)
    review = Review(track, 'Amazing song', 5)
    tracks_services.add_review(2, 'Amazing song', 5, in_memory_repo)
    assert tracks_services.get_reviews(2, in_memory_repo)[0].review_text == 'Amazing song'
    assert tracks_services.get_reviews(2, in_memory_repo)[0].track.track_id == track['track_id']


def test_get_tracks_by_ids(in_memory_repo):
    tracks = tracks_services.get_tracks_by_ids([2, 3, 144], in_memory_repo)
    assert len(tracks) == 3


def test_add_playlist(in_memory_repo):
    tracks_services.add_playlist('Mixtape', in_memory_repo)
    assert tracks_services.get_playlist(1, in_memory_repo).playlist_id == 1
    assert tracks_services.get_playlist(1, in_memory_repo).name == 'Mixtape'


def test_get_playlists(in_memory_repo):
    tracks_services.add_playlist('Mixtape', in_memory_repo)
    tracks_services.add_playlist('Mixtape1', in_memory_repo)

    assert len(tracks_services.get_playlists(in_memory_repo)) == 3


def test_add_track_to_playlist(in_memory_repo):
    tracks_services.add_playlist('Mixtape', in_memory_repo)
    tracks_services.add_track_to_playlist(1, 144, in_memory_repo)
    track = tracks_services.get_track_by_id(144, in_memory_repo)
    assert tracks_services.get_playlist(1, in_memory_repo).tracks[0].track_id == 144


def test_create_random_playlist(in_memory_repo):
    p = tracks_services.create_random_playlist(10, in_memory_repo)
    assert len(p.tracks) == 10


def test_can_get_genres(in_memory_repo):
    genres = tracks_services.get_genres(in_memory_repo)
    assert len(genres) == 60


def test_can_get_artists(in_memory_repo):
    artists = tracks_services.get_artists(in_memory_repo)
    assert len(artists) == 263


def test_can_get_albums(in_memory_repo):
    albums = tracks_services.get_albums(in_memory_repo)
    assert len(albums) == 427


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = 'thorke'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)
    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_can_add_user(in_memory_repo):
    new_user_name = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    assert user_as_dict['password'].startswith('pbkdf2:sha256:')

def test_can_get_list_of_genres(in_memory_repo):
    list_genres = tracks_services.get_genres(in_memory_repo)
    assert len(list_genres) == 60

def test_can_get_list_of_albums(in_memory_repo):
    list_albums = tracks_services.get_albums(in_memory_repo)
    assert len(list_albums) == 427

def test_get_random_tracks(in_memory_repo):
    tracks = tracks_services.get_random_tracks(in_memory_repo)
    assert len(tracks) == 5