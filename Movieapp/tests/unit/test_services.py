from datetime import date

import pytest

from CS235Flix.authentication.services import AuthenticationException
from CS235Flix.movies import services as movie_services
from CS235Flix.authentication import services as auth_services
from CS235Flix.movies.services import NonExistentMovieException


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_review(in_memory_repo):
    movie_id = 3
    review_text = 'The loonies are stripping the supermarkets bare!'
    username = 'fmercury'

    # Call the service layer to add the comment.
    movie_services.add_review(movie_id, review_text, username, in_memory_repo)

    # Retrieve the comments for the article from the repository.
    reviews_as_dict = movie_services.get_reviews_for_movie(movie_id, in_memory_repo)

    # Check that the comments include a comment with the new comment text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    movie_id = 7
    review_text = "COVID-19 - what's that?"
    username = 'fmercury'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movie_services.NonExistentMovieException):
        movie_services.add_review(movie_id, review_text, username, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    movie_id = 3
    review_text = 'The loonies are stripping the supermarkets bare!'
    username = 'gmichael'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movie_services.UnknownUserException):
        movie_services.add_review(movie_id, review_text, username, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_id = 2

    movie_as_dict = movie_services.get_movie(movie_id, in_memory_repo)

    assert movie_as_dict['id'] == movie_id
    assert movie_as_dict['year'] == date.fromisoformat('2012')
    assert movie_as_dict['title'] == 'Prometheus'
    assert movie_as_dict['description'] == 'Following clues to the origin of mankind, a team finds a structure on a distant moon, but they soon realize they are not alone.'
    assert movie_as_dict['director'] == 'Ridley Scott'
    assert movie_as_dict['runtime_minutes'] == 124
    assert len(movie_as_dict['reviews']) == 0
    assert movie_as_dict['rating'] == 7
    assert movie_as_dict['votes'] == 485820
    assert movie_as_dict['revenue_millions'] == 126.46
    assert movie_as_dict['meta_score'] == 65

   # genre_names = [dictionary['name'] for dictionary in movie_as_dict['genre']]
   # assert 'Adventure' in genre_names
   # assert 'Mystery' in genre_names
   # assert 'Sci-Fi' in genre_names
    #actor_names = [dictonary['name'] for dictionary in movie_as_dict['actor']]
   # assert 'Noomi Rapace' in actor_names
    #assert 'Logan Marshall-Green' in actor_names
    #assert 'Michael Fassbender' in actor_names
    #assert 'Charlize Theron' in actor_names


def test_cannot_get_movie_with_non_existent_id(in_memory_repo):
    movie_id = 7

    # Call the service layer to attempt to retrieve the Article.
    with pytest.raises(movie_services.NonExistentMovieException):
        movie_services.get_movie(movie_id, in_memory_repo)


