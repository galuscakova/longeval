#!/usr/bin/python

import sys
import os

input_dirname = sys.argv[1]
output_dirname = sys.argv[2]

for filename in os.listdir(input_dirname):
    old_filename = os.path.join(input_dirname, filename)
    new_filename = os.path.join(output_dirname, filename)

    print(old_filename)

    new_file = ""
    with open(old_filename) as input_file:
        for line in input_file:
            if (not "bytearray(" in line):
                new_file = new_file + line

    with open(new_filename, 'w') as output_file:
        output_file.write(new_file)
