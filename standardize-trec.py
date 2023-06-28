import os
import sys
import math
from scipy.stats import norm
import statistics as stats

input_directory = sys.argv[1]
collection = sys.argv[2]
output_directory = sys.argv[3]
queries_num = sys.argv[4]

map_scores = {}
p10_scores = {}
ndcg_scores = {}
ndcg_10_scores = {}
recall_scores = {}
num_systems = {}
max_num_systems = 0
queries = [] 

for root, dirs, files in os.walk(input_directory):
    for filename in files:

        print (filename)

        if (not ".score" in filename):
            continue

        if (not "." + collection in filename):
            continue

        #print("here")

        with open(os.path.join(root, filename), "r") as input_file:
            for line in input_file:
                measure, query, score = line.split()

                if (query == "all"):
                    continue

                if (not query in queries):
                    queries.append(query)

                if (measure == "map"):
                    if (query in map_scores):
                        map_scores[query].append(float(score))
                        num_systems[query] = num_systems[query] + 1

                    else:
                        map_scores[query] = [float(score)]
                        num_systems[query] = 1

                    if (int(num_systems[query]) > int(max_num_systems)):
                        max_num_systems = int(num_systems[query])

                if (measure == "P_10"):
                    if (query in p10_scores):
                        p10_scores[query].append(float(score))
                    else:
                        p10_scores[query] = [float(score)]

                if (measure == "ndcg"):
                    if (query in ndcg_scores):
                        ndcg_scores[query].append(float(score))
                    else:
                        ndcg_scores[query] = [float(score)]

                if (measure == "ndcg_cut_10"):
                    if (query in ndcg_10_scores):
                        ndcg_10_scores[query].append(float(score))
                    else:
                        ndcg_10_scores[query] = [float(score)]

                if (measure == "recall_1000"):
                    if (query in recall_scores):
                        recall_scores[query].append(float(score))
                    else:
                        recall_scores[query] = [float(score)]


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

#print (map_scores["q062210272"])
#print(str(max_num_systems))

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

    map_mean = float(map_total / int(max_num_systems))

    zeros_missing = int(max_num_systems) - len(map_scores[query])
    
    map_scores_query = map_scores[query]
    p10_scores_query = p10_scores[query]
    recall_scores_query = recall_scores[query]
    ndcg_scores_query = ndcg_scores[query]
    ndcg_10_scores_query = ndcg_10_scores[query]

    for i in range(zeros_missing):
        map_scores_query.append(0.0)
        p10_scores_query.append(0.0)
        recall_scores_query.append(0.0)
        ndcg_scores_query.append(0.0)
        ndcg_10_scores_query.append(0.0)

    map_sd = stats.stdev(map_scores_query)

    #
    #for value in map_scores[query]:
    #    map_sd = float((float(value) - map_mean)**2)
    #    map_sd_total += map_sd
    #
    #map_sd = float(math.sqrt((map_sd_total) / (int(max_num_systems) - 1)))

    map_mean_per_query[query] = map_mean
    map_sd_per_query[query] = map_sd

    #####

    for value in p10_scores[query]:
        p10_total += float(value)

    p10_mean = float(p10_total / int(max_num_systems))

    #for value in p10_scores[query]:
    #    p10_sd_total += (float(value)- p10_mean)**2
    #
    #p10_sd = math.sqrt((p10_sd_total) / (int(max_num_systems)))

    p10_sd = stats.stdev(p10_scores_query)

    p10_mean_per_query[query] = p10_mean
    p10_sd_per_query[query] = p10_sd

    #####

    for value in ndcg_scores[query]:
        ndcg_total += float(value)

    ndcg_mean = ndcg_total / int(max_num_systems)

    #for value in ndcg_scores[query]:
    #    ndcg_sd_total += (float(value) - ndcg_mean)**2
    #
    #ndcg_sd = math.sqrt((ndcg_sd_total) / (int(max_num_systems)))

    ndcg_sd = stats.stdev(ndcg_scores_query)

    ndcg_mean_per_query[query] = ndcg_mean
    ndcg_sd_per_query[query] = ndcg_sd

    #####

    for value in ndcg_10_scores[query]:
        ndcg_10_total += float(value)
    
    ndcg_10_mean = ndcg_10_total / int(max_num_systems)

    #for value in ndcg_10_scores[query]:
    #    ndcg_10_sd_total += (float(value) - ndcg_10_mean)**2
    #
    #ndcg_10_sd = math.sqrt((ndcg_10_sd_total) / (int(max_num_systems)))

    ndcg_10_sd = stats.stdev(ndcg_10_scores_query)

    ndcg_10_mean_per_query[query] = ndcg_10_mean
    ndcg_10_sd_per_query[query] = ndcg_10_sd

    #####

    for value in recall_scores[query]:
        recall_total += float(value)

    recall_mean = recall_total / int(max_num_systems)

    #for value in recall_scores[query]:
    #    recall_sd_total += (float(value) - recall_mean)**2
    #
    #recall_sd = math.sqrt((recall_sd_total) / (int(max_num_systems)))

    recall_sd = stats.stdev(recall_scores_query)

    recall_mean_per_query[query] = recall_mean
    recall_sd_per_query[query] = recall_sd

    print (query + "\t" + str(map_mean) + "\t" + str(map_sd) + "\t" + str(p10_mean) + "\t" + str(p10_sd) + "\t" + str(recall_mean) + "\t" + str(recall_sd) + "\t" + str(ndcg_mean) + "\t" + str(ndcg_sd) + "\t" + str(ndcg_10_mean) + "\t" + str(ndcg_10_sd))

