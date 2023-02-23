#!/usr/bin/python

import sys
import os
import json
import re

directory = sys.argv[1]
output_directory = sys.argv[2]
output_format = sys.argv[3]
filenames = []

def comp(o):
    o = o.replace("part-", "")
    o = o.replace("-d3e8a3c9-bb7d-454c-92d4-bf45cbabd6c4-c000.json", "")
    return int(o)

for filename in os.listdir(directory):
    if ("_SUCCESS" in filename):
        continue
    filenames.append(filename)

filenames.sort(key=comp)

queryid = 1
tsv_output = ""

for filename in filenames:

    full_filename = os.path.join(directory, filename)
    print(full_filename)

    f = open(full_filename)
    for line in f:
        full_query = json.loads(line)
        query = full_query['query']

        if (output_format == "tsv"):            
            query_line = str(queryid) + "\t" + query + "\n"
            tsv_output = tsv_output + query_line

        queryid = queryid + 1

    final_output = ""

    if (output_format == "tsv"):
        final_output = tsv_output

    output_filename = output_directory + "/" + filename
    outFile = open(output_filename, "w")
    outFile.write(final_output)
    outFile.close()

    tsv_output = ""

