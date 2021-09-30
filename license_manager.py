'''
Original Author: Carles S. Soriano Pérez (carles.sorianoperez@deltares.nl).
Department: Software Product Development.
Unit: Deltares Software Centre.
'''
import argparse
from typing import List, Tuple
from pathlib import Path
from fnmatch import fnmatch

# By default we only add the licenses to the /src *.py files.
__excluded_files = [
    '__init__.py'
    ]
__pattern = '*.py'


def license_header_manager(header_licenses: List[str], directory_files: List[str]):
    """ Insert the license header provided in the argument to all the files
    in the directory (also provided in the arguments).

    Arguments:
        argv {[str]} -- default input from command line
    """
    __licenses, __directory_files = __get_input(header_licenses, directory_files)
    __unlicensed_files = __get_unlicensed_files(__licenses[0], __directory_files)
    __replace_license_header(__licenses, __unlicensed_files)


def remove_license_header(header_licenses: List[str], directory_files: List[str]):
    """Removes the license header file content from all the files in
    the given directory. Everything is provided in the argv.

    Arguments:
        argv {[str]} -- Arguments for the calling function.
    """
    __licenses, __directory_files = \
        __get_input(header_licenses, directory_files)
    __files = __get_all_files(__directory_files)
    __remove_license_header(__licenses, __files)


def __get_input(header_licenses: List[str], directory_files: List[str]) \
        -> Tuple[List[str], List[str]]:
    """Validates all the arguments provided when needed for inserting /
    deleting a single header from all the files.

    Arguments:
        argv {[str]} -- Arguments for the calling function.

    Returns:
        Tuple[List[str], List[str]]
            -- License header content list and file paths in directory.
    """
    # First try to parse the arguments
    __header_licenses = __get_license_headers(header_licenses)
    hl_str = "\n".join(__header_licenses)
    print(f"Licenses found: {hl_str}")
    __directory_files = __get_directory_files(directory_files)
    return __header_licenses, __directory_files


def __get_license_headers(header_list: List[str]) -> List[str]:
    """Gets the license header text.

    Arguments:
        header_list {List[str]} -- List of file paths to the license header.

    Returns:
        List[str] -- Content of the license header.
    """
    licenses = []
    for header_file in header_list:
        hf_path = Path(header_file)
        if not hf_path.exists():
            raise FileNotFoundError(hf_path)
        with hf_path.open() as f:
            licenses.append(f.read())
    return licenses


def __get_directory_files(directory_list: List[Path]) -> List[Path]:
    """Gets a list of files matching the patterns

    Arguments:
        directory_list {List[Path]}
            -- List of directories with files to license..

    Returns:
        List[Path] -- List of file paths.
    """
    file_list = []

    for directory in directory_list:
        d_path = Path(directory).resolve()
        for found_path in d_path.rglob("*"):
            if found_path.name not in __excluded_files and fnmatch(found_path.name, __pattern):
                file_list.append(found_path)
    print(f"Found {len(file_list)} files meeting the requirements.")
    return file_list


def __get_all_files(files_list: List[Path]) -> List[Tuple[Path, str]]:
    """Returns a list of all the files and their content.

    Arguments:
        files_list {List[str]}
            -- Directory where to find the files that require licenses.

    Returns:
        List[Tuple[str, str]] -- List of Tuple of [File Path, file content].

    Yields:
        Tuple[str, str] -- File path and its content.
    """
    for file in files_list:
        yield file, file.read_text()


def __get_unlicensed_files(header_file: str, files_list: List[Path]) \
        -> List[Tuple[Path, str]]:
    """Gets all the files that do not contain the required license header.

    Arguments:
        header_file {str} -- Required license header text.
        files_list {List[str]} -- List of files to check.

    Returns:
        List[str, str] -- List of tuple [file path, file content]

    Yields:
        List[str, str] -- List of tuple [file path, file content]
    """
    for file in files_list:
        f_text = file.read_text()
        if header_file not in f_text:
            yield file, f_text


def __replace_license_header(
        license_headers: List[str],
        files: List[Tuple[Path, str]]):
    """Replaces an old license header in all the files provided
    with the new license header.

    Arguments:
        license_headers{List[str]} -- Licenses to manage.
        files {List[Tuple[Path, str]]} -- Files where to add the new header.
    """
    for file_path, file_content in files:
        if len(license_headers) > 1:
            for old_license in license_headers[1:]:
                file_content.replace(old_license, '')
        licensed_text = license_headers[0] + "\n" + file_content
        file_path.write_text(licensed_text)
        print(f"Replaced header for {file_path}")


def __remove_license_header(
        license_headers: List[str],
        files: List[Tuple[Path, str]]):
    """Removes all requested license headers from the files.

    Arguments:
        license_headers{List[str]} -- Licenses to remove.
        files {List[Tuple[str, str]]} -- Files where to add the new header.
    """
    for file_path, file_content in files:
        if len(license_headers) > 0:
            for old_license in license_headers:
                file_content.replace(old_license, "")
        file_path.write_text(file_content)


if __name__ == '__main__':
    """For now we only accpet inserting as a direct call from the main """
    # Define the argparser helper:
    parser = argparse.ArgumentParser(
        description='Manages files license header. \n'
        + 'Sets the last license header given in all files of the file directory.'
        + 'If multiple license headers are given, the first one will be added to all files and replace the rest provided.'
        + 'It is possible to include multiple directories where to insert / replace header files.')
    parser.add_argument(
        '-l, --licenses',
        dest='licenses',
        type=str,
        nargs='+',
        required=True,
        help='License headers file path. The first occurrence is considered as the new one to replace the rest.')
    parser.add_argument(
        '-d, --directories',
        dest='directories',
        nargs='+',
        required=True,
        help='Directories where to insert / replace licenses.'
    )
    args = parser.parse_args()
    print("Initializing license manager.")
    license_header_manager(args.licenses, args.directories)
    print("License manager finished.")
