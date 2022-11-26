import pathlib

from peewee import *

from reportMonaco import report

path_to_database = pathlib.Path(__file__).parent.parent / 'database'
db = SqliteDatabase(path_to_database/'drivers.db')


class Driver(Model):
    abbr = TextField(unique=True)
    name = TextField(null=False)
    car = TextField(null=False)
    result = TimeField(null=False)

    class Meta:
        database = db
        table_name = 'drivers'
        order_by = 'result'


def create_db(path):
    if not (path/'drivers.db').exists():

        path_to_data = pathlib.Path(__file__).parent.parent / 'tests' / 'test_reportMonaco' / 'data'
        data, _ = report.build_report(path_to_data)

        Driver._meta.database = SqliteDatabase(path / 'drivers.db')
        db.create_tables([Driver])
        for abbr in data:
            name = data[abbr]['name']
            car = data[abbr]['car']
            result = data[abbr]['result']

            Driver(abbr=abbr, name=name, car=car, result=result).save()
