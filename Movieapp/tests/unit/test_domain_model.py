from datetime import date

from CS235Flix.domain.model import User, Genre, Actor, Director, Movie, Review, make_genre_association, \
    make_actor_association, make_director_association, ModelException

import pytest


@pytest.fixture()
def movie():
    return Movie(
        "Guardians of the Galaxy",
        "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.",
        2014,
        121,
        8.1,
        757074,
        333.13,
        76
    )


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def genre():
    return Genre('Action')

@pytest.fixture()
def actor():
    return Actor('Chris Pratt')

@pytest.fixture()
def director():
    return Director('James Gunn')


def test_user_construction(user):
    assert user.username == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie 1234567890>'

    for review in user.reviews:
        # User should have an empty list of Comments after construction.
        assert False


def test_movie_construction(movie):
    assert movie.id is None
    assert movie.year == 2014
    assert movie.title == "Guardians of the Galaxy"
    assert movie.description == 'A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.'
    assert movie.runtime_minutes == 121
    assert movie.rating == 8.1
    assert movie.votes == 757074
    assert movie.revenue_millions == 333.13
    assert movie.meta_score == 76

def test_actor_construction(actor):
    assert actor.actor_name == 'Chris Pratt'

    for movie in actor.acted_movies:
        assert False

    assert not actor.is_applied_to(Movie(None, None, None, None, None, None, None, None))


def test_director_construction(director):
    assert director.director_name == 'James Gunn'

    for director in director.directed_movies:
        assert False

    assert not director.is_applied_to(Movie(None, None, None, None, None, None, None, None))


def test_genre_construction(genre):
    assert genre.genre_name == 'Action'

    for movie in genre.genre_of_movies:
        assert False

    assert not genre.is_applied_to(Movie(None, None, None, None, None, None, None, None))
