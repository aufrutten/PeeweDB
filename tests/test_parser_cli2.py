from unittest.mock import patch, MagicMock
import parser_cli
import pathlib
from controllersDB import peeweeDB


class TestCLI:

    @patch('parser_cli.argparse.ArgumentParser.parse_args')
    def test_main(self, mock_argparse, tmp_path):
        path_database = tmp_path / 'test_database.db'
        path_to_files = pathlib.Path(__file__).parent.parent / 'tests' / 'test_reportMonaco' / 'data'
        mock_argparse.return_value = MagicMock(files=path_to_files)
        parser_cli.main(path_database)

        peeweeDB.database_proxy.initialize(peeweeDB.SqliteDatabase(path_database))
        database = peeweeDB.Driver

        driver = database.select().where(peeweeDB.Driver.abbr == 'DRR').get()
        assert driver.name == 'Daniel Ricciardo'
