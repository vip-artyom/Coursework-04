from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    password = fields.Str(load_only=True)
    name = fields.Str()
    surname = fields.Str()
    favourite_genre = fields.Int()
