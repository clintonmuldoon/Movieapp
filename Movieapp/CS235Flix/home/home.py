from flask import Blueprint, render_template

import CS235Flix.utilities.utilities as utilities


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html',
        #selected_articles=utilities.get_selected_articles(),
        genre_urls=utilities.get_genres_and_urls(),
        actor_urls=utilities.get_actors_and_urls(),
        director_urls=utilities.get_directors_and_urls(),
    )
