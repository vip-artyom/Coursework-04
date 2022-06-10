from flask import request
from flask_restx import Resource, Namespace, abort

from project.exceptions import ItemNotFound
from project.container import genre_service
from project.schemas import GenreSchema

genre_ns = Namespace('genres')

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


@genre_ns.route('/')
class GenresViews(Resource):
    @genre_ns.response(200, 'OK')
    @genre_ns.response(404, 'Genres not found')
    def get(self):
        """Get all genres"""

        page = request.args.get('page')
        status = request.args.get('status')

        filters = {
            "page": page,
            "status": status
        }
        try:
            genres = genre_service.get_all(filters)
            return genres_schema.dump(genres), 200
        except ItemNotFound:
            abort(404, message=f'Genres not found')


@genre_ns.route('/<int:gid>/')
class GenreView(Resource):
    @genre_ns.response(200, 'OK')
    @genre_ns.response(404, 'Genre not found')
    def get(self, gid):
        """Get genre by id"""
        try:
            genre = genre_service.get_one(gid)
            return genre_schema.dump(genre), 200
        except ItemNotFound:
            abort(404, f'Genre with id={gid} not found')
