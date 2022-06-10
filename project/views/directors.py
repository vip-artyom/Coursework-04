from flask import request
from flask_restx import Resource, Namespace, abort
from project.exceptions import ItemNotFound
from project.container import director_service
from project.schemas import DirectorSchema

director_ns = Namespace('directors')

directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()


@director_ns.route('/')
class DirectorsViews(Resource):
    @director_ns.response(200, 'Success')
    @director_ns.response(404, 'Not found')
    def get(self):
        """Get all directors"""
        page = request.args.get('page')
        status = request.args.get('status')

        filters = {
            "page": page,
            "status": status
        }
        try:
            directors = director_service.get_all(filters)
            return directors_schema.dump(directors), 200
        except ItemNotFound:
            abort(404)


@director_ns.route('/<int:did>/')
class DirectorView(Resource):
    @director_ns.response(200, 'Success')
    @director_ns.response(404, 'Not found')
    def get(self, did):
        """Get director by id"""
        try:
            director = director_service.get_one(did)
            return director_schema.dump(director), 200
        except ItemNotFound:
            abort(404, f'Director with id={did} not found')
