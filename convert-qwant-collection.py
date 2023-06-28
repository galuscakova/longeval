#!/usr/bin/python

import sys
import os
import json
import re
import spacy

nlp = spacy.load('fr_core_news_sm')

prefix = "0722"
prefix = sys.argv[1]
directory = sys.argv[2]
output_directory = sys.argv[3]
output_format = sys.argv[4]
adult_spam_urls_filename = sys.argv[5]
filenames = []

def comp(o):
    o = o.replace("collector_kodicare_", "")
    o = o.replace(".txt", "")
    return int(o)

for filename in os.listdir(directory):
    if (".log" in filename):
        continue
    if (".hydra" in filename):
        continue
    filenames.append(filename)

filenames.sort(key=comp)

fileid = 1
output = []
processed_urls = []
mapped_output = ""
time_output = ""
trec_output = ""
no_adult_urls = []
spam_removed_urls = []

if "clean" in output_format:
    adult_spam_urls_file = open(adult_spam_urls_filename)
    adult_spam_urls_data = json.load(adult_spam_urls_file)
    adult_spam_urls_file.close()

    no_adult_urls = adult_spam_urls_data["urls"]
    spam_removed_urls = adult_spam_urls_data["spam_removed_urls"]

for filename in filenames:

    full_filename = os.path.join(directory, filename)
    print(full_filename)

    fileid = 1
    documentid = comp(filename)

    f = open(full_filename)
    for line in f:
        document = json.loads(line)
        url = document['url']

        downloaded_time = document['created_at']
        updated_time = document['last_updated_at']

        #print(url)

        # Remove duplicates
        if url in processed_urls:
            #print("duplicate")
            continue

        # Remove adult content
        # Implementation for 06: 
        if url in spam_removed_urls:
            #print("spam")
            continue
        
        if not (url in no_adult_urls):
            #print("adult")
            continue
        # For 07, 09 too much content is removed

        #print("processing")

        documentid_formatted = "{:03d}".format(int(documentid))
        fileid_formatted = "{:05d}".format(int(fileid))
        newid = "doc" + prefix + documentid_formatted + fileid_formatted

        content = document['content']

        if ("json" in output_format):            
            output_page = {"id": newid, "contents": content}
            output.append(output_page)
        
        if ("map" in output_format):
            mapped_line = newid + "\t" + url + "\n"
            mapped_output = mapped_output + mapped_line

        if ("time" in output_format):

            downloaded_time_formatted = datetime.datetime.utcfromtimestamp(downloaded_time).strftime('%Y-%m-%dT%H:%M:%SZ')
            updated_time_formatted = datetime.datetime.utcfromtimestamp(updated_time).strftime('%Y-%m-%dT%H:%M:%SZ')

            time_line = newid + "\t" + downloaded_time_formatted + "\t" + updated_time_formatted + "\n"
            time_output = time_output + time_line

        if ("trec" in output_format):
            trec_outputl = ""

            trec_outputl = trec_outputl + "<DOC>\n"
            trec_outputl = trec_outputl + "<DOCNO>" + newid + "</DOCNO>\n"
            trec_outputl = trec_outputl + "<DOCID>" + newid + "</DOCID>\n"
            trec_outputl = trec_outputl + "<TEXT>\n"

            if ("segmented" in output_format):
                doc_content = nlp(content)

                new_content = ""
                for sent in doc_content.sents:
                    new_content = new_content + sent.text + "\n"

                content = new_content

            if ("normalized" in output_format):
                normalized_content = re.sub(r'[^ \w+]','', content)
                normalized_content = ' '.join(normalized_content.split())
                trec_outputl = trec_outputl + normalized_content + "\n"
            else:
                trec_outputl = trec_outputl + content + "\n"
            trec_outputl = trec_outputl + "</TEXT>\n"
            trec_outputl = trec_outputl + "</DOC>\n"

            trec_output = trec_output + trec_outputl
        
        processed_urls.append(url)

        fileid = fileid + 1

    final_output = ""
    if ("json" in output_format):
        final_output = json.dumps(output)

    if ("map" in output_format):
        final_output = mapped_output

    if ("time" in output_format):
        final_output = time_output

    if ("trec" in output_format):
        final_output = trec_output

    output_filename = output_directory + "/" + filename
    outFile = open(output_filename, "w")
    outFile.write(final_output)
    outFile.close()

    output = []
    mapped_output = ""
    trec_output = ""
    time_output = ""

