import sys
import json

queries_filename = sys.argv[1]

queries_file = open(queries_filename)
data = json.load(queries_file)
for key in data:
        print (data[key])

queries_file.close()
