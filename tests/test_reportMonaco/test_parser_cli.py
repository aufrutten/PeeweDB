from unittest.mock import patch, MagicMock
import pytest
import os

from reportMonaco import parser_cli


def test_file_not_found_error():
    with pytest.raises(parser_cli.FolderNotFoundError):
        raise parser_cli.FolderNotFoundError()

    assert str(parser_cli.FolderNotFoundError()) == 'FolderNotFound has been raised'
    assert str(parser_cli.FolderNotFoundError('Test raise')) == 'FolderNotFound, Test raise'


class TestCheckCorrectFilesInFolder:
    """Test func Check Correct Files in Folder"""

    def test_with_another_argument(self):
        """test with another arguments which not str"""
        with pytest.raises(TypeError):
            parser_cli.check_correct_files_in_folder(123)

    def test_with_typical_case(self, tmp_path_with_files):
        assert parser_cli.check_correct_files_in_folder(str(tmp_path_with_files)) is True

    def test_with_atypical_case(self, tmp_path_with_files):
        with pytest.raises(FileNotFoundError):
            """check if not exist one req file in folder"""
            os.remove(f"{tmp_path_with_files}/abbreviations.txt")
            parser_cli.check_correct_files_in_folder(str(tmp_path_with_files))


class TestCheckFilesInFolder:
    """test function check_files_in_folder"""

    def test_with_another_argument(self):
        with pytest.raises(TypeError):
            parser_cli.check_files_in_folder(123)

    @patch('reportMonaco.parser_cli.check_correct_files_in_folder')
    def test_with_exist_folder(self, mock_check_correct_files_in_folder, tmp_path):
        mock_check_correct_files_in_folder.return_value = True
        assert parser_cli.check_files_in_folder(str(tmp_path)) is True

    def test_with_not_exits_folder(self, tmp_path_with_files):
        with pytest.raises(parser_cli.FolderNotFoundError):
            parser_cli.check_files_in_folder(f'{tmp_path_with_files}/abbreviations.txt')


class TestMain:

    @patch('reportMonaco.parser_cli.argparse.ArgumentParser.parse_args')
    def test_if_folder_is_none(self, mock_argparse):
        mock_argparse.return_value = MagicMock(files=None)
        with pytest.raises(parser_cli.FolderNotFoundError):
            parser_cli.main()

    @patch('reportMonaco.parser_cli.argparse.ArgumentParser.parse_args')
    @patch('reportMonaco.parser_cli.check_files_in_folder')
    def test_with_folder_exist(self, mock_check_files_in_folder, mock_parse):
        mock_parse.return_value = MagicMock(files='TestFolder/', driver='Ihor')
        mock_check_files_in_folder.return_value = True
        result = parser_cli.main()
        assert result['driver'] == 'Ihor' and result['files'] == 'TestFolder/'
#
