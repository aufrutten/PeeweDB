from unittest.mock import patch
import pytest

import pathlib

from reportMonaco import report


class TestFindDriver:

    def test_with_atypical_argument(self, tmp_path_with_files):
        with pytest.raises(TypeError):
            report.find_driver(1.2, tmp_path_with_files)

    def test_to_find_driver(self, tmp_path_with_files):
        result = report.find_driver('Sebastian Vettel', tmp_path_with_files)
        assert result == [['Sebastian Vettel', 'FERRARI', '0:01:04.415000']]

    def test_while_driver_not_found(self, tmp_path_with_files):
        result = report.find_driver('Ihor', tmp_path_with_files)
        assert result == [['Driver not found', 'Driver not found', 'Driver not found']]


class TestPrintToConsole:

    def test_print_function(self):
        test_list = [
            ['Aufrutten Ihor', 'AUDI A5', '0:01:03.321'],
            ['Ihor Aufrutten', 'AUDI A6 ALL ROAD', '0:01:03:132']]
        result = report.print_to_console(test_list)
        path_to_results = (pathlib.Path(__file__).parent / 'results_for_assert/print_report_print_console.txt')
        with open(path_to_results, 'r') as file:
            assert result == file.read()


class TestPrintToHTML:

    def test_print_function(self):
        test_list = [['Aufrutten Ihor', 'AUDI A5', '0:01:03.321'],
                     ['Ihor Aufrutten', 'AUDI A6 ALL ROAD', '0:01:03:132']]
        result = report.print_to_html(test_list)
        path_to_results = (pathlib.Path(__file__).parent / 'results_for_assert/print_report_print_html.txt')
        with open(path_to_results, 'r') as file:
            assert result == file.read()


class TestGetDrivers:

    def test_get_drivers(self, tmp_path_with_files):
        result_of_function = report.get_drivers(path_to_folder_with_data=tmp_path_with_files)
        assert result_of_function == [[1, 'Sebastian Vettel', 'SVF'], [2, 'Lewis Hamilton', 'LHM']]


class TestBuildReport:

    def test_with_atypical_argument(self):
        with pytest.raises(TypeError):
            report.build_report(123)

    def test_with_argument_str(self, tmp_path_with_files):
        result_zero = {'LHM': {'car': 'MERCEDES',
                               'end': {'date': '2018-05-24', 'time': '12:11:32.585'},
                               'name': 'Lewis Hamilton',
                               'result': '0:06:47.540000',
                               'start': {'date': '2018-05-24', 'time': '12:18:20.125'}},
                       'SVF': {'car': 'FERRARI',
                               'end': {'date': '2018-05-24', 'time': '12:04:03.332'},
                               'name': 'Sebastian Vettel',
                               'result': '0:01:04.415000',
                               'start': {'date': '2018-05-24', 'time': '12:02:58.917'}}
                       }

        result_one = {'0:01:04.415000': 'SVF', '0:06:47.540000': 'LHM'}
        result_of_function = report.build_report(str(tmp_path_with_files))
        assert result_of_function[0] == result_zero
        assert result_of_function[1] == result_one


class TestPrintReport:

    def test_with_atypical_argument(self):
        with pytest.raises(TypeError):
            report.print_report(123, {})

    def test_with_correct_argument(self, tmp_path_with_files):
        result = report.print_report(str(tmp_path_with_files))
        path_to_results = (pathlib.Path(__file__).parent / 'results_for_assert/print_report.txt')
        with open(path_to_results, 'r') as file:
            assert str(result) == file.read()
            # file.write(str(result))

    def test_with_reverse_mode(self, tmp_path_with_files):
        result = report.print_report(str(tmp_path_with_files), reverse=True)
        path_to_results = (pathlib.Path(__file__).parent / 'results_for_assert/print_report_reverse.txt')
        with open(path_to_results, 'r') as file:
            assert str(result) == file.read()
            # file.write(str(result))

    def test_print_to_html(self, tmp_path_with_files):
        result = report.print_report(str(tmp_path_with_files), html=True)
        path_to_results = (pathlib.Path(__file__).parent / 'results_for_assert/test_print_to_html.txt')
        with open(path_to_results, 'r') as file:
            assert str(result) == file.read()
            # file.write(str(result))

    def test_print_to_html_reverse(self, tmp_path_with_files):
        result = report.print_report(str(tmp_path_with_files), reverse=True, html=True)
        path_to_results = (pathlib.Path(__file__).parent / 'results_for_assert/test_print_to_html_reverse.txt')
        with open(path_to_results, 'r') as file:
            assert str(result) == file.read()
            # file.write(str(result))


class TestMain:

    @patch('reportMonaco.parser_cli.main')
    def test_main(self, mock_func, tmp_path_with_files, capsys):

        # first case
        mock_func.return_value = {'files': str(tmp_path_with_files), 'driver': None, 'desc': None}
        report.main()
        out, err = capsys.readouterr()
        assert str(out).split('\n\n')[0] == '  1. Sebastian Vettel    | FERRARI                   | 0:01:04.415000'

        # second case
        mock_func.return_value = {'files': str(tmp_path_with_files), 'driver': None, 'desc': True}
        report.main()
        out, err = capsys.readouterr()
        assert str(out).split('\n\n')[0] == '  1. Lewis Hamilton      | MERCEDES                  | 0:06:47.540000'

        # third case
        mock_func.return_value = {'files': str(tmp_path_with_files), 'driver': 'Lewis Hamilton', 'desc': True}
        report.main()
        out, err = capsys.readouterr()
        assert out == '  1. Lewis Hamilton      | MERCEDES                  | 0:06:47.540000\n'

