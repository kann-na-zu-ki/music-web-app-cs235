from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectField, RadioField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError

class TrackSearchForm(FlaskForm):
    search = StringField('Search...')
    submit = SubmitField('Search')

class ReviewForm(FlaskForm):
    track_id = HiddenField("Track id")
    review = TextAreaField('Review...', [DataRequired(), Length(min=4, message='Your comment is too short')])
    rating = RadioField(' Star rating', [DataRequired()], choices=[1, 2, 3, 4, 5])
    submit = SubmitField('Post')

class PlaylistForm(FlaskForm):
    track_id = HiddenField("Track id")
    playlist = RadioField("Playlist", [DataRequired()], coerce=int)
    submit = SubmitField('Add')

class CreatePlaylistForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(min=4, message='Your title is too short')])
    submit = SubmitField('Create')



    



    
