from pathlib import Path

from music.adapters.repository import AbstractRepository

from music.adapters.csvdatareader import TrackCSVReader



def populate(data_path: Path, repo: AbstractRepository, test_mode: bool):
    # Load articles and tags into the repository.
    if test_mode:
        print('test mode')
        albums_filename = str(Path(data_path) / "raw_albums_test.csv")
        tracks_filename = str(Path(data_path) / "raw_tracks_test.csv")
    else:
        albums_filename = str(Path(data_path) / "raw_albums_excerpt.csv")
        tracks_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")

    csvreader = TrackCSVReader(albums_filename, tracks_filename)
    csvreader.read_csv_files()
    repo.load_artists(csvreader.dataset_of_artists)
    repo.load_tracks(csvreader.dataset_of_tracks)
    repo.load_albums(csvreader.dataset_of_albums)

    repo.load_genres(csvreader.dataset_of_genres)
    repo.load_playlists()