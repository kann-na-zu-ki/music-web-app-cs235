from music.adapters.repository import AbstractRepository, RepositoryException
from flask import url_for

from typing import List, Iterable

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList
import random


class NonExistentTrackException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class TitleNotUnique(Exception):
    pass


def get_track_by_id(track_id: int, repo: AbstractRepository):
    track = repo.get_track(track_id)

    if track is None:
        raise NonExistentTrackException

    return track_to_dict(track)


def get_tracks(repo: AbstractRepository):
    tracks = repo.get_tracks()
    if tracks is None:
        raise NonExistentTrackException
    return tracks_to_dict(tracks)


def get_number_of_tracks(repo: AbstractRepository):
    length = repo.get_number_of_tracks()
    return length


def get_tracks_by_ids(ids: list, repo: AbstractRepository):
    tracks = repo.get_tracks_by_ids(ids)
    return tracks


def get_track_by_genre(genre_name: str, repo: AbstractRepository):  # DO WE NEED THIS?
    track_ids = repo.get_track_ids_by_genre(
        genre_name)  # I wrote this one to simulate get_artical by tags to put genres on navi bar. However we have too many genres. So give up the idea.
    return track_ids


def get_tracks_by_artist(artist: Artist, repo: AbstractRepository):
    tracks = repo.get_tracks_by_artist(artist)
    return tracks_to_dict(tracks)


def get_artist_by_id(artist_id: int, repo: AbstractRepository):
    artist = repo.get_artist(artist_id)
    if artist is None:
        raise NonExistentTrackException
    return artist


def search_tracks(search_input: str, repo: AbstractRepository):
    tracks = repo.search_tracks(search_input)
    return tracks_to_dict(tracks)


def add_review(track_id: int, review_text: str, review_rating: int, repo: AbstractRepository):
    track = repo.get_track(track_id)
    if track == None:
        raise NonExistentTrackException
    review = Review(track, review_text, review_rating)
    repo.add_review(review)


def get_reviews(track_id: int, repo: AbstractRepository):
    track = repo.get_track(track_id)
    if track == None:
        raise NonExistentTrackException
    reviews = repo.get_reviews(track)
    return reviews


def get_artists(repo: AbstractRepository):
    artists = repo.get_artists()
    return artists


def get_genres(repo: AbstractRepository):
    genres = repo.get_genres()
    return genres


def get_albums(repo: AbstractRepository):
    albums = repo.get_albums()
    return albums


def track_to_dict(track: Track):
    track_dict = {
        'track_id': track.track_id,
        'title': track.title,
        'genres': track.genres,
        'artist': track.artist,
        'duration': track.track_duration,
        'url': track.track_url,
        'album': track.album,
    }
    return track_dict


def tracks_to_dict(tracks: Iterable[Track]):
    return [track_to_dict(track) for track in tracks]


def add_playlist(playlist_name: str, repo: AbstractRepository):
    playlists = repo.get_playlists()
    for p in playlists:
        if p.name == playlist_name:
            raise TitleNotUnique
    id = len(repo.get_playlists())
    playlist = PlayList(id, playlist_name)
    repo.add_playlist(playlist)


def get_playlists(repo: AbstractRepository):
    return repo.get_playlists()


def get_playlist(id: int, repo: AbstractRepository):
    return repo.get_playlist(id)


def add_track_to_playlist(playlist_id: int, track_id: int, repo: AbstractRepository):
    p = repo.get_playlist(playlist_id)
    t = repo.get_track(track_id)
    repo.add_track_to_playlist(p, t)


def create_random_playlist(length: int, repo: AbstractRepository):
    return repo.create_random_playlist(length)


def get_number_of_genres(repo: AbstractRepository):
    length = repo.get_number_of_genres()
    return length


def get_number_of_albums(repo: AbstractRepository):
    length = repo.get_number_of_albums()
    return length


def get_genres(repo: AbstractRepository):
    genres = repo.get_genres()
    genres_list = []
    if genres is None:
        raise NonExistentTrackException
    for genre in genres:
        genres_list.append(genre)
    genres_list.sort()
    return genres_list


def get_albums(repo: AbstractRepository):
    albums = repo.get_albums()
    albums_list = []
    if albums is None:
        raise NonExistentTrackException
    for album in albums:
        albums_list.append(album)
    albums_list.sort()
    return albums_list


def get_random_tracks(repo: AbstractRepository):
    tracks = repo.get_tracks()
    length = len(tracks)
    random_index_list = []
    for i in range(5):
        random_index = random.randint(1, 5)
        random_index_list.append(random_index)
    random_tracks = []
    for index in random_index_list:
        random_tracks.append(tracks[index])
    return random_tracks
