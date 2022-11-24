from app_main import app
from bs4 import BeautifulSoup as parser_bs4


def test_main_glory_hole():
    response = app.test_client().get('/report/')
    content = parser_bs4(response.data, 'html.parser').find_all('tr')[0].text

    assert response.status_code == 200
    assert content == '\n0\nSebastian Vettel\nFERRARI\n0:01:04.415000\n'


class TestRouteDrivers:

    def test_route_drivers(self):
        response = app.test_client().get('/report/drivers/')
        content = parser_bs4(response.data, 'html.parser').find_all('tr')[0].text

        assert response.status_code == 200
        assert content == '\n1\nDaniel Ricciardo\nDRR\n'

    def test_with_reverse_mode(self):
        response = app.test_client().get('/report/drivers/?order=desc')
        content = parser_bs4(response.data, 'html.parser').find_all('tr')[0].text

        assert response.status_code == 200
        assert content == '\n19\nKevin Magnussen\nKMH\n'

    def test_with_abbr(self):
        response = app.test_client().get('/report/drivers/?driver=NHR')
        content = parser_bs4(response.data, 'html.parser').find_all('div')[0].text

        assert response.status_code == 200
        assert content == '\n        Nico Hulkenberg | RENAULT | 0:01:13.065000\n    '

