from controllersDB import peeweeDB


class TestOfCreateDB:

    def test_main_case(self, tmp_path):
        peeweeDB.create_db(tmp_path)
        peeweeDB.Driver._meta.database = peeweeDB.SqliteDatabase(tmp_path / 'drivers.db')
        peeweeDB.Driver(abbr='TEST', name='TEST', car='TEST', result='TEST').save()

        request = peeweeDB.Driver.select().where(peeweeDB.Driver.abbr == 'TEST').get()
        assert request.abbr == 'TEST'
