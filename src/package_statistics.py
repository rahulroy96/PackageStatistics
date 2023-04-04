""" CLI tool to download that takes the architecture as
an argument, downloads the compressed Contents file associated with
it parse the file and output the statistics of the top 10 packages
that have the most files associated with them"""
import sys
import shutil
import click
import os
from utils import download_file
from constants import DOWNLOAD_FOLDER, URL_BASE, CHUNK_SIZE, FILE_NAME_FORMAT, K_VALUE
from contents_parser import ContentsParser, InvalidContentFileFormat
from requests.exceptions import HTTPError, ConnectionError


@click.command()
@click.option('--no_cache', default=True, help='If set to true, the downloaded files are not deleted.')
@click.option('--debug', default=False, help='Print the exception to the console for more info.')
@click.option('--force', default=False, help='Force download the content file even if it exists locally')
@click.option('--table_header', default=False,
              help='Specifies if the table structure of the contents file has a header')
@click.argument('architecture')
def package_statistics(architecture, table_header, force, debug, no_cache):
    try:
        # Check if the download folder exists and c
        if not os.path.exists(DOWNLOAD_FOLDER):
            os.mkdir(DOWNLOAD_FOLDER)

        gz_filename = FILE_NAME_FORMAT.format(architecture)  # Format the filename prefix using the architecture
        gz_filepath = os.path.join(DOWNLOAD_FOLDER, gz_filename)
        url = f'{URL_BASE}{gz_filename}'  # Form the url by adding the filename with the base url

        # Download the file again only is the file not present locally or if the force option is set
        if os.path.isfile(gz_filepath) and not force:
            click.echo(f"Using the local copy of the file - {gz_filename}")
        else:
            click.echo(f"Downloading {gz_filename} from {url}")
            download_file(url, gz_filepath, CHUNK_SIZE)  # Download the file

        content_parser = ContentsParser(gz_filepath, table_header=table_header)  # Initialize the ContentsParser class
        top_10 = content_parser.top_k_packages_max_files(K_VALUE)  # Get the top 10 elements
        for i, data in enumerate(top_10):
            click.echo(f"{i+1}. {data[0]: <35}\t{data[1]}")
    except HTTPError as e:
        click.echo("\nError: Couldn't download the contents file!! Please check the architecture name")
        if debug:
            click.echo(e)
        sys.exit(1)
    except ConnectionError as e:
        click.echo("\nError: Couldn't connect to the server!! Please check your network connection")
        if debug:
            click.echo(e)
        sys.exit(1)
    except InvalidContentFileFormat as e:
        click.echo("\nError: Invalid contents File format! Table header(FILE LOCATION) not found. "
                   "Try using --table_header=false if the contents file is not expected to have a table header.")
        if debug:
            click.echo(e)
        sys.exit(1)

    finally:
        if no_cache:
            shutil.rmtree(DOWNLOAD_FOLDER)


if __name__ == '__main__':
    package_statistics()
