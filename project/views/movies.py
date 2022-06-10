from flask import request
from flask_restx import Resource, Namespace, abort

from project.exceptions import ItemNotFound
from project.container import movie_service
from project.schemas import MovieSchema

movie_ns = Namespace('movies')

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()


@movie_ns.route('/')
class MoviesViews(Resource):
    @movie_ns.response(200, 'OK')
    @movie_ns.response(404, 'Movies not found')
    def get(self):
        """Get all movies"""

        page = request.args.get('page')
        status = request.args.get('status')

        filters = {
            "page": page,
            "status": status
        }
        try:
            all_movies = movie_service.get_all(filters)
            return movies_schema.dump(all_movies), 200
        except ItemNotFound:
            abort(404, message=f'Movies not found')


@movie_ns.route('/<int:mid>/')
class MovieView(Resource):
    @movie_ns.response(200, 'OK')
    @movie_ns.response(404, 'Movie not found')
    def get(self, mid):
        """Get movie by id"""
        try:
            movie = movie_service.get_one(mid)
            return movie_schema.dump(movie), 200
        except ItemNotFound:
            abort(404, f'Movie with id={mid} not found')
