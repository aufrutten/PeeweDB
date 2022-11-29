import pytest

from controllersDB import peeweeDB
import pathlib


class TestOfCreateDB:

    def test_main_case(self, tmp_path):
        path_database = tmp_path / 'test_database.db'
        path_to_files = pathlib.Path(__file__).parent.parent / 'test_reportMonaco' / 'data'

        peeweeDB.create_db(path_database, path_to_files)

        peeweeDB.database_proxy.initialize(peeweeDB.SqliteDatabase(path_database))
        database = peeweeDB.Driver

        driver = database.select().where(peeweeDB.Driver.abbr == 'DRR').get()
        assert driver.name == 'Daniel Ricciardo'

        driver.delete_instance()

        driver = peeweeDB.Driver.get_or_none(peeweeDB.Driver.abbr == 'DRR')
        assert driver is None

        peeweeDB.create_db(path_database, path_to_files)

        driver = peeweeDB.Driver.get_or_none(peeweeDB.Driver.abbr == 'DRR')
        assert driver is not None


