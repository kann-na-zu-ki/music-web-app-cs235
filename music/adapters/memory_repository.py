import csv, random
from pathlib import Path
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from music.adapters.csvdatareader import TrackCSVReader
from music.adapters.repository import AbstractRepository, RepositoryException

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList
from music.tracks.services import get_playlist, get_track_by_id
from music.tracks.tracks import playlist


class MemoryRepository(AbstractRepository):

    def __init__(self):
        # List of unique tracks
        self.__dataset_of_tracks = []
        # Set of unique artists
        self.__dataset_of_artists = set()
        # Set of unique albums
        self.__dataset_of_albums = set()
        # Set of unique genres
        self.__dataset_of_genres = set()
        self.__track_index = dict()

        self.__dataset_of_reviews = list()
        self.__users = list()
        self.__playlists = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user_by_id(self, user_id) -> User:
        for user in self.__users:
            if user.user_id == user_id:
                return user
        return None

    def get_artist(self, id) -> Artist:
        for artist in self.__dataset_of_artists:
            if artist.artist_id == id:
                return artist
        return None

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def load_tracks(self, track_list: List):
        self.__dataset_of_tracks = track_list
        for track in track_list: 
            self.__track_index[track.track_id] = track
            

    def add_track(self, track: Track):
        insort_left(self.__dataset_of_tracks, track)
        self.__track_index[track.track_id] = track

    def get_track(self, id: int) -> Track:
        track = None
        try:
            track = self.__track_index[id]
        except KeyError:
            pass
        return track
        # for track in self.__dataset_of_tracks:
        #     if track.track_id == id:
        #         return track
        # return None

    def get_tracks(self) -> list: 
        return self.__dataset_of_tracks

    def get_number_of_tracks(self):
        return len(self.__dataset_of_tracks)

    def get_tracks_by_artist(self, artist: Artist):
        selected_tracks = []
        for track in self.__dataset_of_tracks: 
            if track.artist == artist:
                selected_tracks.append(track)
        return selected_tracks

    def add_artist(self, artist: Artist):
        if isinstance(artist, Artist):
            self.__dataset_of_artists.add(artist)

    def load_artists(self, artist_set: set):
        self.__dataset_of_artists = artist_set

    def get_artists(self) -> Artist:
        return self.__dataset_of_artists

    def load_genres(self, genre_set: set):
        self.__dataset_of_genres = genre_set

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre):
            self.__dataset_of_genres.add(genre)

    def get_genres(self) -> Genre:
        return self.__dataset_of_genres

    def get_number_of_genres(self):
        return len(self.__dataset_of_genres)

    def get_track_ids_by_genre(self, genre_name: str):
        track_ids = []
        for track in self.__dataset_of_tracks:
            genre_list = []
            for genre in track.genres:
                genre_list.append(genre.name)
            if genre_name in genre_list:
                track_ids.append(track.track_id)
        return track_ids
    def get_tracks_by_ids(self, track_ids: List):
        # Strip out any ids in id_list that don't represent Article ids in the repository.
        existing_ids = [id for id in track_ids if id in self.__track_index]
        tracks = [self.__dataset_of_tracks[id] for id in existing_ids]
        return tracks

    def search_tracks(self, input: str):
        ''' search by title, artist, genre or album'''
        tracks = []
        input = input.lower()
        for track in self.__dataset_of_tracks:
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

    def track_index(self, track: Track):
        index = bisect_left(self.__dataset_of_tracks, track)
        if index != len(self.__dataset_of_tracks) and self.__dataset_of_tracks[index].track_id == track.track_id:
            return index
        raise ValueError


    def load_albums(self, albums_set: set):
        self.__dataset_of_albums = albums_set

    def add_album(self, album: Album):
        if isinstance(album, Album):
            self.__dataset_of_albums.add(album)

    def get_albums(self):
        return self.__dataset_of_albums

    def get_number_of_albums(self):
        return len(self.__dataset_of_albums)

    def add_review(self, review: Review):
        if isinstance(review, Review):
            self.__dataset_of_reviews.append(review)

    def get_reviews(self, track: Track):
        reviews = []
        for review in self.__dataset_of_reviews:
            if review.track == track:
                reviews.append(review)
        return reviews

    def add_playlist(self, playlist: PlayList):
        if isinstance(playlist, PlayList):
            self.__playlists.append(playlist)

    def get_playlist(self, playlist_id: int):
        for playlist in self.__playlists:
            if playlist.playlist_id == playlist_id:
                return playlist
        return None

    def get_playlists(self):
        return self.__playlists

    def add_track_to_playlist(self, playlist: PlayList, track: Track):
        if track not in playlist.tracks:
            playlist.add_track(track)          

    def load_playlists(self):
        p1 = PlayList(0, "Developers' picks")

        indices = [0, 1, 2, 141, 165, 167, 204, 252, 306, 307, 316, 318, 350, 458, 495, 601]

        for i in indices: 
            p1.add_track(self.__dataset_of_tracks[i])  

        self.__playlists.append(p1)

    def create_random_playlist(self, length: int):
        id = len(self.__playlists)
        name = 'Random Playlist #' + str(id)
        p = PlayList(id, name)

        tracks = random.choices(self.__dataset_of_tracks, k=length)
        p.tracks = tracks
        
        self.__playlists.append(p)

        return p



def populate(data_path: Path, repo: MemoryRepository):
    albums_filename = str(Path(data_path) / "raw_albums_excerpt.csv")
    tracks_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")

    csvreader = TrackCSVReader(albums_filename, tracks_filename)
    csvreader.read_csv_files()
    repo.load_tracks(csvreader.dataset_of_tracks)
    repo.load_artists(csvreader.dataset_of_artists)
    repo.load_genres(csvreader.dataset_of_genres)
    repo.load_albums(csvreader.dataset_of_albums)
    repo.load_playlists()


