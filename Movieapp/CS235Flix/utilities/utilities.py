from flask import Blueprint, request, render_template, redirect, url_for, session

from CS235Flix.adapters import repository as repo
import CS235Flix.utilities.services as services


# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_genres_and_urls():
    genre_names = services.get_genre_names(repo.repo_instance)
    genre_urls = dict()
    for genre_name in genre_names:
        genre_urls[genre_name] = url_for('movies_bp.movies_by_variables', genre=genre_name)

    return genre_urls

def get_actors_and_urls():
    actor_names = services.get_actor_names(repo.repo_instance)
    actor_urls = dict()
    for actor_name in actor_names:
        actor_urls[actor_name] = url_for('movies_bp.movies_by_variables', actor=actor_name)

    return actor_urls


def get_directors_and_urls():
    director_names = services.get_director_names(repo.repo_instance)
    director_urls = dict()
    for director_name in director_names:
        director_urls[director_name] = url_for('movies_bp.movies_by_variables', director=director_name)

    return director_urls


#def get_selected_articles(quantity=3):
   # articles = services.get_random_articles(quantity, repo.repo_instance)

   # for article in articles:
   #     article['hyperlink'] = url_for('news_bp.articles_by_date', date=article['date'].isoformat())
   # return articles
