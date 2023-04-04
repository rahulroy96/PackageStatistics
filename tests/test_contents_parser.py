from src.contents_parser import ContentsParser, InvalidContentFileFormat
from unittest import mock
from unittest.mock import patch, mock_open
from collections import defaultdict
import pytest

GZ_CONTENT_WITHOUT_HEADER = b"file1  package1\n" \
                            b"file2  package1\n" \
                            b"file1  package2\n" \
                            b"file2  package2\n" \
                            b"file3  package2"

GZ_CONTENT_WITH_HEADER = b"FILE  LOCATION\n" \
                         b"file1  package1\n" \
                         b"file2  package1\n" \
                         b"file1  package2\n" \
                         b"file2  package2\n" \
                         b"file3  package2"


def mock_parse_file(*_):
    """Mock the parse_file function from the ContentsParser class"""
    files_list_per_package = defaultdict(list)
    files_list_per_package['package1'].append('file1')
    files_list_per_package['package1'].append('file2')
    files_list_per_package['package2'].append('file1')
    files_list_per_package['package2'].append('file2')
    files_list_per_package['package2'].append('file3')
    files_list_per_package['package3'].append('file1')
    files_list_per_package['package4'].append('file1')
    files_list_per_package['package4'].append('file1')
    return files_list_per_package


def test_top_k_packages_max_files_successful():
    # mock the parse file function and check if the top k function is working
    with mock.patch.object(ContentsParser, 'get_files_list_per_package', new=mock_parse_file):
        content_parser = ContentsParser("file_path")
        top_k = content_parser.top_k_packages_max_files(2)
        assert len(top_k), 2
        assert top_k[0] == ('package2', 3)


def test_top_k_packages_max_files_k_greater_than_files_successful():
    # mock the parse file function and check if the top k function is working
    # with k greater than the # of packages
    with mock.patch.object(ContentsParser, 'get_files_list_per_package', new=mock_parse_file):
        content_parser = ContentsParser("file_path")
        top_k = content_parser.top_k_packages_max_files(5)
        assert len(top_k) == 4
        assert top_k[0] == ('package2', 3)


@patch('gzip.GzipFile', mock_open(read_data=GZ_CONTENT_WITHOUT_HEADER))
def test_parse_file_without_header_successful():
    # Test if the ContentsParser.parse_file is working for files without Header row.
    # Header row is the line containing value "FILE LOCATION".
    # Call the parse_file function to get the returned files_list_per_package
    content_parser = ContentsParser("file_path", table_header=False)
    files_list_per_package_returned = content_parser.get_files_list_per_package()

    # assert that the returned dict is as expected
    assert files_list_per_package_returned["package1"] == ['file1', 'file2']
    assert files_list_per_package_returned['package2'] == ['file1', 'file2', 'file3']


@patch('gzip.GzipFile', mock_open(read_data=GZ_CONTENT_WITH_HEADER))
def test_parse_file_with_header_successful():
    # Test if the ContentsParser.parse_file is working for files with Header row.
    # Header row is the line containing value "FILE LOCATION".
    # Call the parse_file function to get the returned files_list_per_package
    content_parser = ContentsParser("file_path", table_header=True)
    files_list_per_package_returned = content_parser.get_files_list_per_package()

    # assert that the returned dict is same as the original
    assert files_list_per_package_returned["package1"] == ['file1', 'file2']
    assert files_list_per_package_returned['package2'] == ['file1', 'file2', 'file3']


@patch('gzip.GzipFile', mock_open(read_data=GZ_CONTENT_WITHOUT_HEADER))
def test_parse_file_with_header_invalid_format():

    with pytest.raises(InvalidContentFileFormat):
        # Call the parse_file function to get the returned files_list_per_package
        content_parser = ContentsParser("file_path", table_header=True)
        _ = content_parser.get_files_list_per_package()
