#!/usr/bin/python

import sys
import fasttext

filename = sys.argv[1]
#output_dir = sys.argv[2]
mode = "french"
mode = sys.argv[2]

translated_sentences = []

model = fasttext.load_model('lid.176.bin')

with open(filename, 'r') as inputfile:

    translated_senteces = []

    for line in inputfile.readlines():

        line = line.rstrip('\n')

        if (line == ""):
            continue

        if (line == "</DOC>"):
            print("")

        if (line == "<DOC>" or line == "</DOC>" or line == "<TEXT>" or line == "</TEXT>" or "</DOCNO>" in line or "</DOCID>" in line):
            continue

        pred = model.predict(line, k=50)
        score_best, score_abs, score_rel = pred[1][0], 0, 0
        for i in range(len(pred[0])):
            if pred[0][i][9:] == 'fr':
                score_abs = pred[1][i]
                score_rel = pred[1][i] / score_best
                break

        if (score_rel < 0.05):
            continue

        #line_encoded = line.encode('utf8')
        line_encoded = bytearray(line, 'utf-8')

        # Find too long  sentences
        if (len(line_encoded) > 500):

            # Shorten the sentence in bytes
            shortened_line_encoded = line_encoded[0:500]

            shortened_line = ""
            e = "No failure yet"
            while e:
                try:
                    shortened_line = shortened_line_encoded.decode()
                except Exception as err:
                    shortened_line_encoded.pop()
                else:
                    e = ""
            
            #print(shortened_line_encoded)
            shortened_line = shortened_line_encoded.decode()

            # Shorten the sentence and deduplicate
            if (not shortened_line in translated_sentences):
                print(shortened_line)
                translated_sentences.append(shortened_line)
        else:

            # Just deduplicate and print
            if (not line in translated_sentences):
                print(line)
                translated_sentences.append(line)

