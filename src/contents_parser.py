"""Class to parse the contents of the debian content file.
File format can be found t https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices
"""
import gzip
from collections import defaultdict
from heapq import heapify, heappop
from exceptions import InvalidContentFileFormat


class ContentsParser:

    def __init__(self, filepath, table_header=True):
        self.filepath = filepath  # The path to the file that is to be parsed
        self.files_list_per_package = defaultdict(list)
        self.table_header = table_header

    def parse_file(self):
        """
        Parse the contents file and create a dictionary of package -> list of files
        :return: None
        """
        self.files_list_per_package = defaultdict(list)

        table_started = False
        with gzip.GzipFile(self.filepath) as lines:
            for i, line in enumerate(lines):
                line = line.decode('utf-8')

                left, _, right = line.strip().rpartition(' ')
                left = left.strip()
                right = right.strip()

                if self.table_header and not table_started:  # Loop over the lines till FILE and LOCATION is found if table_header is true
                    if left == 'FILE' and right == 'LOCATION':
                        table_started = True
                    continue

                file = left
                # Once the table starts the right value contains list of qualified package names, separated by comma.
                qualified_package_names = right.split(',')

                for qualified_package_name in qualified_package_names:
                    # A qualified package name has the form [[$AREA/]$SECTION/]$NAME, where $AREA is the archive area,
                    # $SECTION the package section, and $NAME the name of the package.
                    _, _, package_name = qualified_package_name.rpartition('/')
                    self.files_list_per_package[package_name].append(file)  # Append file to file list of the package

        if self.table_header and not table_started:
            # The table header containing FILE LOCATION was not detected in the file even though table header exists
            raise InvalidContentFileFormat("Invalid contents File! Table header - FILE LOCATION not found")

    def top_k_packages_max_files(self, k: int) -> list:
        """
        Parse the contents file and return the top k packages with most files associated with it.
        :param k: The value k gives the number of top packages that needs to be returned
        :return: A list (package_name, number of files) containing the k top packages
        """
        # parse the file to create the files_list_per_package dictionary
        self.parse_file()

        # Convert the dictionary to list of tuples of the form (# of files, package name)
        # negate the number of files since we are going to use max heap
        files_per_package_count_list = [(-len(files), package_name)
                                        for package_name, files in self.files_list_per_package.items()]

        heapify(files_per_package_count_list)  # Heapify the list of tuples

        top_k = []
        # top k packages can be found by poping from the heap k times
        for _ in range(k):
            if files_per_package_count_list:
                top = heappop(files_per_package_count_list)
                top_k.append((top[1], -top[0]))

        return top_k
