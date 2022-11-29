import pathlib
from controllersDB import peeweeDB


__doc_for_developers__ = \
    """
    style of write is SOLID, close for modification, and open for adding
    
    if you wanna add the new modification, you have create new class in style V{0} - number of version
    and class should have methods which will understood other users of that API
    
    API class in __init__ can parse url which take, /api/{version}/{parser}/{format}
    
    version - V1; V2; V3... V- must be in uppercase
    parser - report; spam... should have the same name what and module  
    available format that - JSON and XML: ?format=JSON; ?format=XML
    
    all version must have small documentation of class
    """


class V1:
    __parser_name__ = 'report'
    __api_version__ = 'V1'
    __doc__ = """That parser for parsing data from reportMonaco, version 1"""

    @staticmethod
    def get() -> dict:
        """api get request of HTTP, getting data from reportMonaco"""
        database = peeweeDB.Driver.select().order_by(peeweeDB.Driver.result)
        data = {n.abbr: {'name': n.name, 'car': n.car, 'result': str(n.result)} for n in database}
        return data


if __name__ == "__main__":  # pragma: no cover
    path = pathlib.Path(__file__).parent.parent / 'database' / 'drivers.db'
    peeweeDB.database_proxy.initialize(peeweeDB.SqliteDatabase(path))
    for key, value in V1.get().items():
        print(key, value['result'])
