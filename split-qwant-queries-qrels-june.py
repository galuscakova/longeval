#!/usr/bin/python

# python ~/scripts/longeval/split-qwant-queries-qrels.py ~/../gonzagab/Kodicare/qwant-data/2022-04_fr/id2query.json ~/../gonzagab/Kodicare/qwant-data/2022-04_fr/qrels.txt ~/projects/qwant-data/2022-04_fr/split-collection/queries-inside.json ~/projects/qwant-data/2022-04_fr/split-collection/qrels-inside.txt ~/projects/qwant-data/2022-04_fr/split-collection/queries-outside.json ~/projects/qwant-data/2022-04_fr/split-collection/qrels-outside.txt

import sys
import os
import json
import re
import random

random.seed(10)

filename_input_queries = sys.argv[1]
filename_input_qrels = sys.argv[2]
filename_output_queries_inside = sys.argv[3]
filename_output_qrels_inside = sys.argv[4]
filename_output_queries_outside = sys.argv[5]
filename_output_qrels_outside = sys.argv[6]
# might be set to undefined:
filename_queries_to_merge = sys.argv[9]

percentage = sys.argv[7]
min_qrels = sys.argv[8]

output_queries_inside = {}
output_qrels_inside = {}
output_queries_outside = {}
output_qrels_outside = {}

queryids_inside = []
query_titles = {}
query_ids = {}

queries_file = open(filename_input_queries)
queries = json.load(queries_file)

qrel_numbers = {}

good_queries = []
representant_queries = []
new_query_ids = {}

# Split the queries
for iterator in queries:
    queryid = iterator
    query = queries[iterator]

    query_titles[queryid] = query
    query_ids[query] = queryid

    rng = random.randint(0,100)
    if (rng >= int(percentage)):
        queryids_inside.append(queryid)

# Read manually created sets of queries
if (not filename_queries_to_merge == "undefined"):
    queries_to_merge = open(filename_queries_to_merge)
    for line in queries_to_merge:
        queries = line.split("\t")
        queries.pop(0)
        setid = "q0"
        for query in queries:
            query = query.rstrip("\n")
            if (not query):
                continue
            if (not query in query_ids):
                continue

            queryid = query_ids[query]
            good_queries.append(queryid)

            if (setid == "q0"):
                setid = queryid
                representant_queries.append(setid)
            else:
                # If the representative id is in the inside queries
                if (setid in queryids_inside):
                    
                    # If this query is already in inside queries don't do anything
                    # Else put it into inside queries

                    if (not queryid in queryids_inside):
                        queryids_inside.append(queryid)

                # If it is not in the inside queries
                else:

                    # If the query is inside the queries
                    if (queryid in queryids_inside):
                        # Remove it
                        queryids_inside.remove(queryid)

            new_query_ids[queryid] = setid
    queries_to_merge.close()

# For the queries:
# If they are not in the approved queries, do not put them to inside/outside lists
# For the qrels:
# If the query is not in the approved queries, then do not put the corresponding qrels on the output
# Merging:
#   Queries: only keep one query as a representant
#   Qrels: 

# Calculate the qrels
with open(filename_input_qrels) as data_qrel:
    for line in data_qrel:
        line = line.rstrip()
        queryid, zero, docid, relevace = line.split()

        # Skip explicit content
        if (not filename_queries_to_merge == "undefined"):
            if (not queryid in good_queries):
                continue

        if queryid in qrel_numbers:
            old_qrel_num = qrel_numbers[queryid]
            qrel_numbers[queryid] = old_qrel_num + 1
        else:
            qrel_numbers[queryid] = int(1)

# Save everything
with open(filename_input_qrels) as data_qrel:
    for line in data_qrel:
        line = line.rstrip()
        queryid, zero, docid, relevance = line.split()

        newqueryid = queryid

        # Skip explicit content
        if (not filename_queries_to_merge == "undefined"):
            if (not queryid in good_queries):
                continue
            newqueryid = new_query_ids[queryid]

        if (int(qrel_numbers[queryid]) < int(min_qrels)):
            continue
        
        if (queryid in queryids_inside):
            if newqueryid + " " + docid in output_qrels_inside:
                # If already in the list
                oldrelevance = output_qrels_inside[newqueryid + " " + docid]
                if (relevance != oldrelevance):
                    if ((relevance == "1" and oldrelevance == "2") or (relevance == "2" and oldrelevance == "1")):
                        output_qrels_inside[newqueryid + " " + docid] = "1"
                    if ((relevance == "0" and (oldrelevance == "1" or oldrelevance == "2")) or ((relevance == "1" or relevance == "2") and oldrelevance == "0")):
                        output_qrels_inside[newqueryid + " " + docid] = "-1"
            else:
                # Merging the qrels
                output_qrels_inside[newqueryid + " " + docid] = relevance

            #if (not queryid in output_queries_inside):
            #    title = query_titles[queryid]
            #
            #    if (not filename_queries_to_merge == "undefined"):
            #        if (queryid in representant_queries):
            #            output_queries_inside[queryid] = title
            #    else:
            #        output_queries_inside[queryid] = title
        else:
            if newqueryid + " " + docid in output_qrels_outside:
                oldrelevance = output_qrels_outside[newqueryid + " " + docid]
                if (relevance != oldrelevance):
                    if ((relevance == "1" and oldrelevance == "2") or (relevance == "2" and oldrelevance == "1")):
                        output_qrels_outside[newqueryid + " " + docid] = "1"
                    if ((relevance == "0" and (oldrelevance == "1" or oldrelevance == "2")) or ((relevance == "1" or relevance == "2") and oldrelevance == "0")):
                        output_qrels_inside[newqueryid + " " + docid] = "-1"
            else:
                # Merging the qrels
                output_qrels_outside[newqueryid + " " + docid] = relevance

            #if (not queryid in output_queries_outside):
            #    title = query_titles[queryid]
            #
            #    if (not filename_queries_to_merge == "undefined"):
            #        if (queryid in representant_queries):
            #            output_queries_outside[queryid] = title
            #    else:
            #        output_queries_outside[queryid] = title

inside_qrels_file = open(filename_output_qrels_inside, "w")
for output_qrel_inside in output_qrels_inside:
    relevance = output_qrels_inside[output_qrel_inside]
    if (relevance == "-1"):
        continue

    query, document = output_qrel_inside.split()
    print_line = query + " 0 " + document + " " + relevance
    print(print_line, file=inside_qrels_file)

    if (not query in output_queries_inside):
        title = query_titles[query]
        output_queries_inside[query] = title

inside_qrels_file.close()

outside_qrels_file = open(filename_output_qrels_outside, "w")
for output_qrel_outside in output_qrels_outside:
    relevance = output_qrels_outside[output_qrel_outside]
    if (relevance == "-1"):
        continue

    query, document = output_qrel_outside.split()
    print_line = query + " 0 " + document + " " + relevance
    print(print_line, file=outside_qrels_file)

    if (not query in output_queries_outside):
        title = query_titles[query]
        output_queries_outside[query] = title

outside_qrels_file.close()

json_inside_queries = json.dumps(output_queries_inside)
with open(filename_output_queries_inside, "w") as inside_queries_file:
    inside_queries_file.write(json_inside_queries)

json_outside_queries = json.dumps(output_queries_outside)
with open(filename_output_queries_outside, "w") as outside_queries_file:
    outside_queries_file.write(json_outside_queries)

