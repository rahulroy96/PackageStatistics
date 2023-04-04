""" CLI tool to download that takes the architecture as
an argument, downloads the compressed Contents file associated with
it parse the file and output the statistics of the top 10 packages
that have the most files associated with them"""

import click
import os
from utils import download_file
from constants import DOWNLOAD_FOLDER, URL_BASE, CHUNK_SIZE, FILE_NAME_FORMAT
from contents_parser import ContentsParser


@click.command()
@click.option('--force', default=False, help='force download the content file even if it exists locally')
@click.argument('architecture')
def package_statistics(architecture, force):
    # Check if the download folder exists and c
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.mkdir(DOWNLOAD_FOLDER)

    gz_filename = FILE_NAME_FORMAT.format(architecture)  # Form the filename by adding the architecture with file prefix
    gz_filepath = os.path.join(DOWNLOAD_FOLDER, gz_filename)
    url = f'{URL_BASE}{gz_filename}'  # Form the url by adding the filename with the base url

    # Download the file again only is the file not present locally or if the force option is set
    if os.path.isfile(gz_filepath) and not force:
        click.echo(f"Using the local copy of the file - {gz_filename}")
    else:
        click.echo(f"Downloading {gz_filename} from {url}")
        download_file(url, gz_filepath, CHUNK_SIZE)  # Download the file

    content_parser = ContentsParser(gz_filepath, table_header=False)  # Initialize the ContentsParser class
    top_10 = content_parser.top_k_packages_max_files(10)  # Get the top 10 elements
    for i, data in enumerate(top_10):
        click.echo(f"{i+1}. {data[0]: <35}\t{data[1]}")


if __name__ == '__main__':
    package_statistics()
