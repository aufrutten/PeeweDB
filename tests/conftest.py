import pytest


@pytest.fixture
def tmp_path_with_files(tmp_path):
    req_files = (
        ('abbreviations.txt', ['SVF_Sebastian Vettel_FERRARI', 'LHM_Lewis Hamilton_MERCEDES']),
        ('start.log', ['SVF2018-05-24_12:02:58.917', 'LHM2018-05-24_12:18:20.125']),
        ('end.log', ['SVF2018-05-24_12:04:03.332', 'LHM2018-05-24_12:11:32.585'])
    )
    temp_path_with_files = tmp_path / 'test_parser_cli'
    temp_path_with_files.mkdir()

    for file, texts in req_files:
        temp_file = temp_path_with_files / file
        temp_file.write_text('\n'.join(texts))
    return temp_path_with_files
