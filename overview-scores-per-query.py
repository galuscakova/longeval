import os
import sys
import math
import statistics
import re

input_directory = sys.argv[1]
collection = sys.argv[2]

results = {}
teams = []
queries = []

for root, dirs, files in os.walk(input_directory):
    for filename in files:

        if (not ".score" in filename):
            continue

        if (not "." + collection in filename):
            continue

        teams.append(filename)

        with open(os.path.join(root, filename), "r") as input_file:

            results[filename] = {}

            for line in input_file:
                line = line.rstrip("\n")

                measure, query, score = re.split(r"\s+", line)

                if (query == "all"):
                    continue

                if (not query in queries):
                    queries.append(query)

                if (measure == "ndcg"):
                    results[filename][query] = score                   

for query in queries:
    print ("\t" + query, end="")

print()

for team in teams:

    print(team, end="")

    for query in queries:

        score = ""
        if (query in results[team]):
            score = results[team][query]
        
        print ("\t" + score, end="")

    print()

