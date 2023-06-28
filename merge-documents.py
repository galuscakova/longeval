#!/usr/bin/python

import sys
import os
import json
import random

input_directory = sys.argv[1]
output_directory = sys.argv[2]

filenames = []
max_files = 21

for filename in os.listdir(input_directory):
    if (".log" in filename):
        continue
    if (".hydra" in filename):
        continue
    filenames.append(filename)

random.seed(10)
random.shuffle(filenames)


new_fileid = 1
processed_files = 0
output = []

for filename in filenames:

    full_filename = os.path.join(input_directory, filename)
    print(full_filename)

    f = open(full_filename)
    for line in f:
        document = json.loads(line)

        content = document['content']
        url = document['url']

        output_page = {"url": url, "content": content}
        output.append(json.dumps(output_page))
        
    processed_files = processed_files + 1 

    if (processed_files == max_files):
            
            output_filename = output_directory + "/collector_kodicare_" + str(new_fileid) + ".txt"
            print(output_filename)
            outFile = open(output_filename, "w")
            outFile.write('\n'.join(output))
            outFile.close()
            output = []

            new_fileid = new_fileid + 1
            processed_files = 0

output_filename = output_directory + "/collector_kodicare_" + str(new_fileid) + ".txt"
print(output_filename)
outFile = open(output_filename, "w")
outFile.write('\n'.join(output))
outFile.close()
