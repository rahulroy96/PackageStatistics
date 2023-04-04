"""A collection of utility files used by the command line tool"""

import os
import requests
import shutil
import gzip


def download_file(file_url: str, file_name: str, chunk_size=1024 * 1024):
    """
    Downloads the file from the given url and saves it to the path.

    :param file_url: The url of the file to be downloaded.
    :param file_name: The filename to save the downloaded file.
    :param chunk_size: The chunk_size in bytes that should be used while downloading.
    :return: True if file was successfully downloaded false otherwise
    """
    try:

        with requests.get(file_url, stream=True) as r:  # Send a GET request to the URL with streaming enabled
            r.raise_for_status()  # Raise an exception if the response has an error status code
            with open(file_name, "wb") as f:  # Open the file in binary mode for writing
                for chunk in r.iter_content(chunk_size=chunk_size):  # Iterate over the response content in chunks
                    f.write(chunk)  # Write each chunk to the file

    except requests.exceptions.HTTPError as e:  # Raised when there is 4xx or 5xx return status code
        print(f"Exception while downloading the file, please check your url  - {file_url}")
        print(f"Exception - {e}")
        raise
    except requests.exceptions.ConnectionError as e:  # Raised when there is a network problem
        print(e)
        raise
    else:
        print(f"Downloaded {file_name} successfully.")

    return os.path.isfile(file_name)  # Returns true if the file was downloaded successfully


def unzip_gz_file(gz_file_path, output_file):
    """
    Unzips the gzip file to the specified directory
    :param gz_file_path: The path to the file which is to be unzipped
    :param output_file: The path where the file is to be saved
    :return: True if the file was unzipped successfully
    """
    # Check that the input file is a .gz file
    if not gz_file_path.endswith('.gz'):
        raise ValueError('file is not a .gz file')

    # Check that the input file exists
    if not os.path.isfile(gz_file_path):
        raise FileNotFoundError(f'File not found: {gz_file_path}')

    try:
        # Open the .gz file for reading and the output file for writing
        with gzip.open(gz_file_path, 'rb') as gz_file, open(output_file, 'wb') as out_file:
            # Read the contents of the .gz file and write them to the output file
            shutil.copyfileobj(gz_file, out_file)  # Shuttle allows copy without loading the entire file
    except Exception as e:
        raise Exception(f'Error unzipping file {gz_file_path}: {str(e)}')

    return os.path.isfile(output_file)
