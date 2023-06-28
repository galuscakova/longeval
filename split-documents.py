#!/usr/bin/python

import sys
import os
import json

input_directory = sys.argv[1]
output_directory = sys.argv[2]

filenames = []

for filename in os.listdir(input_directory):
    if (".log" in filename):
        continue
    if (".hydra" in filename):
        continue
    filenames.append(filename)

total_fileid = 1

for filename in filenames:

    full_filename = os.path.join(input_directory, filename)
    print(full_filename)

    fileid = 1
    output = []

    f = open(full_filename)
    for line in f:
        document = json.loads(line)

        content = document['content']
        url = document['url']

        output_page = {"url": url, "content": content}
        output.append(json.dumps(output_page))
        fileid = fileid + 1

        if ((fileid % 1000) == 0):
            output_filename = output_directory + "/" + str(total_fileid)
            print(output_filename)
            outFile = open(output_filename, "w")
            outFile.write('\n'.join(output))
            outFile.close()
            output = []

            total_fileid = total_fileid + 1
            fileid = 1

    if (fileid != 1):
        print ("Warning: some files remaining" + str(fileid))

        output_filename = output_directory + "/" + str(total_fileid)
        print(output_filename)
        outFile = open(output_filename, "w")
        outFile.write('\n'.join(output))
        outFile.close()
        total_fileid = total_fileid + 1
