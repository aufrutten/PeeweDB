import argparse
from controllersDB import peeweeDB


def main(path_to_database):
    cli = argparse.ArgumentParser()
    cli.add_argument("--files",
                     type=str,
                     help="pointer of folder")  # add --files argument

    cli = cli.parse_args().__dict__

    if cli.get('files'):
        peeweeDB.create_db(path_to_database,
                           cli['files'])
