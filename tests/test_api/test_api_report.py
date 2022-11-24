from app_main import app
import json
from bs4 import BeautifulSoup as parser_bs4


class TestV1:

    def test_JSON_case(self):
        response = app.test_client().get('http://127.0.0.1:5000/api/V1/report/?format=JSON')
        content = json.loads(response.json)
        result = {'name': 'Daniel Ricciardo',
                  'car': 'RED BULL RACING TAG HEUER',
                  'start': {'date': '2018-05-24', 'time': '12:14:12.054'},
                  'end': {'date': '2018-05-24', 'time': '12:11:24.067'},
                  'result': '0:02:47.987000'}
        assert response.status_code == 200
        assert content['DRR'] == result

    def test_XML_case(self):
        response = app.test_client().get('http://127.0.0.1:5000/api/V1/report/?format=XML')
        content = parser_bs4(json.loads(response.json), 'xml').find('DRR').find('name').contents[0]
        name_of_driver = 'Daniel Ricciardo'

        assert response.status_code == 200
        assert content == name_of_driver

    def test_with_other_format(self):
        response = app.test_client().get('http://127.0.0.1:5000/api/V1/report/?format=testJSON')
        content = json.loads(response.json)

        assert content['status_code'] == 404
        assert content['message'] == 'you wrote uncorrected format, JSON or XML'

    def test_if_module_not_exist(self):
        response = app.test_client().get('http://127.0.0.1:5000/api/V1/report_test/?format=JSON')
        content = json.loads(response.json)

        assert content['status_code'] == 404
        assert content['message'] == 'you wrote uncorrected parser?'

    def test_if_version_of_module_is_not_correct(self):
        response = app.test_client().get('http://127.0.0.1:5000/api/V999/report/?format=JSON')
        content = json.loads(response.json)

        assert content['status_code'] == 404
        assert content['message'] == 'you wrote uncorrected version for parser?'

    def test_if_user_forgot_required_arguments(self):
        response = app.test_client().get('http://127.0.0.1:5000/api/V1/report/')
        content = json.loads(response.json)

        assert content['status_code'] == 404
        assert content['message'] == 'you forgot to specify required arguments'