#print(map_mean_per_query["q062210272"])
#print(map_sd_per_query["q062210272"])

for root, dirs, files in os.walk(input_directory):
    for filename in files:

        if (not ".score" in filename):
            continue

        if (not "." + collection in filename):
            continue

        print(filename)

        normalized_trec_file = ""
        total_normalized_map = 0
        total_normalized_p10 = 0
        total_normalized_ndcg = 0
        total_normalized_ndcg_10 = 0
        total_normalized_recall = 0

        with open(os.path.join(root, filename), "r") as input_file:
            for line in input_file:
                measure, query, score = line.split()

                if (query == "all"):
                    continue

                if (measure == "map"):

                    map_query_mean = map_mean_per_query[query]
                    map_query_sd = map_sd_per_query[query]

                    if (map_query_sd == 0):
                        map_normalized_score = 0
                    else:
                        map_z_score = (float(score) - map_query_mean) / map_query_sd
                        map_normalized_score = norm.cdf(float(score), map_query_mean, map_query_sd)

                    normalized_trec_file += measure + "\t\t" + query + "\t%.4f\n" % map_normalized_score
                    total_normalized_map += map_normalized_score

                    #if (query == "q062210272"):
                    #    print(str(score))
                    #    print(str(map_normalized_score))
                    #    print(str(map_query_mean))
                    #    print(str(map_query_sd))

                if (measure == "P_10"):

                    p10_query_mean = p10_mean_per_query[query]
                    p10_query_sd = p10_sd_per_query[query]

                    if (p10_query_sd == 0):
                        p10_normalized_score = 0
                    else:
                        p10_z_score = (float(score) - p10_query_mean) / p10_query_sd
                        p10_normalized_score = norm.cdf(float(score), p10_query_mean, p10_query_sd)

                    normalized_trec_file += measure + "\t\t" + query + "\t%.4f\n" % p10_normalized_score
                    total_normalized_p10 += p10_normalized_score

                if (measure == "ndcg"):

                    ndcg_query_mean = ndcg_mean_per_query[query]
                    ndcg_query_sd = ndcg_sd_per_query[query]

                    if (ndcg_query_sd == 0):
                        ndcg_normalized_score = 0
                    else:
                        ndcg_z_score = (float(score) - ndcg_query_mean) / ndcg_query_sd
                        ndcg_normalized_score = norm.cdf(float(score), ndcg_query_mean, ndcg_query_sd)

                    normalized_trec_file += measure + "\t\t" + query + "\t%.4f\n" % ndcg_normalized_score
                    total_normalized_ndcg += ndcg_normalized_score

                if (measure == "ndcg_cut_10"):

                    ndcg_10_query_mean = ndcg_10_mean_per_query[query]
                    ndcg_10_query_sd = ndcg_sd_per_query[query]

                    if (ndcg_10_query_sd == 0):                
                        ndcg_10_normalized_score = 0
                    else:
                        ndcg_10_z_score = (float(score) - ndcg_10_query_mean) / ndcg_10_query_sd
                        ndcg_10_normalized_score = norm.cdf(float(score), ndcg_10_query_mean, ndcg_10_query_sd)

                    normalized_trec_file += measure + "\t" + query + "\t%.4f\n" % ndcg_10_normalized_score
                    total_normalized_ndcg_10 += ndcg_10_normalized_score

                if (measure == "recall_1000"):

                    recall_mean = recall_mean_per_query[query]
                    recall_sd = recall_sd_per_query[query]

                    if (recall_sd == 0):
                        recall_normalized_score = 0
                    else:
                        recall_z_score = (float(score) - recall_mean) / recall_sd
                        recall_normalized_score = norm.cdf(float(score), recall_mean, recall_sd)

                    normalized_trec_file += measure + "\t" + query + "\t%.4f\n" % recall_normalized_score
                    total_normalized_recall += recall_normalized_score

                    #print(query + "\t" + str(score) + "\t" + str(recall_mean) + "\t" + str(recall_sd))


            average_map = total_normalized_map / float(queries_num)
            normalized_trec_file += "map\tall\t%.4f\n" % average_map

            average_p10 = total_normalized_p10 / float(queries_num)
            normalized_trec_file += "P_10\tall\t%.4f\n" % average_p10

            average_recall = total_normalized_recall / float(queries_num)
            normalized_trec_file += "recall_1000\tall\t%.4f\n" % average_recall

            average_ndcg = total_normalized_ndcg / float(queries_num)
            normalized_trec_file += "ndcg\tall\t%.4f\n" % average_ndcg

            average_ndcg_10 = total_normalized_ndcg_10 / float(queries_num)
            normalized_trec_file += "ndcg_cut_10\tall\t%.4f\n" % average_ndcg_10 

            output_filename = os.path.join(output_directory, "normalized_" + filename)
            f = open(output_filename, "w")
            f.write(normalized_trec_file)
            f.close()
