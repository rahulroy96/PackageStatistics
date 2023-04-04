import requests
import responses
import pytest
from src.utils import download_file, unzip_gz_file
import os
from unittest.mock import patch, mock_open

VALID_URL = 'http://valid_url'
INVALID_URL = 'http://invalid_url'
GZ_FILE_NAME = 'file.gz'
FILE_NAME = 'file'
FILE_CONTENT = b'Hello, world!'


@responses.activate
def test_download_file_success():
    # Mock the requests.get() function to return a response with status code 200 and content
    responses.add(responses.GET, VALID_URL, body=FILE_CONTENT, status=200)

    # Call the download_file() function with a URL and file name
    result = download_file(VALID_URL, GZ_FILE_NAME)

    # Assert that the file was downloaded successfully and the content matches the mocked response
    assert result, True
    with open(GZ_FILE_NAME, 'rb') as f:
        content = f.read()
    assert content, FILE_CONTENT
    assert os.path.isfile(GZ_FILE_NAME)
    os.remove(GZ_FILE_NAME)


@responses.activate
def test_download_file_error():
    # Mock the requests.get() function to raise an exception
    responses.add(responses.GET, INVALID_URL,
                  body=requests.RequestException('Download error'), status=404)

    # Assert that the file was not downloaded successfully and the function returned False
    with pytest.raises(requests.RequestException):
        # Call the download_file() function with a URL and file name
        _ = download_file(INVALID_URL, GZ_FILE_NAME)
        assert os.path.isfile(GZ_FILE_NAME), False


@patch('gzip.open', mock_open(read_data=FILE_CONTENT))
@patch('os.path.isfile')
def test_unzip_gz_file_success(mock_isfile):
    mock_isfile.return_value = True

    # Call the unzip_gz_file with GZ_FILE_NAME and FILE_NAME
    result = unzip_gz_file(GZ_FILE_NAME, FILE_NAME)

    # Assert that the file was unzipped successfully and the function returned True
    assert result, True
    with open(FILE_NAME, 'rb') as f:
        content = f.read()
    assert content, FILE_CONTENT
    assert os.path.isfile(FILE_NAME)
    os.remove(FILE_NAME)


@patch('gzip.open', mock_open(read_data=FILE_CONTENT))
@patch('os.path.isfile')
def test_unzip_gz_file_not_gz_input_exception(mock_isfile):
    mock_isfile.return_value = True

    # Assert that ValueError was raised and the function returned False
    with pytest.raises(ValueError):
        # Call the unzip_gz_file with GZ_FILE_NAME and FILE_NAME
        _ = unzip_gz_file(FILE_NAME, FILE_NAME)
        assert os.path.isfile(FILE_NAME), False


@patch('gzip.open', mock_open(read_data=FILE_CONTENT))
@patch('os.path.isfile')
def test_unzip_gz_file_input_file_not_exists_exception(mock_isfile):
    mock_isfile.return_value = False

    # Assert FileNotFoundError was raised and the function returned False
    with pytest.raises(FileNotFoundError):
        # Call the unzip_gz_file with GZ_FILE_NAME and FILE_NAME
        _ = unzip_gz_file(GZ_FILE_NAME, FILE_NAME)
        assert os.path.isfile(FILE_NAME), False
