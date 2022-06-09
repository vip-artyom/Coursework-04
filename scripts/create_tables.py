from project import DevelopmentConfig, create_app, db
from project.dao.models import director, genre, movie, user


app = create_app(DevelopmentConfig)

with app.app_context():
    db.drop_all()
    db.create_all()
