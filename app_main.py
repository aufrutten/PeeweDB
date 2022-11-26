import pathlib

from flask import Flask
from flask_restful import Api

from views import simple_page
from api import API
from controllersDB import peeweeDB


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        FLASK_DEBUG=True,
        instance_relative_config=True,
    )
    app.config['path_to_folder'] = str(pathlib.PosixPath(__file__).parent / 'tests' / 'test_reportMonaco' / 'data')
    peeweeDB.create_db(pathlib.Path(__file__).parent/'database')
    app.config['drivers'] = peeweeDB.Driver
    return app


app = create_app()
app.register_blueprint(simple_page)

api_of_app = Api(app)
api_of_app.add_resource(API, '/api/<path:path>')

create_app()

if __name__ == '__main__':  # pragma: no cover
    app.run(debug=True)
