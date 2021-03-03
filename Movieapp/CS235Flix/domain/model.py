from datetime import date, datetime
from typing import List, Iterable


class User:
    def __init__(
            self, username: str, password: str
    ):
        self._username: str = username
        self._password: str = password
        self._reviews: List[Review] = list()

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def reviews(self) -> Iterable['Review']:
        return iter(self._reviews)

    def add_review(self, review: 'Review'):
        self._reviews.append(review)

    def __repr__(self) -> str:
        return f'<User {self._username} {self._password}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return other._username == self._username


class Review:
    def __init__(
            self, user: User, movie: 'Movie', review: str, timestamp: datetime
    ):
        self._user: User = user
        self._movie: Movie = movie
        self._review: Review = review
        self._timestamp: datetime = timestamp

    @property
    def user(self) -> User:
        return self._user

    @property
    def movie(self) -> 'Movie':
        return self._movie

    @property
    def review(self) -> str:
        return self._review

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return other._user == self._user and other._movie == self._movie and other._review == self._review and other._timestamp == self._timestamp


class Movie:
    def __init__(
            self, title: str, description: str,
            year: int, runtime_minutes: int, rating: float, votes: int, revenue_millions: float, meta_score: int,
            id: int = None
    ):
        self._id: int = id
        self._title: str = title
        self._description: str = description
        self._year: int = year
        self._runtime_minutes: int = runtime_minutes
        self._rating: float = rating
        self._votes: int = votes
        self._revenue_millions: float = revenue_millions
        self._meta_score: int = meta_score
        self._reviews: List[Review] = list()
        self._genres: List[Genre] = list()
        self._actors: List[Actor] = list()
        self._directors: List[Director] = list()

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def year(self) -> int:
        return self._year

    @property
    def runtime_minutes(self) -> int:
        return self._runtime_minutes

    @property
    def rating(self) -> float:
        return self._rating

    @property
    def votes(self) -> int:
        return self._votes

    @property
    def revenue_millions(self) -> float:
        return self._revenue_millions

    @property
    def meta_score(self) -> int:
        return self._meta_score

    @property
    def reviews(self) -> Iterable[Review]:
        return iter(self._reviews)

    @property
    def number_of_reviews(self) -> int:
        return len(self._reviews)

    @property
    def genres(self) -> Iterable['Genre']:
        return iter(self._genres)

    @property
    def number_of_genres(self) -> int:
        return len(self._genres)

    @property
    def actors(self) -> Iterable['Actor']:
        return iter(self._actors)

    @property
    def number_of_actors(self) -> int:
        return len(self._actors)

    @property
    def directors(self) -> Iterable['Director']:
        return iter(self._directors)

    @property
    def number_of_directors(self) -> int:
        return len(self._directors)

    def has_genre(self, genre: 'Genre'):
        return genre in self._genres

    def is_genres(self) -> bool:
        return len(self._genres) > 0

    def has_actor(self, actor: 'Actor'):
        return actor in self._actors

    def is_actors(self) -> bool:
        return len(self._actors) > 0

    def has_director(self, director: 'Director'):
        return director in self._directors

    def is_director(self) -> bool:
        return len(self._directors) > 0

    def add_review(self, review: Review):
        self._reviews.append(review)

    def add_genre(self, genre: 'Genre'):
        self._genres.append(genre)

    def add_actor(self, actor: 'Actor'):
        self._actors.append(actor)

    def add_director(self, director: 'Director'):
        self._directors.append(director)

    def __repr__(self):
        return f'<Movie {self._year} {self._title}>'

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        return (
                other._title == self._title and
                other._description == self._description and
                other._year == self._year and
                other._runtime_minutes == self._runtime_minutes and
                other._rating == self._rating and
                other._votes == self._votes and
                other._revenue_millions == self._revenue_millions and
                other._meta_score == self._meta_score
        )

    def __lt__(self, other):
        return float(self._rating) < float(other._rating)


class Genre:
    def __init__(
            self, genre_name: str
    ):
        self._genre_name: str = genre_name
        self._genre_of_movies: List[Movie] = list()

    @property
    def genre_name(self) -> str:
        return self._genre_name

    @property
    def genre_of_movies(self) -> Iterable[Movie]:
        return iter(self._genre_of_movies)

    @property
    def number_of_genre_movies(self) -> int:
        return len(self._genre_of_movies)

    def is_applied_to(self, movie: Movie) -> bool:
        return movie in self._genre_of_movies

    def add_movie(self, movie: Movie):
        self._genre_of_movies.append(movie)

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False
        return other._genre_name == self._genre_name


class Actor:
    def __init__(
            self, actor_name: str
    ):
        self._actor_name: str = actor_name
        self._acted_movies: List[Movie] = list()

    @property
    def actor_name(self) -> str:
        return self._actor_name

    @property
    def acted_movies(self) -> Iterable[Movie]:
        return iter(self._acted_movies)

    @property
    def number_of_acted_movies(self) -> int:
        return len(self._acted_movies)

    def is_applied_to(self, movie: Movie) -> bool:
        return movie in self._acted_movies

    def add_movie(self, movie: Movie):
        self._acted_movies.append(movie)

    def __eq__(self, other):
        if not isinstance(other, Actor):
            return False
        return other._actor_name == self._actor_name


class Director:
    def __init__(
            self, director_name: str
    ):
        self._director_name: str = director_name
        self._directed_movies: List[Movie] = list()

    @property
    def director_name(self) -> str:
        return self._director_name

    @property
    def directed_movies(self) -> Iterable[Movie]:
        return iter(self._directed_movies)

    @property
    def number_of_director_movies(self) -> int:
        return len(self._directed_movies)

    def is_applied_to(self, movie: Movie) -> bool:
        return movie in self._directed_movies

    def add_movie(self, movie: Movie):
        self._directed_movies.append(movie)

    def __eq__(self, other):
        if not isinstance(other, Director):
            return False
        return other._director_name == self._director_name


class ModelException(Exception):
    pass


def make_review(review_text: str, user: User, movie: Movie, timestamp: datetime = datetime.today()):
    review = Review(user, movie, review_text, timestamp)
    user.add_review(review)
    movie.add_review(review)

    return review


def make_genre_association(movie: Movie, genre: Genre):
    if genre.is_applied_to(movie):
        raise ModelException(f'Genre {genre.genre_name} already applied to Movie "{movie.title}"')
    movie.add_genre(genre)
    genre.add_movie(movie)


def make_actor_association(movie: Movie, actor: Actor):
    if actor.is_applied_to(movie):
        raise ModelException(f'Actor {actor.actor_name} already applied to Movie "{movie.title}"')
    movie.add_actor(actor)
    actor.add_movie(movie)


def make_director_association(movie: Movie, director: Director):
    movie.add_director(director)
    director.add_movie(movie)