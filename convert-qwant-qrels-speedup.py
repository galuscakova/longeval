#!/usr/bin/python

import sys
import os
import json
import re

filename_qrel = sys.argv[1]
filename_mapping = sys.argv[2]
filename_urls = sys.argv[3]
filename_spam_adult = sys.argv[4]

output = ""
prefix = "q0922"

f_urls = open(filename_urls)
data_urls = json.load(f_urls)

kodicareids_to_url = {}
url_to_newids = {}

no_adult_urls_dict = {}
spam_removed_urls_dict = {}

if (filename_spam_adult != "undefined"):
    adult_spam_urls_file = open(filename_spam_adult)
    adult_spam_urls_data = json.load(adult_spam_urls_file)

    no_adult_urls = adult_spam_urls_data["urls"]
    no_adult_urls_dict = dict.fromkeys(no_adult_urls, "")

    spam_removed_urls = adult_spam_urls_data["spam_removed_urls"]
    spam_removed_urls_dict = dict.fromkeys(spam_removed_urls, "")

    adult_spam_urls_file.close()


for iterator in data_urls:
    kodicareids_to_url[iterator] = data_urls[iterator]

with open(filename_mapping) as data_maps:
    for line in data_maps:
        line = line.rstrip()
        newid, url = re. split(r'\t+', line)
        url_to_newids[url] = newid

with open(filename_qrel) as data_qrel:
    for line in data_qrel:
        line = line.rstrip()
        queryid, zero, docid, relevance = line.split()
        new_queryid = prefix + queryid
        url = kodicareids_to_url[docid]

        if (filename_spam_adult != "undefined"):
            if url in spam_removed_urls_dict:
                continue
            if (not url in no_adult_urls_dict):
                continue

        newdocid = "-1"
        if url in url_to_newids:
            newdocid = url_to_newids[url]
            print (new_queryid + " 0 " + newdocid + " " + relevance)
        #else:
            #print("Docid unknown: " + url)

        #print (new_queryid + " 0 " + newdocid + " " + relevance)
