#!/usr/bin/python

import sys
import os
import json

mapping_filename = sys.argv[1]
input_directory = sys.argv[2]

filenames = []
ordered_urls = []
url_docid = {}
url_created = {}
url_updated = {}

f = open(mapping_filename)
for line in f:
    line = line.rstrip("\n")
    docid, url = line.split(None, 1)
    ordered_urls.append(url)
    url_docid[url] = docid

for filename in os.listdir(input_directory):
    if (".log" in filename):
        continue
    if (".hydra" in filename):
        continue
    filenames.append(filename)

for filename in filenames:

    full_filename = os.path.join(input_directory, filename)

    f = open(full_filename)
    for line in f:
        line = line.rstrip("\n")
        document = json.loads(line)

        url = document['url']
        created = document['created_at']
        updated = document['last_updated_at']
        url_created[url] = str(created)
        url_updated[url] = str(updated)

for url in ordered_urls:
    docid = url_docid[url]
    created = url_created[url]
    updated = url_updated[url]

    print(docid + "\t" + created + "\t" + updated)


