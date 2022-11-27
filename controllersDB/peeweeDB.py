import pathlib

from peewee import *

from reportMonaco import report


database_proxy = DatabaseProxy()


class Driver(Model):
    abbr = TextField(unique=True)
    name = TextField(null=False)
    car = TextField(null=False)
    result = TimeField(null=False)

    class Meta:
        database = database_proxy
        table_name = 'drivers'
        order_by = 'result'


def create_db(path_DB, path_to_files_with_data):
    if not path_DB.exists():

        data, _ = report.build_report(path_to_files_with_data)

        database_proxy.initialize(SqliteDatabase(path_DB))
        database_proxy.create_tables([Driver])

        for abbr in data:
            name = data[abbr]['name']
            car = data[abbr]['car']
            result = data[abbr]['result']

            Driver(abbr=abbr, name=name, car=car, result=result).save()
