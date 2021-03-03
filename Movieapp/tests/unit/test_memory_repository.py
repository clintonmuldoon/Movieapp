from datetime import date, datetime
from typing import List

import pytest

from CS235Flix.domain.model import User, Movie, Actor, Genre, make_review, Director, Review
from CS235Flix.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()

    # Check that the query returned 10 movies.
    assert number_of_movies == 10


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie(
            "Guardians of the Galaxy",
            "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.",
            2014,
            121,
            8.1,
            757074,
            333.13,
            76
    )
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie(9) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)

    # Check that the Article has the expected title.
    assert movie.title == 'Guardians of the Galaxy'

    # Check that the Article is commented as expected.
    review_one = [review for review in movie.reviews if review.review == 'Oh no, COVID-19 has hit New Zealand'][
        0]
    review_two = [review for review in movie.reviews if review.review == 'Yeah Freddie, bad news'][0]

    assert review_one.user.username == 'fmercury'
    assert review_two.user.username == "thorke"


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(101)
    assert movie is None

def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([123, 555])

    assert len(movies) == 0



