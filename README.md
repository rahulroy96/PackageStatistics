## Task
****
The task is to develop a python command line tool that takes the architecture as
an argument and downloads the compressed Contents file associated with
it from a Debian mirror. The program should parse the file and output the statistics
of the top 10 packages that have the most files associated with them.


## Initial thoughts
****************
Below are my initial thoughts on how to approach the problem, there may be changes
when starting to implement

- Downloader function to download the Contents file from debian mirror
    - takes url of the debian mirror
    - takes path to save the downloaded mirror
    - download can be done in chunks of size 1MB
    - downloading in chunks is not absolutely necessary since the content file size is
      only around 10 mb, but it is a good practice to download in chunks
    - Should handle invalid url, network errors
- Parser class for parsing the downloaded content file
    - takes the path where file was downloaded
    - Content file structure consists of zero or more lines of free form text followed by Table
        - the free form text can be ignored
        - the first row can be identified by checking for FILE and LOCATION
        - each table entry consists of filename followed by list of qualified package names
        - qualified package name has the form [[$AREA/]$SECTION/]$NAME where $AREA is deprecated
    - Creates a dictionary of package name as key and number of files as value
        - iterate over the rows of table
        - increment file count by 1 for each package in the list of each file.
    - Get the top k packages with most files.
        - use heap data structure to find the top k  packages with most files
        - create a list of tuples of the form (# of files, package)
        - heapify the list on # of files. This can be done in log(n) complexity
        - pop the top element k times. this can be done in k log(n) complexity
        - heap is best suited since we are interested in just the top 10 elements
          and not sorting the entire list which has n log(n) complexity.


## Implementation
**************
I have used the below folder structure for this task
package_statistics
|---src
    |---constants.py
    |---contents_parser.py
    |---package_statistics.py
    |---utils.py
|---test
    |---__init__.py
    |---test_contents_parser.py
    |---test_package_statistics.py
    |---test_utils.py

I spend around 7-8 hours spanning over a day to implement this completely. I took me around 30 min - 1 hr to ideate and
put down my initial thoughts. Once an initial outline was created, I started working on the task part by part. I started
with download_file, once the function and all its test cases where implemented I started working on the contents parser
and finally put it all together in the package_statistics. I used the click module which provided a simple and elegant
way to implement the command line utility. It took around 4-5 hours to implement initial working code and document.
Another 2 hours were spent in iterating over the initial and adding more options to give flexibility to the user. Some
time was also spent in trying to write a function for unzipping the gz file which I later found out was not necessary
since the gzip library provides methods to directly read from a gz file.

Initially, the program was implemented considering that the contents file will have the table header associated with it.
Since it was not the case, an optional parameter - table_header was added, which can be used to change this behaviour.
If table_header is set to false, the code starts to parse the contents file from the first line and if set to true, it
will look for the line containing FILE LOCATION before starting to parse the filenames and package names.

I thought of 2 approaches for what to do with the files that are downloaded. One approach was to delete the files once
the file is parsed. Second was to keep the file and reuse it if a second request for the same architecture is received.
Inorder to give flexibility to the user to choose between the approaches 2 optional parameters were added --no_cache
and --force. This allows the users to control the behaviour of the utility as they prefer. The --force option allow the
user to force download the contents file and not use the local copy and the --no_cache allow them to delete the files
after execution and not save locally.


## Usage
*****
python src/package_statistics package_name [options]

options description
--force=[true|false] - Force download the contents file even if it is available in local. The default value is false,
                       so the local copy will be used if available.
--no_cache=[true|false] - Delete the downloaded files after execution. The default value is True,
                          so the files will be deleted if not specified.
--table_header=[true|false] - If set to true, will check for table header "FILE  LOCATION" in the contents file. The
                              default is false, so if not specified the code doesn't look for the table header and
                              starts to parse from the first line
--debug=[true|false] - If set to true, the exception traceback will be output to the console. Default is false.


## Main components
***************
ContentsParser - The class takes as argument the path of a contents file. It has 2 methods, first is
get_files_list_per_package method will return a dictionary of packageName -> list of files associated with tha package.
Second method, top_k_packages_max_files, takes a parameter k and returns the top k packages with most files associated
with it. It uses a heap datastructure to find the top k packages. The function returns a list of tuples of the format
(package_name, # of files). This could also have been implemented as a generator but since the usage for the function is
to generate 10 values, it was decided to return the list.

package_statistics - the entry point function to the utility. It takes the architecture and a set of optional parameters
as input. The architecture is used to create the filename and the url from which the file is to be downloaded. It then
calls the download_file function from utility or uses the local version of the file depending on the --force optional
parameter. Once the file is downloaded it is passed to the contents parser to get the top 10 packages. The packages are
then output to the console.
