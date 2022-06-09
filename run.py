from project import DevelopmentConfig, create_app, db
from project.dao.models import Genre, Director, Movie, User


app = create_app(DevelopmentConfig)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Director": Director,
        "Movie": Movie,
        "User": User
    }


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='25000')
