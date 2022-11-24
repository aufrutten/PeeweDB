import argparse
from typing import Any
import os


class FolderNotFoundError(Exception):

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'FolderNotFound, {0}'.format(self.message)
        else:
            return 'FolderNotFound has been raised'


def check_correct_files_in_folder(path_to_folder) -> bool:
    """checking required files in folder"""
    required_files = ('abbreviations.txt',
                      'start.log',
                      'end.log')
    if not isinstance(path_to_folder, str):
        raise TypeError("path to folder must be string")
    files_in_folder = [files[2] for files in os.walk(path_to_folder)][0]  # getting all files in folder

    for req_file in required_files:
        if req_file not in files_in_folder:
            raise FileNotFoundError(f'required file not in {path_to_folder}')
    else:
        return True


def check_files_in_folder(path: str) -> bool:
    """checking if path is folder and required files"""
    if not isinstance(path, str):
        raise TypeError('argument must be str')

    if os.path.isdir(path):
        return check_correct_files_in_folder(path_to_folder=path)
    else:
        raise FolderNotFoundError('you wrote not correct path to folder')


def main() -> dict[str, Any]:
    """
    function for parse our command lines
    """
    parser_cli = argparse.ArgumentParser(description="Parse program for data from Monaco")
    parser_cli.add_argument("--files",
                            type=str,
                            help="pointer of folder")  # add --files argument

    parser_cli.add_argument("--driver",
                            type=str,
                            help="for search driver in data")  # add --driver argument

    parser_cli.add_argument("--asc",
                            action="store_true",
                            help="string in sort")  # add --asc argument

    parser_cli.add_argument("--desc",
                            action="store_true",
                            help="string sorted, but in reverse")  # add --desc argument

    cli_args = parser_cli.parse_args()  # getting all arguments in CLI
    if cli_args.files is None:
        raise FolderNotFoundError("you didn't write path to folder")

    if check_files_in_folder(path=cli_args.files):
        return cli_args.__dict__

