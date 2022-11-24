__all__ = ['API']

from flask_restful import Resource
from flask import request
import json
from dicttoxml import dicttoxml as dict_to_xml


class Response:

    def __init__(self, parser, version, method):
        self.status_code = 0
        self.message = ''

        self.method = method

        self.parser = None
        self.create_parser(parser, version)

    def create_parser(self, parser, version):
        try:
            parser = __import__(f'{__package__}.{parser}').__dict__[parser].__dict__[version]

        except ModuleNotFoundError:
            self.status_code = 404
            self.message = 'you wrote uncorrected parser?'

        except KeyError:
            self.status_code = 404
            self.message = 'you wrote uncorrected version for parser?'

        else:
            self.status_code = 200
            self.parser = parser

    @property
    def JSON(self):
        return json.dumps(self.parser.__dict__[self.method]())

    @property
    def XML(self):
        return json.dumps(dict_to_xml(self.parser.__dict__[self.method]()).decode('UTF-8'))


class API(Resource):

    def get(self, path):
        """method of API HTTP GET"""
        version, parser, *_ = path.split('/')
        req_format = request.values.get('format')

        version = version.upper()
        parser = parser.lower()
        req_format = req_format.upper()

        if not (parser and version and req_format):
            return json.dumps({'status_code': 404, 'message': 'you forgot to specify required arguments'})

        response = Response(parser, version, 'get')

        if response.status_code != 200:
            return json.dumps({'status_code': response.status_code, 'message': response.message})

        if req_format == 'JSON':
            return response.JSON

        elif req_format == 'XML':
            return response.XML

        else:
            return json.dumps({'status_code': 404, 'message': 'you wrote uncorrected format, JSON or XML'})
