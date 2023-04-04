"""A collection of utility files used by the command line tool"""

import os
import requests


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
