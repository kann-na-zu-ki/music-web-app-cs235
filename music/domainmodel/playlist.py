from music.domainmodel.track import Track


class PlayList:

    def __init__(self, playlist_id: int, name:str):
        self.__list_of_tracks = []
        self.__playlist_id = playlist_id
        self.__name = name

    def size(self):
        size_playlist = len(self.__list_of_tracks)
        if size_playlist > 0:
            return size_playlist

    @property
    def playlist_id(self) -> int:
        return self.__playlist_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def tracks(self) -> list:
        return self.__list_of_tracks

    @name.setter
    def name(self, name: str):
        self.__name = None
        if type(name) is str:
            name = name.strip()
            if name != '':
                self.__name = name

    @tracks.setter
    def tracks(self, tracks: list):
        if type(tracks) is list:
            self.__list_of_tracks = tracks

    def add_track(self, track: Track):
        if track not in self.__list_of_tracks:
            self.__list_of_tracks.append(track)
        else:
            pass

    def first_track_in_list(self):
        if len(self.__list_of_tracks) > 0:
            return self.__list_of_tracks[0]
        else:
            return None

    def remove_track(self, track):
        if track in self.__list_of_tracks:
            self.__list_of_tracks.remove(track)
        else:
            pass

    def select_track_to_listen(self, index):
        if 0 <= index < len(self.__list_of_tracks):
            return self.__list_of_tracks[index]
        else:
            return None

    def __iter__(self):
        self.__current = 0
        return self

    def __next__(self):
        if self.__current >= len(self.__list_of_tracks):
            raise StopIteration
        else:
            self.__current += 1
            return self.__list_of_tracks[self.__current - 1]

    def __repr__(self) -> str:
        return f'<Playlist {self.name}, id = {self.playlist_id}>'
