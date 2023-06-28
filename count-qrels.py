#!/usr/bin/python

import sys
import os
import json

all_queries_filename = sys.argv[1]
qrels_filename = sys.argv[2]

highly_relevant = {}
relevant = {}

f = open(qrels_filename)
for line in f:
    line = line.rstrip("\n")
    qid, zero, docid, relevance = line.split()

    if (int(relevance) >= 1):
        if qid in relevant:
            relevant[qid] = relevant[qid] + 1
        else:
            relevant[qid] = 1

    if (int(relevance) >= 2):
        if qid in highly_relevant:
            highly_relevant[qid] = highly_relevant[qid] + 1
        else:
            highly_relevant[qid] = 1

f = open(all_queries_filename)
for line in f:
    line = line.rstrip("\n")
    qid, rest = line.split('\t', 1)

    relevant_score = 0
    highly_relevant_score = 0

    if qid in relevant:
        relevant_score = relevant[qid]

    if qid in highly_relevant:
        highly_relevant_score = highly_relevant[qid]

    print (qid + " " + str(highly_relevant_score) + " " + str(relevant_score))


