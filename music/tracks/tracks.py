from re import T
from tkinter.messagebox import NO
from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectField, RadioField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError

import music.tracks.services as tracks_services
import music.adapters.repository as repo
from music.domainmodel.track import Track
from music.tracks.forms import TrackSearchForm, ReviewForm, PlaylistForm, CreatePlaylistForm
from music.authentication.authentication import login, login_required

tracks_blueprint = Blueprint(
    'tracks_bp', __name__)


@tracks_blueprint.route('/tracks', methods=['GET', 'POST'])
def get_tracks():
    tracks_per_page = 15
    cursor = request.args.get('cursor')
    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    n = tracks_services.get_number_of_tracks(repo.repo_instance)
    tracks = tracks_services.get_tracks(repo.repo_instance)[cursor:cursor + tracks_per_page]
    for t in tracks:
        t['add_review_url'] = url_for('tracks_bp.review', track=t['track_id'])
        t['add_to_playlist_url'] = url_for('tracks_bp.add_to_playlist', track=t['track_id'])

    next_page_url = None
    prev_page_url = None

    if cursor > 0:
        prev_page_url = url_for('tracks_bp.get_tracks', cursor=cursor - tracks_per_page)

    if cursor + tracks_per_page < n:
        next_page_url = url_for('tracks_bp.get_tracks', cursor=cursor + tracks_per_page)

    return render_template('tracks/tracks.html', tracks=tracks, subheader="Browse", form=None,
                           next_page_url=next_page_url, prev_page_url=prev_page_url,
                           selected_tracks=get_random_tracks(), playlist_id=None)


@tracks_blueprint.route('/byartist/<int:artist_id>', methods=['GET'])
def get_tracks_by_artist(artist_id):
    artist = tracks_services.get_artist_by_id(artist_id, repo.repo_instance)
    tracks = tracks_services.get_tracks_by_artist(artist, repo.repo_instance)
    for t in tracks:
        t['add_review_url'] = url_for('tracks_bp.review', track=t['track_id'])
        t['add_to_playlist_url'] = url_for('tracks_bp.add_to_playlist', track=t['track_id'])
    return render_template('tracks/tracks.html', tracks=tracks, form=None, subheader=artist.full_name, next_page_url=None, prev_page_url=None, playlist_id=None)


@tracks_blueprint.route('/search', methods=['GET', 'POST'])
def search_tracks():
    searchstring = request.args.get('searchstring')
    search = TrackSearchForm(request.form)
    searchstring = search.search.data

    if searchstring is not None:
        if len(searchstring) == 0:
            tracks = None
            return render_template('tracks/tracks.html', tracks=None, form=search, prev_page_url=None,
                                   next_page_url=None, subheader='Search by title, genre, artist or album', playlist_id=None)
        tracks = tracks_services.search_tracks(searchstring.lower(), repo.repo_instance)
        for t in tracks:
            t['add_review_url'] = url_for('tracks_bp.review', track=t['track_id'])
            t['add_to_playlist_url'] = url_for('tracks_bp.add_to_playlist', track=t['track_id'])
        return render_template('tracks/tracks.html', tracks=tracks, form=search, prev_page_url=None, next_page_url=None,
                               subheader='Search by title, genre, artist or album', selected_tracks=get_random_tracks(), playlist_id=None)
    else:
        tracks = None
        return render_template('tracks/tracks.html', tracks=None, form=search, prev_page_url=None, next_page_url=None,
                               subheader='Search by title, genre, artist or album', selected_tracks=get_random_tracks(), playlist_id=None)


@tracks_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    user_name = session['user_name']
    form = ReviewForm()
    if form.validate_on_submit():
        review_text = form.review.data
        rating = form.rating.data
        track_id = int(form.track_id.data)
        tracks_services.add_review(track_id, review_text, int(rating), repo.repo_instance)

    if request.method == 'GET':
        track_id = int(request.args.get('track'))
        form.track_id.data = track_id
    else:
        track_id = int(form.track_id.data)

    track = tracks_services.get_track_by_id(track_id, repo.repo_instance)
    reviews = tracks_services.get_reviews(track_id, repo.repo_instance)
    return render_template('tracks/review.html', form=form, track=track, reviews=reviews,
                           handler_url=url_for('tracks_bp.review'), selected_tracks=get_random_tracks(), playlist_id=None)


@tracks_blueprint.route('/playlist/<int:id>', methods=('GET', 'POST'))
def playlist(id):
    playlist = tracks_services.get_playlist(id, repo.repo_instance)
    tracks = tracks_services.tracks_to_dict(playlist.tracks)
    if len(tracks) == 0:
        tracks = None
    else:
        for t in tracks:
            t['add_review_url'] = url_for('tracks_bp.review', track=t['track_id'])
            t['add_to_playlist_url'] = url_for('tracks_bp.add_to_playlist', track=t['track_id'])

    return render_template('tracks/tracks.html', form=None, tracks=tracks, subheader=playlist.name, next_page_url=None,
                           prev_page_url=None, selected_tracks=get_random_tracks(), playlist_id=id)


