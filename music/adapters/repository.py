import abc 
from typing import List
from datetime import date

from music.domainmodel.artist import Artist
from music.domainmodel.album import  Album
from music.domainmodel.playlist import PlayList
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review

repo_instance = None

class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_track(self, track: Track):
        """ Adds an Track to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track(self, id: int) -> Track:
        """ Returns Track with id from the repository.

        If there is no Track with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks(self) -> list:
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_number_of_tracks(self) -> int:
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_tracks_by_artist(self, artist: Artist) -> list:
        raise NotImplementedError

    @abc.abstractclassmethod
    def search_tracks(self, input: str) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def add_artist(self, artist: Artist):
        raise NotImplementedError

    @abc.abstractmethod
    def get_artists(self) -> Artist:
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> Genre:
        raise NotImplementedError

    @abc.abstractmethod
    def add_album(self, album: Album):
        raise NotImplementedError

    @abc.abstractmethod
    def get_albums(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_playlist(self, playlist: PlayList):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_playlist(self, playlist_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlists(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_track_to_playlist(self, playlist_id: int, track_id: int):
        raise NotImplementedError
    
    @abc.abstractmethod
    def create_random_playlist(self, length:int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_genres(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_albums(self):
        raise NotImplementedError