import responses
import pytest
from src.utils import download_file
import os

VALID_URL = 'http://valid_url'
INVALID_URL = 'http://invalid_url'
FILE_NAME = 'file'


@responses.activate
def test_download_file_success():
    # Mock the requests.get() function to return a response with status code 200 and content
    responses.add(responses.GET, VALID_URL, body=b'Hello, world!', status=200)

    # Call the download_file() function with a URL and file name
    result = download_file(VALID_URL, FILE_NAME)

    # Assert that the file was downloaded successfully and the content matches the mocked response
    assert result, True
    with open(FILE_NAME, 'rb') as f:
        content = f.read()
    assert content, b'Hello, world!'
    assert os.path.isfile(FILE_NAME)


@responses.activate
def test_download_file_error():
    # Mock the requests.get() function to raise an exception
    responses.add(responses.GET, INVALID_URL,
                  body=Exception('Download error'), status=404)

    # Assert that the file was not downloaded successfully and the function returned False
    with pytest.raises(Exception):
        # Call the download_file() function with a URL and file name
        _ = download_file(INVALID_URL, FILE_NAME)
        assert os.path.isfile(FILE_NAME), False
