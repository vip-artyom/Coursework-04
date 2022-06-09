from .dao import GenreDAO, DirectorDAO, MovieDAO, UserDAO
from .dao.models import Genre, Director, Movie, User
from project.services import GenresService, UserService, AuthService, DirectorsService, MoviesService
from project.setup_db import db

movie_dao = MovieDAO(session=db.session, model=Movie)
director_dao = DirectorDAO(session=db.session, model=Director)
genre_dao = GenreDAO(session=db.session, model=Genre)
user_dao = UserDAO(session=db.session, model=User)


movie_service = MoviesService(dao=movie_dao)
director_service = DirectorsService(dao=director_dao)
genre_service = GenresService(dao=genre_dao)
user_service = UserService(dao=user_dao)
auth_service = AuthService(user_service=user_service)
