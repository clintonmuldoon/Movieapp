from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from CS235Flix.adapters import repository as repo
import CS235Flix.utilities.utilities as utilities
import CS235Flix.movies.services as services

from CS235Flix.authentication.authentication import login_required


# Configure Blueprint.
movies_blueprint = Blueprint(
    'movies_bp', __name__)


@movies_blueprint.route('/movies_by_variables', methods=['GET'])
def movies_by_variables():
    movies_per_page = 3

    # Read query parameters.
    genre_name = request.args.get('genre')
    director_name = request.args.get('director')
    actor_name = request.args.get('actor')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    if movie_to_show_reviews is None:
        # No view-comments query parameter, so set to a non-existent article id.
        movie_to_show_reviews = -1
    else:
        # Convert article_to_show_comments from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)
    if genre_name:
        genre_name = genre_name.strip()
    else:
        genre_name = ''
    if actor_name:
        actor_name = actor_name.strip()
    else:
        actor_name = ''
    if director_name:
        director_name = director_name.strip()
    else:
        director_name = ''
    movie_ids = services.get_all_movie_ids(repo.repo_instance)
    # Retrieve article ids for articles that are tagged with tag_name.
    if genre_name:
        genre_movie_ids = services.get_movie_ids_by_genre(genre_name, repo.repo_instance)
        movie_ids = list(set(movie_ids) & set(genre_movie_ids))

    # Retrieve article ids for articles that are tagged with tag_name.
    if actor_name:
        actor_movie_ids = services.get_movie_ids_by_actor(actor_name, repo.repo_instance)
        movie_ids = list(set(movie_ids) & set(actor_movie_ids))

    # Retrieve article ids for articles that are tagged with tag_name.
    if director_name:
        director_movie_ids = services.get_movie_ids_by_director(director_name, repo.repo_instance)
        movie_ids = list(set(movie_ids) & set(director_movie_ids))

    # Retrieve the batch of articles to display on the Web page.
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movies_by_variables', genre=genre_name, actor=actor_name, director=director_name,
                                 cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_variables', genre=genre_name, actor=actor_name, director=director_name)

    if cursor + movies_per_page < len(movie_ids):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_variables', genre=genre_name, actor=actor_name, director=director_name
                                 , cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_variables', genre=genre_name, actor=actor_name, director=director_name, cursor=last_cursor)

    # Construct urls for viewing article comments and adding comments.
    for movie in movies:
        movie['view_comment_url'] = url_for('movies_bp.movies_by_variables', genre=genre_name, actor=actor_name, director=director_name,
                                            cursor=cursor, view_comments_for=movie['id'])
        movie['add_comment_url'] = url_for('movies_bp.review_on_movie', movie=movie['id'])

    # Generate the webpage to display the articles.
    if genre_name is None:
        genre_name = 'None'
    return render_template(
        'movies/movies.html',
        title='Movies',
        articles_title='Movies information: ' + genre_name,
        movies=movies,
        genre_urls=utilities.get_genres_and_urls(),
        actor_urls=utilities.get_actors_and_urls(),
        director_urls=utilities.get_directors_and_urls(),
        first_article_url=first_movie_url,
        last_article_url=last_movie_url,
        prev_article_url=prev_movie_url,
        next_article_url=next_movie_url,
        show_reviews_for_movie=movie_to_show_reviews
    )


@movies_blueprint.route('/review_on_movie', methods=['GET', 'POST'])
@login_required
def review_on_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the article id, representing the commented article, from the form.
        movie_id = int(form.movie_id.data)

        # Use the service layer to store the new comment.
        services.add_review(movie_id, form.comment.data, username, repo.repo_instance)

        # Retrieve the article in dict form.
        movie = services.get_movie(movie_id, repo.repo_instance)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('movies_bp.review_on_movie', date=movie['year'], view_reviews_for=movie_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        movie_id = int(request.args.get('movie'))

        # Store the article id in the form.
        form.movie_id.data = movie_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        movie_id = int(form.movie_id.data)

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    movie = services.get_movie(movie_id, repo.repo_instance)
    return render_template(
        'movies/review_on_movie.html',
        title='Review movie',
        movie=movie,
        form=form,
        handler_url=url_for('movie_bp.review_on_movie'),
        selected_articles=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls(),
        actor_urls=utilities.get_actors_and_urls(),
        director_urls=utilities.get_directors_and_urls(),
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    movie_id = HiddenField("Movie id")
    submit = SubmitField('Submit')