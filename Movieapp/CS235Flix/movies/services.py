from typing import List, Iterable

from CS235Flix.adapters.repository import AbstractRepository
from CS235Flix.domain.model import make_review, Movie, Actor, Genre, Review, Director


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(movie_id: int, review_text: str, username: str, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie(movie_id)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create review.
    review = make_review(review_text, user, movie)

    # Update the repository.
    repo.add_review(review)


def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_all_movie_ids(repo: AbstractRepository):
    movie_ids = repo.get_all_movie_ids()

    return movie_ids


def get_movie_ids_by_genre(genre_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_by_genre(genre_name)

    return movie_ids


def get_movie_ids_by_actor(actor_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_by_actor(actor_name)

    return movie_ids


def get_movie_ids_by_director(director_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_by_director(director_name)

    return movie_ids


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)

    # Convert Movies to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_reviews_for_movie(movie_id, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return reviews_to_dict(movie.comments)


def get_reviews_for_movie(movie_id, repo: AbstractRepository):
    article = repo.get_movie(movie_id)

    if article is None:
        raise NonExistentMovieException

    return reviews_to_dict(article.comments)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie):

    movie_dict = {
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'year': movie.year,
        'runtime_minutes': movie.runtime_minutes,
        'rating': movie.rating,
        'votes': movie.votes,
        'revenue_millions': movie.revenue_millions,
        'meta_score': movie.meta_score,
        'reviews': reviews_to_dict(movie.reviews),
        'genres': genres_to_dict(movie.genres),
        'actors': actors_to_dict(movie.actors),
        'directors': directors_to_dict(movie.directors)
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def review_to_dict(review: Review):
    review_dict = {
        'username': review.user.username,
        'movie_id': review.movie.id,
        'review_text': review.review,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


def genre_to_dict(genre: Genre):
    genre_dict = {
        'name': genre.genre_name,
        'genre_of_movies': [movie.id for movie in genre.genre_of_movies]
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]


def actor_to_dict(actor: Actor):
    actor_dict = {
        'name': actor.actor_name,
        'acted_movies': [movie.id for movie in actor.acted_movies]
    }
    return actor_dict


def actors_to_dict(actors: Iterable[Actor]):
    return [actor_to_dict(actor) for actor in actors]


def director_to_dict(director: Director):
    director_dict = {
        'name': director.director_name,
        'directed_movies': [movie.id for movie in director.directed_movies]
    }
    return director_dict


def directors_to_dict(directors: Iterable[Director]):
    return [director_to_dict(director) for director in directors]


# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_movie(dict):
    movie = Movie(dict.id, dict.title, dict.description, dict.year, dict.runtime_minutes,dict.rating,dict.rating,dict.votes,dict.revenue_millions,
                  dict.meta_score, dict.reviews, dict.genres, dict.actors, dict.directors)
    # Note there's no comments or tags.
    return movie
