import csv
import os
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from CS235Flix.adapters.repository import AbstractRepository, RepositoryException
from CS235Flix.domain.model import  User, Movie, Genre, Actor, Director, Review, make_genre_association, make_actor_association, make_director_association, make_review


class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self._tags = list()
        self._users = list()
        self._comments = list()
        self._movies = list()
        self._movies_index = dict()
        self._genres = list()
        self._actors = list()
        self._directors = list()
        self._reviews = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.username == username), None)

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)
        self._movies_index[movie.id] = movie

    def get_movie(self, id: int) -> Movie:
        movie = None
        try:
            movie = self._movies_index[id]
        except KeyError:
            pass # Ignore exception and return None.

        return movie

    def get_number_of_movies(self):
        return len(self._movies)

    def get_movie_ids_by_genre(self, selected_genre: str):
        existing_genre = next((genre for genre in self._genres if genre.genre_name == selected_genre), 'end')
        if existing_genre == 'end':
            movie_ids =list()
        else:
            movie_ids = [movie.id for movie in existing_genre.genre_of_movies]
        return movie_ids

    def get_movie_ids_by_director(self, selected_director: str):
        existing_director = next((director for director in self._directors if director.director_name == selected_director), 'end')
        if existing_director == 'end':
            movie_ids = list()
        else:
            movie_ids = [movie.id for movie in existing_director.directed_movies]

        return movie_ids

    def get_movie_ids_by_actor(self, selected_actor: str):
        existing_actor = next((actor for actor in self._actors if actor.actor_name == selected_actor),'end')
        if existing_actor == 'end':
            movie_ids = list()
        else:
            movie_ids = [movie.id for movie in existing_actor.acted_movies]
        return movie_ids

    def get_movies_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent Movie ids in the repository.
        existing_ids = []
        for movie_id in id_list:
            if movie_id in self._movies_index:
                existing_ids.append(movie_id)

        # Fetch the Movies.
        movies = [self._movies_index[movie_id] for movie_id in existing_ids]
        return movies

    def get_all_movie_ids(self):
        movieids = [movie.id for movie in self._movies]
        return movieids

    def add_genre(self, genre: Genre):
        self._genres.append(genre)

    def get_genres(self) -> List[Genre]:
        return self._genres

    def add_actor(self, actor: Actor):
        self._actors.append(actor)

    def get_actors(self) -> List[Actor]:
        return self._actors

    def add_director(self, director: Director):
        self._directors.append(director)

    def get_directors(self) -> List[Director]:
        return self._directors

    def add_review(self, review: Review):
        super().add_review(review)
        self._reviews.append(review)

    def get_reviews(self):
        return self._reviews

    # Helper method to return article index.
#    def article_index(self, article: Article):
     #   index = bisect_left(self._articles, article)
      #  if index != len(self._articles) and self._articles[index].date == article.date:
        #    return index
       # raise ValueError


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for line in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            username=line[1],
            password=generate_password_hash(line[2])
        )
        repo.add_user(user)
        users[line[0]] = user
    return users


def load_reviews(data_path: str, repo: MemoryRepository, users):
    for line in read_csv_file(os.path.join(data_path, 'reviews.csv')):
        if line[4] is None:
            review = make_review(
                review_text=line[3],
                user=users[line[1]],
                movie=repo.get_movie(int(line[2])),
                timestamp=line[4]
            )
            repo.add_review(review)

def load_movie_data(data_path: str, repo: MemoryRepository):
    actors = dict()
    genres = dict()
    directors = dict()

    for line in read_csv_file(os.path.join(data_path, 'Data1000Movies.csv')):
        movie_id = line[0]
        movie_genres = line[2].split(',')
        movie_director = line[4].strip()
        movie_actors = line[5].split(',')

        for actor in movie_actors:
            actor = actor.strip()
            if actor not in actors.keys():
                actors[actor] = list()
            actors[actor].append(movie_id)

        for genre in movie_genres:
            if genre not in genres.keys():
                genres[genre] = list()
            genres[genre].append(movie_id)

        if movie_director not in directors.keys():
            directors[movie_director] = list()
        directors[movie_director].append(movie_id)

        movie = Movie(
            title=line[1], description=line[3], year=line[6], runtime_minutes=line[7], rating=line[8],
            votes=line[9], revenue_millions=line[10], meta_score=line[11], id=movie_id
            )
        repo.add_movie(movie)

    for actor in actors.keys():
        actorobj = Actor(actor)
        for movie_id in actors[actor]:
            movie = repo.get_movie(movie_id)
            make_actor_association(movie, actorobj)
        repo.add_actor(actorobj)

    for genre in genres.keys():
        genreobj = Genre(genre)
        for movie_id in genres[genre]:
            movie = repo.get_movie(movie_id)
            make_genre_association(movie, genreobj)
        repo.add_genre(genreobj)

    for director in directors.keys():
        directorobj = Director(director)
        for movie_id in directors[director]:
            movie = repo.get_movie(movie_id)
            make_director_association(movie, directorobj)
        repo.add_director(directorobj)

def populate(data_path: str, repo: MemoryRepository):
    # Load movie data into the repository.
    load_movie_data(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load reviews into the repository.
    load_reviews(data_path, repo, users)
