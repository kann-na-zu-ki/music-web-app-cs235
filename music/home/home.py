from flask import Blueprint, render_template

import music.tracks.tracks as tracks


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home.html',
        selected_tracks=tracks.get_random_tracks(),
    )