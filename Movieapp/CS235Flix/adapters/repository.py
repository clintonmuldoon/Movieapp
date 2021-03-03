import abc
from typing import List
from datetime import date

from CS235Flix.domain.model import User, Movie, Genre, Actor, Director, Review


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, id: int) -> Movie:
        """ Returns movie with id from the repository.

        If there is no movie with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_by_genre(self, selected_genre: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_by_director(self, selected_director: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_by_actor(self, selected_actor: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_id(self, id_list):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_movie_ids(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        raise NotImplementedError

    @abc.abstractmethod
    def get_actors(self) -> List[Actor]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, director: Director):
        raise NotImplementedError

    @abc.abstractmethod
    def get_directors(self) -> List[Director]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a review to the repository.

        If the review doesn't have bidirectional links with a movie and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('review not correctly attached to a User')
        if review.movie is None or review not in review.movie.comments:
            raise RepositoryException('Comment not correctly attached to a movie')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError







