import sqlite3
import pathlib


class SQLite:

    def __init__(self, name_of_db):
        path_to_database = pathlib.Path(__file__).parent.parent / 'database'
        self.connection = sqlite3.connect(path_to_database/name_of_db)
        self.cursor = self.connection.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS "drivers"
         ("abbr" CHAR UNIQUE, "name" CHAR, "car" CHAR, "result" TIME)""")
        self.connection.commit()

    def get_all_drivers(self):
        result = self.cursor.execute("""SELECT * FROM "drivers";""")
        return result.fetchall()

    def get_driver_by_abbr(self, abbr):
        request = f'SELECT * FROM "drivers" WHERE "abbr" == "{abbr}"'
        return self.cursor.execute(request).fetchone()

    def insert_driver(self, abbr, name, car, result):
        request = f'INSERT INTO "drivers" VALUES ("{abbr}", "{name}", "{car}", "{result}")'

        if not self.get_driver_by_abbr(abbr):  # check if abbr not exist in table
            self.cursor.execute(request)
            self.connection.commit()
            return 1
        else:
            return 0


if __name__ == '__main__':  # pragma: no cover
    db = SQLite('Test.db')
    print(db.get_all_drivers())
    # db.get_driver_by_abbr('SIV2')
    db.insert_driver('SIV', 'Ihor', 'R34', '0.1')
