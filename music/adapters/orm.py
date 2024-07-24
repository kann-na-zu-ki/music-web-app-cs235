from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

artists = Table(
    'artists', metadata,
    Column('artist_id', Integer, primary_key=True),
    Column('full_name', String(255), primary_key=True),

)

albums = Table(
    'albums', metadata,
    Column('album_id', Integer, primary_key=True),
    Column('title', String(255)),
    Column('album_url', String(255)),
    Column('album_type', String(255)),
    Column('release_year', Integer),

)

tracks = Table(
    'tracks', metadata,
    Column('track_id', Integer, primary_key=True),
    Column('title', String(255)),
    Column('track_duration', Integer),
    Column('track_url', String(255)),
    Column('artist_id', ForeignKey('artists.artist_id')),
    Column('album_id', ForeignKey('albums.album_id')),
)
track_genre = Table(
    'track_genre', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.track_id')),
    Column('genre_id', ForeignKey('genres.genre_id')),
)

genres = Table(
    'genres', metadata,
    Column('genre_id', Integer, primary_key=True),
    Column('genre_name', String(255), nullable=False)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.track_id')),
    # Column('user_id', ForeignKey('users.id')),
    Column('review_text', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

playlists = Table(
    'playlists', metadata,
    Column('playlist_id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255))
)

track_playlist = Table(
    'track_playlist', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.track_id')),
    Column('playlist_id', ForeignKey('playlists.playlist_id'))
)


def map_model_to_tables():
    mapper(User, users, properties={
        '_User__user_name': users.c.user_name,
        '_User__password': users.c.password,
        '_User__user_id': users.c.id,
    })

    mapper(Artist, artists, properties={
        '_Artist__artist_id': artists.c.artist_id,
        '_Artist__full_name': artists.c.full_name,
        '_Artist__tracks': relationship(Track, backref='_Track__artist')

    })

    mapper(Album, albums, properties={
        '_Album__album_id': albums.c.album_id,
        '_Album__title': albums.c.title,
        '_Album__album_url': albums.c.album_url,
        '_Album__release_year': albums.c.release_year,
        '_Album__album_type': albums.c.album_type,
        '_Album__tracks': relationship(Track, backref='_Track__album')
    })

    mapper(Track, tracks, properties={
        '_Track__track_id': tracks.c.track_id,
        '_Track__title': tracks.c.title,
        '_Track__track_duration': tracks.c.track_duration,
        '_Track__track_url': tracks.c.track_url,
        '_Track__genres': relationship(Genre, secondary=track_genre, backref='_Track__genres')
    })

    mapper(Genre, genres, properties={
        '_Genre__genre_id': genres.c.genre_id,
        '_Genre__name': genres.c.genre_name
    })

    mapper(Review, reviews, properties={
        '_Review__review_text': reviews.c.review_text,
        '_Review__timestamp': reviews.c.timestamp,
        '_Review__track': relationship(Track, backref='_Track__reviews'), 
        '_Review__rating': reviews.c.rating,
    })

    mapper(PlayList, playlists, properties={
        '_PlayList__playlist_id': playlists.c.playlist_id,
        '_PlayList__name': playlists.c.name,
        '_PlayList__list_of_tracks': relationship(Track, secondary=track_playlist)
    })

