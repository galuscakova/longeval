#!/usr/bin/python

import sys
import random

random.seed(1)

full_pool_5 = []
full_pool_5_10 = []
full_pool_10_30 = []
stratified_pool = []

# The list for the train set
#queries = ['q06221312', 'q06224677', 'q062216960', 'q06227968', 'q062216056', 'q062217348', 'q062217180', 'q06227537', 'q062217472', 'q062220278']
# The list for the heldout set
#queries = ["q06223111", "q062220549", "q062223332", "q06227214", "q06222807", "q062211754", "q06226280", "q062210990", "q06226328", "q062213762", "q062216217", "q062217637", "q062214373", "q06225415", "q062214361", "q062218996", "q062216531", "q062217640", "q062210941", "q062221273", "q06222011", "q06227380", "q062220965", "q062224471", "q062214534", "q062211871", "q06225394", "q062220044", "q062217065", "q062214587", "q062221541", "q062222130", "q06221728", "q062219794", "q06228206", "q0622404", "q062223909", "q062222273", "q06223951", "q06224970", "q062214170", "q062214315", "q062210272", "q062217643", "q062224532", "q062219087", "q062213628", "q062216851", "q062223808", "q062221297"]
#queries = ["q072213053", "q0722123", "q07224677", "q072226054", "q07221511", "q072228594", "q07223445", "q07229290", "q07227444", "q072220851", "q072223480", "q072225293", "q072221916", "q072225901", "q072214905", "q072213216", "q072216518", "q072214509", "q072219211", "q072224582", "q07221378", "q072223499", "q072226483", "q072227192", "q072226211", "q07222375", "q072215857", "q07228075", "q07226331", "q072227714", "q07221016", "q072226341", "q072213180", "q072213058", "q07222062", "q072225665", "q072228491", "q072224274", "q072218137", "q072226511", "q07225410", "q072216557", "q07228174", "q072212275", "q072218811", "q072217109", "q07227023", "q072211861", "q072212543", "q072220870"]
queries = ["q092230586", "q09227878", "q092232895", "q092221389", "q092233045", "q09229052", "q092225023", "q09225196", "q09227543", "q092229943", "q092235670", "q092229587", "q092217293", "q092218418", "q092227378", "q092231980", "q092236059", "q09228872", "q092214491", "q09229280", "q092222595", "q09221381", "q09224909", "q092232498", "q09229151", "q09225901", "q092221429", "q092212604", "q092213207", "q09225786", "q092223271", "q092222162", "q092210437", "q092218556", "q092230034", "q092232738", "q092210111", "q092232734", "q092215133", "q09229096", "q092235768", "q092225889", "q092215641", "q09225141", "q092211879", "q092236345", "q092213272", "q09223138", "q09221155", "q092225834"]

# Read all the outputs from the file
for filename in sys.argv[1:]:
    print (filename)
    
    with open(filename) as input_file:

        prev_query = "-"
        
        for line in input_file:

            query, q0, document, rank, score, desc = line.split()
            if (prev_query != query):
                real_rank = 1

            prev_query = query

            if ((not len(queries) == 0) and (not query in queries)):
                continue

            new_item = query + " " + document

            if (real_rank <= 5):
                if (not new_item in full_pool_5):
                    full_pool_5.append(new_item)

            elif (real_rank <= 10):
                if (not new_item in full_pool_5_10):
                    full_pool_5_10.append(new_item)

            elif (real_rank <= 30):
                if (not new_item in full_pool_10_30):
                    full_pool_10_30.append(new_item)

            real_rank = real_rank + 1

# Do stratified selection
for item in full_pool_5:
    stratified_pool.append(item)

for item in full_pool_5_10:
    if (not item in stratified_pool):
        num = random.random()
        if (num <= 0.5):
            stratified_pool.append(item)

for item in full_pool_10_30:
    if (not item in stratified_pool):
        num = random.random()
        if (num <= 0.25):
            stratified_pool.append(item)

for item in stratified_pool:
    print(item)

