import random
from datetime import date
from typing import List
from pathlib import Path
from sqlalchemy import desc, asc, select
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from music.adapters.csvdatareader import TrackCSVReader
from music.adapters.repository import AbstractRepository, RepositoryException

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def load_tracks(self, tracks):
        print('....LOADING TRACKS...')
        for t in tracks:
            self.add_track(t)

    def load_artists(self, artists):
        print('....LOADING ARTISTS...')
        for a in artists:
            self.add_artist(a)

    def load_albums(self, albums):
        print('....LOADING ALBUMS...')
        for a in albums:
            self.add_album(a)

    def load_genres(self, genres):
        print('....LOADING GENRES...')
        for a in genres:
            self.add_genre(a)

    def load_playlists(self):
        print('....LOADING PLAYLISTS...')
        p1 = PlayList(0, "Developers' picks")

        indices = [2, 3, 5, 10, 20]
        for a in indices:
            p1.add_track(self.get_track(a))
        self.add_playlist(p1)

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def add_track(self, track: Track):
        with self._session_cm as scm:
            scm.session.merge(track)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return user

    def get_track(self, id: int):
        track = None
        try:
            track = self._session_cm.session.query(Track).filter(Track._Track__track_id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return track

    def get_tracks(self):
        tracks = self._session_cm.session.query(Track).all()
        return tracks

    def get_number_of_tracks(self):
        number_of_tracks = self._session_cm.session.query(Track).count()
        return number_of_tracks

    def get_tracks_by_artist(self, artist: Artist):
        if artist is None:
            tracks = self._session_cm.session.query(Track).all()
            return tracks
        else:
            tracks = self._session_cm.session.query(Track).filter(Track._Track__artist == artist).all()
            return tracks
    
    def search_tracks(self, input: str):
        dataset_of_tracks = self._session_cm.session.query(Track).all()
        tracks = []
        input = input.lower()
        for track in dataset_of_tracks:
            genre_match = False
            if len(track.genres) == 1:
                if input in track.genres[0].name.lower():
                    genre_match = True
            elif len(track.genres) > 1:
                for g in track.genres:
                    if input in g.name.lower():
                        genre_match = True

            if input in track.title.lower() or (track.artist is not None and input in track.artist.full_name.lower()) or (track.album is not None and input in track.album.title.lower()) or genre_match:
                tracks.append(track)
        return tracks

    def add_artist(self, artist: Artist):
        with self._session_cm as scm:
            scm.session.merge(artist)
            scm.commit()

    def get_artist(self, id):
        a = None
        try:
            a = self._session_cm.session.query(Artist).filter(Artist._Artist__artist_id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return a

    def get_artists(self):
        artists = []
        try:
            artists = self._session_cm.session.query(Artist).all()
        except NoResultFound:
            pass

        return artists

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()
    
    def get_genres(self):
        genres = []
        try:
            genres = self._session_cm.session.query(Genre).all()
        except NoResultFound:
            pass
        return genres

    def add_album(self, album: Album):
        with self._session_cm as scm:
            scm.session.merge(album)
            scm.commit()

    def get_album(self, id):
        a = None
        try:
            a = self._session_cm.session.query(Album).filter(Album._Album__album_id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return a
    
    def get_albums(self):
        albums = []
        try:
            albums = self._session_cm.session.query(Album).all()
        except NoResultFound:
            pass

        return albums

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews(self, track: Track):
        reviews = self._session_cm.session.query(Review).filter(Track._Track__track_id == track.track_id).all()
        return reviews

    def add_playlist(self, playlist: PlayList):
        with self._session_cm as scm:
            scm.session.add(playlist)
            scm.commit()

    def get_playlist(self, playlist_id: int):
        playlist = None
        try:
            playlist = self._session_cm.session.query(PlayList).filter(PlayList._PlayList__playlist_id == playlist_id).one()
        except NoResultFound:
            pass
        return playlist

    def get_playlists(self):
        playlists = []
        try:
            playlists = self._session_cm.session.query(PlayList).all()
        except NoResultFound:
            pass

        return playlists

    def add_track_to_playlist(self, playlist_id: int, track_id: int):
        playlist = self.get_playlist(playlist_id)
        track = self.get_track(track_id)
        if track not in playlist.tracks:
            playlist.add_track(track)
        

    def create_random_playlist(self, length: int):
        playlists = self._session_cm.session.query(PlayList).all()
        dataset_of_tracks = self._session_cm.session.query(Track).all()

        id = len(playlists)
        name = 'Random Playlist #' + str(id)
        p = PlayList(id, name)

        tracks = random.choices(dataset_of_tracks, k=length)
        p.tracks = tracks

        self.add_playlist(p)

        return p

    def get_number_of_genres(self):
        number_of_genres = self._session_cm.session.query(Genre).count()
        return number_of_genres

    def get_number_of_albums(self):
        number_of_albums = self._session_cm.session.query(Album).count()
        return number_of_albums
