# PythonLicenseUpdater
Simple tool that updates your python files license headers for the given directories. By default it will skip __init__.py.

## How to use it?
The following command should be used.
```bash
python license_manager.py -l <path_to_your_license_file> -d <path_to_directory_with_python_files>
```
* <path_to_your_licenses_file> Only the first license will be taken.
* <path_to_directory_with_python_files> List of arguments representing paths to the directories containing python files.

### Example
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
```

The following command:

```bash
python license_manager.py -l my_license.txt -d src
```

Will update the license for src\main.py and src\utils.py
Wheras executing the following command:

```bash
python license_manager.py -l my_license.txt -d src test
```

Will result in updating the license header for src\main.py, src\utils.py, test\test_main.py and test\test_utils.py