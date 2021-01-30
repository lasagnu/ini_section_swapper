## Table of contents
* [General info](#general-info)
* [Usage](#usage)
* [Examples](#usage)

## General info
a simple tool for overwriting the entire sections from base .ini in target .ini file 

## Usage
```
-f: path to file you would like to change
-o: path to output file, if not provided new file with _out suffix will be created
-c: sections to change (i.e. section_name_base:section_name_target)
--overwrite: (bool) once passed it will overwrite the section name in target file with the name from base file
```

## Examples
Change the 'to_change' section contents (keys and values) in test.ini file with 'example' section from base_map/default.ini file and save as test_out.ini:

```
ini_section_swapper.py -f 'path/to/test.ini' -c example:to_change
```

Change multiple section contents in test.ini file with sections from base_map/default.ini file and save as test_out.ini:

```
ini_section_swapper.py -f 'path/to/test.ini' -c example:to_change another_example:to_another_change
```
```
ini_section_swapper.py -f 'path/to/test.ini' -c example:to_change -c another_example:to_another_change
```

Change multiple section contents and section name in test.ini file with section contents and names from base_map/default.ini file and save as test_out.ini:

```
ini_section_swapper.py -f 'path/to/test.ini' -c example:to_change another_example:to_another_change --overwrite
```

Save to custom output file:

```
ini_section_swapper.py -f 'path/to/test.ini' -c example:to_change -o 'path/to/output.ini'
```
