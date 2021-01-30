import argparse
import ini
import os
import sys
import re
from pathlib import Path

# binds arg parser
arg_parser = argparse.ArgumentParser()
# sets file_path variable as required and ensures its Path type
arg_parser.add_argument('-f', dest='file_path', action='store', nargs=1, type=Path, help='path to file you would like to change')
arg_parser.add_argument('-o', dest='output_file_path', action='store', nargs=1, type=Path, help='path to output file, if not provided new file with _out suffix will be created', required=False)
arg_parser.add_argument('-c', dest='seg_to_change', action='append', type=str, nargs='*', required=True,
                        help='sections to change (i.e. section_name_base->section_name_target')
arg_parser.add_argument('--overwrite', dest='overvrite_target_segments', action='store_true', help='once passed it will overwrite the section name in target file with the name from base file, default = off', required=False)
# parses the arguments
p = arg_parser.parse_args()

# loads base mapping .ini file to memory
# it contains all sections/definitions you can change to
cwd = os.getcwd()
base_ini_fp = Path(cwd) / 'base_map' / 'default.ini'
base_ini = ini.parse(open(base_ini_fp).read())
base_ini_sections = []
for section in base_ini.keys():
    base_ini_sections.append(section)

# checks if file exists at the path provided in the argument and loads it into memory, otherwise graciously spierdalaj
target_ini = None
target_ini_sections = []
if p.file_path[0].exists():
    target_ini = ini.parse(open(p.file_path[0]).read())
    for section in target_ini.keys():
        target_ini_sections.append(section)
else:
    print(f'File {p.file_path[0]} does not exist. Are you out of your mind?!')
    sys.exit()

# iterate through input combination of seg_to_change and get valid combinations
valid_segments_to_change = dict()
valid_segment_name = re.compile(r"^[a-zA-Z0-9\._-]+:[a-zA-Z0-9\._-]+$")
for list_of_segment_combinations in p.seg_to_change:
    for combination in list_of_segment_combinations:
        if valid_segment_name.match(combination):
            base_name = combination.split(":")[0]
            target_name = combination.split(":")[1]
            valid_segments_to_change[base_name] = target_name
        else:
            print(f'[SEGMENTS COMBINATION NOT VALID]: {combination} - please use combination of [a-zA-Z0-9\._-] and separate them with ":", ie: segment:other_segment')

# iterate through regexp-valid segs to change and apply the changes if both exist
for combination in valid_segments_to_change.keys():
    base_section = combination
    target_section = valid_segments_to_change[combination]
    if base_section in base_ini_sections and target_section in target_ini_sections:
        del target_ini[target_section]
        if p.overvrite_target_segments:
            target_ini[base_section] = base_ini[base_section]
        else:
            target_ini[target_section] = base_ini[base_section]
        output = str(p.file_path[0]).rsplit('.', 1)
        output_fp = Path(output[0] + '_out.' + output[1])

        if p.output_file_path:
            try:
                with open(p.output_file_path[0], 'w+') as f:
                    f.write(ini.stringify(target_ini))
                print(f'file saved as: {p.output_file_path[0]}')
            except Exception as ex:
                print(ex)
        else:
            try:
                with open(output_fp, 'w+') as f:
                    f.write(ini.stringify(target_ini))
                print(f'file saved as: {output_fp}')
            except Exception as ex:
                print(ex)

    elif not base_section in base_ini_sections and target_section in target_ini_sections:
        print(f'base section missing: {base_section} ({base_section}->{target_section})')
    elif not target_section in target_ini_sections and base_section in base_ini_sections:
        print(f'target section missing: {target_section} ({base_section}->{target_section})')
    else:
        print(f'base and target section missing: {base_section}, {target_section} ({base_section}->{target_section})')
