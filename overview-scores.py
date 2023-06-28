import os
import sys
import math
import statistics
import re

input_directory = sys.argv[1]
collection = sys.argv[2]

map_score = "0"
p10_score = "0"
ndcg_score = "0"
ndcg_10_score = "0"
recall_score = "0"

for root, dirs, files in os.walk(input_directory):
    for filename in files:

        if (not ".score" in filename):
            continue

        if (not "." + collection in filename):
            continue

        with open(os.path.join(root, filename), "r") as input_file:
            for line in input_file:
                line = line.rstrip("\n")

                measure, query, score = re.split(r"\s+", line)

                if (not query == "all"):
                    continue

                if (measure == "map"):
                    map_score = score

                if (measure == "P_10"):
                    p10_score = score

                if (measure == "ndcg"):
                    ndcg_score = score

                if (measure == "ndcg_cut_10"):
                    ndcg_10_score = score
                    print (filename + "\t" + map_score + "\t" + p10_score + "\t" + ndcg_score + "\t" + ndcg_10_score + "\t" + recall_score)


                if (measure == "recall_1000"):
                    recall_score = score
                    #print (filename + "\t" + map_score + "\t" + p10_score + "\t" + ndcg_score + "\t" + ndcg_10_score + "\t" + recall_score)




