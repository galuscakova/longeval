#!/usr/bin/python

import sys
import os
import json
import re

filename = sys.argv[1]
output_format = sys.argv[2]

output = ""

if ".json" in filename:

    f = open(filename)
    data = json.load(f)

    for iterator in data:
        #print(iterator, ":", data[iterator])
    
        if (output_format == "tsv"):            
            query_line = str(iterator) + "\t" + data[iterator] + "\n"
            output = output + query_line

        if (output_format == "trec"):
            query_line = "<top>\n<num>" + str(iterator) + "</num>\n<title>" + data[iterator] + "</title>\n</top>\n\n"
            output = output + query_line

    print(output)

if ".tsv" in filename:
    with open(filename) as file:
        for line in file:

            line = line.rstrip("\n")
            lid, ltext = line.split("\t")

            if (output_format == "trec"):
                query_line = "<top>\n<num>" + str(lid) + "</num>\n<title>" + ltext + "</title>\n</top>\n\n"
                output = output + query_line

    print (output)
