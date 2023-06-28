import os
import sys
import math
from scipy.stats import norm
import statistics


input_directory = sys.argv[1]
collection = sys.argv[2]

map_scores = {}
p10_scores = {}
ndcg_scores = {}
ndcg_10_scores = {}
recall_scores = {}
num_systems = {}
max_systems = 0
queries = [] 

for root, dirs, files in os.walk(input_directory):
    for filename in files:

        if (not collection + ".score" in filename):
            continue

        with open(os.path.join(root, filename), "r") as input_file:
            for line in input_file:
                measure, query, score = line.split()

                if (query == "all"):
                    continue

                if (not query in queries):
                    queries.append(query)

                if (measure == "map"):
                    if (query in map_scores):
                        map_scores[query].append(score)
                        num_systems[query] = num_systems[query] + 1

                        if (num_systems[query] > max_systems):
                            max_systems = num_systems[query]

                    else:
                        map_scores[query] = [score]
                        num_systems[query] = 1
    
                        if (num_systems[query] > max_systems):
                            max_systems = num_systems[query]

                if (measure == "P_10"):
                    if (query in p10_scores):
                        p10_scores[query].append(score)
                    else:
                        p10_scores[query] = [score]

                if (measure == "ndcg"):
                    if (query in ndcg_scores):
                        ndcg_scores[query].append(score)
                    else:
                        ndcg_scores[query] = [score]

                if (measure == "ndcg_cut_10"):
                    if (query in ndcg_10_scores):
                        ndcg_10_scores[query].append(score)
                    else:
                        ndcg_10_scores[query] = [score]

                if (measure == "recall_1000"):
                    if (query in recall_scores):
                        recall_scores[query].append(score)
                    else:
                        recall_scores[query] = [score]


map_mean_per_query = {}
p10_mean_per_query = {}
ndcg_mean_per_query = {}
ndcg_10_mean_per_query = {}
recall_mean_per_query = {}

map_sd_per_query = {}
p10_sd_per_query = {}
ndcg_sd_per_query = {}
ndcg_10_sd_per_query = {}
recall_sd_per_query = {}

queries_num = len(queries)

for query in queries:

    # MAP scores
    map_total = 0.0
    map_sd_total = 0.0
    p10_total = 0.0
    p10_sd_total = 0.0
    ndcg_total = 0.0
    ndcg_sd_total = 0.0
    ndcg_10_total = 0.0
    ndcg_10_sd_total = 0.0
    recall_total = 0.0
    recall_sd_total = 0.0

    map_mean = 0.0
    map_sd = 0.0
    p10_mean = 0.0
    p10_sd = 0.0
    ndcg_mean = 0.0
    ndcg_sd = 0.0
    ndcg_10_mean = 0.0
    ndcg_10_sd = 0.0
    recall_mean = 0.0
    recall_sd = 0.0

    #####

    for value in map_scores[query]:
        map_total += float(value)

    map_mean = float(map_total / int(max_systems))

    for value in map_scores[query]:
        map_sd = float((float(value) - map_mean)**2)
        map_sd_total += map_sd

    map_sd = float(math.sqrt((map_sd_total) / (int(max_systems) - 1)))

    map_mean_per_query[query] = map_mean
    map_sd_per_query[query] = map_sd

    #if (query == "q092210070"):
    #    print (str(map_total), str(map_sd_total), str(map_mean), str(map_sd), str(queries_num), str(max_systems))

    #####

    for value in p10_scores[query]:
        p10_total += float(value)

    p10_mean = float(p10_total / int(max_systems))

    for value in p10_scores[query]:
        p10_sd_total += (float(value)- p10_mean)**2

    p10_sd = math.sqrt((p10_sd_total) / (int(max_systems) - 1))

    p10_mean_per_query[query] = p10_mean
    p10_sd_per_query[query] = p10_sd

    #####

    for value in ndcg_scores[query]:
        ndcg_total += float(value)

    ndcg_mean = ndcg_total / int(max_systems)

    for value in ndcg_scores[query]:
        ndcg_sd_total += (float(value) - ndcg_mean)**2

    ndcg_sd = math.sqrt((ndcg_sd_total) / (int(max_systems) - 1))

    ndcg_mean_per_query[query] = ndcg_mean
    ndcg_sd_per_query[query] = ndcg_sd

    #####

    for value in ndcg_10_scores[query]:
        ndcg_10_total += float(value)
    
    ndcg_10_mean = ndcg_10_total / int(max_systems)

    for value in ndcg_10_scores[query]:
        ndcg_10_sd_total += (float(value) - ndcg_10_mean)**2

    ndcg_10_sd = math.sqrt((ndcg_10_sd_total) / (int(max_systems) - 1))

    ndcg_10_mean_per_query[query] = ndcg_10_mean
    ndcg_10_sd_per_query[query] = ndcg_10_sd

    #####

    for value in recall_scores[query]:
        recall_total += float(value)

    recall_mean = recall_total / int(max_systems)

    for value in recall_scores[query]:
        recall_sd_total += (float(value) - recall_mean)**2

    recall_sd = math.sqrt((recall_sd_total) / (int(max_systems) - 1))

    recall_mean_per_query[query] = recall_mean
    recall_sd_per_query[query] = recall_sd

    print (query + "\t" + str(map_mean) + "\t" + str(map_sd) + "\t" + str(p10_mean) + "\t" + str(p10_sd) + "\t" + str(ndcg_mean) + "\t" + str(ndcg_sd) + "\t" + str(ndcg_10_mean) + "\t" + str(ndcg_10_sd) + "\t" + str(recall_mean) + "\t" + str(recall_sd))

