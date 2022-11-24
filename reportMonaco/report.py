import pathlib

from . import parser_files
from . import parser_cli


def print_to_console(list_to_print) -> str:
    """That is common format for print to console"""
    msg = [f'{num + 1:>3}. {name:<20}| {car:<25} | {result}' for num, (name, car, result) in enumerate(list_to_print)]
    return '\n\n'.join(msg)


def print_to_html(list_to_print) -> str:
    """That is common format for print into html"""
    msg = [f'{num + 1:>3}. {name:<20}| {car:<25} | {result}' for num, (name, car, result) in enumerate(list_to_print)]
    return '<br><br>'.join(msg)


def get_drivers(path_to_folder_with_data):
    data, results = build_report(path_to_folder_with_data)
    return [[num+1, data[abbreviation]["name"], abbreviation] for num, abbreviation in enumerate(data)]


def get_sorted_list_with_results(path_to_folder_with_data):
    list_with_results = []
    data, results = build_report(path_to_folder_with_data)
    sorted_results = [value for value in results.keys()]
    sorted_results.sort()

    for value in sorted_results:
        abbreviation = results[value]
        list_with_results.append([data[abbreviation]['name'], data[abbreviation]['car'], value])
    return list_with_results


def find_driver(driver, path_to_folder_with_data) -> list:
    """function for find driver in data"""

    if not isinstance(driver, str):
        raise TypeError('argument driver must be str')

    data, results = build_report(path_to_folder_with_data)

    for abbreviation in data:
        if data[abbreviation]['name'] == driver:
            car = data[abbreviation]['car']
            result = data[abbreviation]['result']
            return [[driver, car, result]]
    else:
        return [['Driver not found', 'Driver not found', 'Driver not found']]


def build_report(path_to_data):
    """main data collector, get raw data, and return full data"""

    if not (isinstance(path_to_data, str) or isinstance(path_to_data, pathlib.PosixPath)):
        raise TypeError('path should be str or pathlib.PosixPath')

    if isinstance(path_to_data, str):
        path_to_data = pathlib.PosixPath(path_to_data)

    return parser_files.Parser().get_data_from_folder(path_to_data)


def print_report(path_to_folder_with_data, html=False, reverse=False, driver=''):
    """incoming data handler"""
    if not (isinstance(path_to_folder_with_data, str) and isinstance(reverse, bool)):
        raise TypeError("first argument should be str, second bool")

    if driver:
        return print_to_console(find_driver(driver, path_to_folder_with_data))

    list_with_results = get_sorted_list_with_results(path_to_folder_with_data)
    if reverse is False:
        if html:
            return list_with_results
        else:
            return print_to_console(list_with_results)
    else:
        list_with_results.reverse()
        if html:
            return list_with_results
        else:
            return print_to_console(list_with_results)


def main():
    """program entry point"""
    arguments_cli = parser_cli.main()

    path_to_folder = arguments_cli['files']
    driver = arguments_cli['driver']
    reverse_mode = True if arguments_cli['desc'] else False

    print(print_report(path_to_folder, reverse=reverse_mode, driver=driver))


if __name__ == "__main__":  # pragma: no cover
    path_to_lib = (pathlib.PosixPath(__file__).parent.parent / 'tests' / 'test_reportMonaco' / 'data')
    # find_driver(123, str(path_to_lib))
    # get_drivers(path_to_lib)
    # main()
    # build_report(path_to_lib)
