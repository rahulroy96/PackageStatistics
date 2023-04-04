""" CLI tool to download that takes the architecture as
an argument, downloads the compressed Contents file associated with
it parse the file and output the statistics of the top 10 packages
that have the most files associated with them"""

import click
import os
from utils import download_file
from constants import DOWNLOAD_FOLDER, URL_BASE


@click.command()
@click.argument('architecture')
def package_statistics(architecture):

    if not os.path.exists(DOWNLOAD_FOLDER):
        os.mkdir(DOWNLOAD_FOLDER)

    filename = f'Contents-{architecture}.gz'
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    url = f'{URL_BASE}{filename}'

    click.echo(f"Downloading the contents file for {architecture}.")
    click.echo(f"Downloading {filename} using {url}")
    download_file(url, filepath)



if __name__ == '__main__':
    package_statistics()
