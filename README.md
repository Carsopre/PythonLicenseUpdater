[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3109/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# PythonLicenseUpdater
Simple tool that updates your python files license headers for the given directories. By default it will skip __init__.py.

## How to use it?

### Installation.

1. With pip:
```bash
pip install pylicup
```
2. With latest version from GitHub:
```bash
pip install git+https://github.com/Carsopre/PythonLicenseUpdater.git 
```
3. With custom version from GitHub:
```bash
pip install git+https://github.com/Deltares/PythonLicenseUpdater.git@v0.0.1
```

### Usage
The following command should be used.
```bash
python pylicup -l <path_to_your_license_file> -d <path_to_directory_with_python_files>
```
* <path_to_your_licenses_file> List of licenses, the first one will replace the ones that follow (in case present) or simply added at the top.
* <path_to_directory_with_python_files> List of arguments representing paths to the directories containing python files.

### Examples
Given the following directory hierarchy:
```
license_manager.py
|-src\
    |-__init__.py
    |-main.py
    |-utils.py
|-test\
    |-__init__.py
    |-test_main.py
    |-test_utils.py
|-setup.py
|-my_license.txt
|-my_newer_license.txt
```

1. The following command will update the license for src\main.py and src\utils.py:
```bash
python license_manager.py -l my_license.txt -d src
```

2. Whereas executing the following command will result in updating the license header for src\main.py, src\utils.py, test\test_main.py and test\test_utils.py:
```bash
python license_manager.py -l my_license.txt -d src test
```

3. Last, if we want to replace an existing license header with a new one, we would do the following command:
```bash
python license_manager.py -l {NEW_LICENSE} {OLD_LICENSE} -d src
```