@tracks_blueprint.route('/add_to_playlist', methods=('GET', 'POST'))
@login_required
def add_to_playlist():
    user_name = session['user_name']
    form = PlaylistForm()

    playlist_choices = []
    for p in tracks_services.get_playlists(repo.repo_instance):
        playlist_choices.append((p.playlist_id, p.name))
    form.playlist.choices = playlist_choices

    if form.validate_on_submit():
        playlist_id = form.playlist.data
        track_id = int(form.track_id.data)
        tracks_services.add_track_to_playlist(playlist_id, track_id, repo.repo_instance)

    if request.method == 'GET':
        track_id = int(request.args.get('track'))
        form.track_id.data = track_id
        track = tracks_services.get_track_by_id(track_id, repo.repo_instance)
        return render_template('tracks/add_to_playlist.html', form=form, track=track,
                               handler_url=url_for('tracks_bp.add_to_playlist'),
                               selected_tracks=get_random_tracks())
    else:
        track_id = int(form.track_id.data)
        playlist_id = form.playlist.data
        track = tracks_services.get_track_by_id(track_id, repo.repo_instance)
        return redirect(url_for('tracks_bp.playlist', id=playlist_id))


@tracks_blueprint.route('/create_playlist', methods=['GET', 'POST'])
@login_required
def create_playlist():
    playlists = tracks_services.get_playlists(repo.repo_instance)
    form = CreatePlaylistForm()
    error = None

    if form.validate_on_submit():
        try:
            title = form.title.data
            tracks_services.add_playlist(title, repo.repo_instance)
        except tracks_services.TitleNotUnique:
            error = 'Playlist name already taken - please supply another'

    if request.method == 'GET':
        title = form.title.data

    else:
        title = form.title.data

    return render_template('tracks/playlists.html', playlists=playlists, form=form, error=error,
                           handler_url=url_for('tracks_bp.create_playlist'),
                           selected_tracks=get_random_tracks())


@tracks_blueprint.route('/artists',methods=['GET'])
def get_artists():
    artists_per_page = 20
    cursor = request.args.get('cursor')
    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    artists = list(tracks_services.get_artists(repo.repo_instance))[cursor:cursor + artists_per_page]
    n = len(tracks_services.get_artists(repo.repo_instance))

    next_page_url = None
    prev_page_url = None

    if cursor > 0:
        prev_page_url = url_for('tracks_bp.get_artists', cursor=cursor - artists_per_page)

    if cursor + artists_per_page < n:
        next_page_url = url_for('tracks_bp.get_artists', cursor=cursor + artists_per_page)


    return render_template('tracks/artists.html', artists=artists, subheader = "Browse", next_page_url=next_page_url, prev_page_url=prev_page_url)

@tracks_blueprint.route('/create_random_playlist', methods=['GET'])
def create_random_playlist():
    p = tracks_services.create_random_playlist(15, repo.repo_instance)
    
    return redirect(url_for('tracks_bp.playlist', id=p.playlist_id))

@tracks_blueprint.route('/track/<int:track_id>', methods=['GET'])
def get_track_by_id(track_id):
    track = tracks_services.get_track_by_id(track_id, repo.repo_instance)

    return render_template('simple_track.html', track=track)

@tracks_blueprint.route('/genres', methods=['GET'])
def get_genres():
    genres_per_page = 20
    cursor = request.args.get('cursor')
    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)
    n = tracks_services.get_number_of_genres(repo.repo_instance)
    genres = tracks_services.get_genres(repo.repo_instance)[cursor:cursor + genres_per_page]

    next_page_url = None
    prev_page_url = None

    if cursor > 0:
        prev_page_url = url_for('tracks_bp.get_genres', cursor=cursor - genres_per_page)

    if cursor + genres_per_page < n:
        next_page_url = url_for('tracks_bp.get_genres', cursor=cursor + genres_per_page)

    return render_template('tracks/genres.html', genres=genres, subheader="Genres for You", form=None,
                           next_page_url=next_page_url, prev_page_url=prev_page_url,
                           selected_tracks=get_random_tracks())


@tracks_blueprint.route('/albums', methods=['GET'])
def get_albums():
    albums_per_page = 20
    cursor = request.args.get('cursor')
    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)
    n = tracks_services.get_number_of_albums(repo.repo_instance)
    albums = tracks_services.get_albums(repo.repo_instance)[cursor:cursor + albums_per_page]
    next_page_url = None
    prev_page_url = None
    if cursor > 0:
        prev_page_url = url_for('tracks_bp.get_albums', cursor=cursor - albums_per_page)

    if cursor + albums_per_page < n:
        next_page_url = url_for('tracks_bp.get_albums', cursor=cursor + albums_per_page)

    return render_template('tracks/albums.html', albums=albums, subheader="Albums for You", form=None,
                           next_page_url=next_page_url, prev_page_url=prev_page_url,
                           selected_tracks=get_random_tracks())

def get_random_tracks():
    tracks = tracks_services.get_random_tracks(repo.repo_instance)
    return tracks