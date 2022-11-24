import pytest

from reportMonaco import parser_files


class TestParser:

    def test_parse_of_file_atypical_case(self, tmp_path):
        with pytest.raises(TypeError):
            parser_files.Parser().parse_of_file(123)
        with pytest.raises(FileNotFoundError):
            parser_files.Parser().parse_of_file(tmp_path)

    def test_parse_of_file(self, tmp_path_with_files):
        result = parser_files.Parser().parse_of_file(str(tmp_path_with_files/'abbreviations.txt'))
        result_mem = [['SVF', 'Sebastian Vettel', 'FERRARI'], ['LHM', 'Lewis Hamilton', 'MERCEDES']]
        assert result == result_mem

    def test_compare_start_end_time(self):
        with pytest.raises(TypeError):
            parser_files.Parser().compare_start_end_time(123)

