from functools import lru_cache
import datetime
import pathlib


class Parser:

    def get_data_from_folder(self, path_to_folder) -> tuple[dict, dict]:
        required_files = ('abbreviations.txt',
                          'start.log',
                          'end.log')

        for req_file in required_files:
            path_to_file = path_to_folder / req_file

            if req_file == 'abbreviations.txt':
                data_abbr = {i[0]: {'name': i[1], 'car': i[2]} for i in self.parse_of_file(path_to_file)}
            elif req_file == 'start.log':
                data_start = {i[0]: {'start': {'date': i[1], 'time': i[2]}} for i in self.parse_of_file(path_to_file)}
            elif req_file == 'end.log':
                data_end = {i[0]: {'end': {'date': i[1], 'time': i[2]}} for i in self.parse_of_file(path_to_file)}

        raw_data = {abbr: data_abbr[abbr] | data_start[abbr] | data_end[abbr] for abbr in data_abbr}
        return self.compare_start_end_time(raw_data)

    @staticmethod
    def read_file(path_to_file):
        with open(path_to_file) as file:
            if path_to_file.name == 'abbreviations.txt':
                return [line.rstrip().split('_') for line in file if line != '\n']

            elif path_to_file.name in ('start.log', 'end.log'):
                return [
                    [line[:3], line.split('_')[0][3:], line.rstrip().split('_')[1]] for line in file if line != '\n'
                ]

    @lru_cache(maxsize=None)
    def parse_of_file(self, path_to_file) -> list:
        """
        function parse file with abbreviations
        get file
        :return (abbreviation, name, car)"""
        if not (isinstance(path_to_file, str) or isinstance(path_to_file, pathlib.PosixPath)):
            raise TypeError("the object being passed must be str of 'pathlib.PosixPath'")
        if not isinstance(path_to_file, pathlib.PosixPath):
            path_to_file = pathlib.PosixPath(path_to_file)

        if path_to_file.is_file():
            return self.read_file(path_to_file)
        else:
            raise FileNotFoundError(f'file {path_to_file} not exist')

    @staticmethod
    def compare_start_end_time(data) -> tuple[dict, dict]:
        """compare time in start and in end, and take result"""
        if not isinstance(data, dict):
            raise TypeError

        dict_with_results = {}
        for abbreviation in data:
            start = "{}_{}".format(
                data[abbreviation]['start']['date'],
                data[abbreviation]['start']['time']
            )
            end = "{}_{}".format(
                data[abbreviation]['end']['date'],
                data[abbreviation]['end']['time']
            )

            start_time = datetime.datetime.strptime(start, '%Y-%m-%d_%H:%M:%S.%f')
            end_time = datetime.datetime.strptime(end, '%Y-%m-%d_%H:%M:%S.%f')
            result = str(abs(end_time - start_time))

            data[abbreviation]['result'] = result
            dict_with_results[result] = abbreviation
        return data, dict_with_results
