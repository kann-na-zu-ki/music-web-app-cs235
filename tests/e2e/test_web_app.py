import pytest

from flask import session


# def test_get_track_by_id(client):
#     # Check that we can retrieve the tracks page. 
#     response = client.get('/track/2')
#     assert response.status_code == 200

def test_get_tracks(client):
    response = client.get('/tracks')
    assert response.status_code == 200


def test_get_tracks_by_artist(client):
    response = client.get('/byartist/1')
    assert response.status_code == 200


def test_register(client):
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == '/authentication/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another')
))
def test_register_with_invalid_input(client, user_name, password, message):
    client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login_and_logout(client):
    client.post(
        '/authentication/register',
        data={'user_name': 'fmercury', 'password': 'Test#6^0'}
    )
    client.post(
        '/authentication/login',
        data={'user_name': 'fmercury', 'password': 'Test#6^0'}
    )
    with client:
        client.get('/')
        assert session['user_name'] == 'fmercury'
    response = client.get('/authentication/logout')
    assert response.headers['Location'] == '/'


def test_login_required_to_review(client):
    response = client.get('/review?track=3')
    assert response.headers['Location'] == '/authentication/login'


def test_can_not_add_to_playlist_without_login(client):
    response_to_add_to_playlist = client.post('/add_to_playlist')
    assert response_to_add_to_playlist.headers['Location'] == '/authentication/login'
    client.post(
        '/authentication/register',
        data={'user_name': 'fmercury', 'password': 'Test#6^0'}
    )
    client.post(
        '/authentication/login',
        data={'user_name': 'fmercury', 'password': 'Test#6^0'}
    )
    response_to_add_to_playlist_after_login = client.get('/add_to_playlist?track=2')
    assert response_to_add_to_playlist_after_login.status_code == 200

def test_can_get_artists(client):
    response = client.get('/artists')
    assert response.status_code == 200

def test_search_tracks(client):
    response = client.post('/search', data={'searchstring': 'Food'})
    assert response.status_code == 200

def test_can_get_genres(client):
    response = client.get('/genres')
    assert response.status_code == 200

def test_can_get_albums(client):
    response = client.get('/albums')
    assert response.status_code == 200

def test_can_create_random_playlist(client):
    response = client.get('/create_random_playlist')
    assert response.status_code == 302

def test_can_create_playlist(client):
    response = client.get('/create_playlist')
    assert response.status_code == 302
    response_after_create = client.post('/create_playlist', data={'Title': 'Playlist1'})
    assert response_after_create.status_code == 302

def test_add_to_playlist(client):
    response = client.get('/add_to_playlist')
    assert response.headers['Location'] == '/authentication/login'
    client.post(
        '/authentication/register',
        data={'user_name': 'fmercury', 'password': 'Test#6^0'}
    )
    client.post(
        '/authentication/login',
        data={'user_name': 'fmercury', 'password': 'Test#6^0'}
    )
    response = client.get('/add_to_playlist?track=3')
    assert response.status_code == 200

def test_playlist(client):
    response = client.get('/playlist/0')
    assert response.status_code == 200

def test_review(client):
    client.post(
        '/authentication/register',
        data={'user_name': 'fmercury', 'password': 'Test#6^0'}
    )
    client.post(
        '/authentication/login',
        data={'user_name': 'fmercury', 'password': 'Test#6^0'}
    )
    response = client.get('/review?track=3')
    assert response.status_code == 200