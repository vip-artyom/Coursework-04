from sqlalchemy.exc import IntegrityError
from project import DevelopmentConfig, create_app, db, read_json
from project.dao.models import Director, Genre, Movie

app = create_app(DevelopmentConfig)

data = read_json("fixtures.json")

with app.app_context():
    for genre in data["genres"]:
        db.session.add(Genre(**genre))

    for director in data["directors"]:
        db.session.add(Director(**director))

    for movie in data["movies"]:
        db.session.add(Movie(**movie))

    try:
        db.session.commit()
        db.session.close()

    except IntegrityError:
        print("Fixtures already loaded")
