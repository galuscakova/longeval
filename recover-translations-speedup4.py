#!/usr/bin/python3

import sys
import os
import json

translations_directory = sys.argv[1]
french_clean_directory = sys.argv[2]
french_original_directory = sys.argv[3]
output_directory = sys.argv[4]
mode = sys.argv[5] # Either trec or json

def process_file(french_original_filename, french_clean_filename, translated_filename):

    # Read and save the clean file
    clean_lines = []
    clean_lines_beginnings = []
    with open(french_clean_filename) as file_clean:
        for line in file_clean:
            line = line.rstrip('\n')
            line_beginning = line[0:400]
            clean_lines.append(line)

            #if (line in clean_lines_beginnings):
                #print ("Problem: the same beginning of the line: " + line_beginning)
            clean_lines_beginnings.append(line_beginning)

    # Read and save the translated file
    translated_lines = []
    with open(translated_filename) as file_translated:
        for line in file_translated:
            line = line.rstrip('\n')
            translated_lines.append(line)

    # Go through the original file
    clean_line_id = 0
    output_file = ""

    zipped_dictionary = dict(zip(clean_lines_beginnings, translated_lines))
    output_list = []

    with open(french_original_filename) as file_original:

        docno = "-1"
        document_line = ""

        for line in file_original:
            line = line.rstrip('\n')
            line_beginning = line[0:400]

            translated_sentence = ""

            # Do not process the TREC "commands"
            # ! Might be improved
            if ("<DOC>" in line or "</DOC>" in line or "<DOCNO>" in line or "<DOCID>" in line or "<TEXT>" in line or "</TEXT>" in line):

                if ("<DOCNO>" in line):
                    docno = line
                    docno = docno.replace("<DOCNO>", "")
                    docno = docno.replace("</DOCNO>", "")

                if ("trec" in mode or "TREC" in mode or "Trec" in mode):
                    output_list.append(line + "\n")
            
                    #if ("</DOC>" in line):
                    #    print(output_file)

                if ("json" in mode or "JSON" in mode or "Json" in mode):
                    if ("</DOC>" in line):
                        document = {"id": docno, "contents": document_line}
                        output_list.append(document)

                        document_line = ""

            else:

                # Do not translate too short sentences
                if (len(line) == 1):
                    translated_sentence = line
            
                else:
                    # Find if asked for the translation
                    try: 
                        translated_sentence = zipped_dictionary[line_beginning]
                    except KeyError:
                        # Otherwise, we have no translation and just use the original sentence in French
                        translated_sentence = line
            
                if ("trec" in mode or "TREC" in mode or "Trec" in mode):
                    output_list.append(translated_sentence + "\n")

                if ("json" in mode or "JSON" in mode or "Json" in mode):
                    document_line = document_line + translated_sentence + "\n"

    output_file = ""

    if ("json" in mode or "Json" in mode or "JSON" in mode):
        output_file = json.dumps(output_list)
        
    if ("trec" in mode or "TREC" in mode or "Trec" in mode):
        output_file = ''.join(output_list)
    
    return(output_file)

for filename in os.listdir(french_original_directory):
    
    french_original_filename = os.path.join(french_original_directory, filename)
    french_clean_filename = os.path.join(french_clean_directory, filename)
    translated_filename = os.path.join(translations_directory, filename)
    translated_filename = translated_filename.replace("collector_kodicare_", "collector_kodicare_english_")
    output_filename = os.path.join(output_directory, filename)
    print(output_filename)

    output = process_file(french_original_filename, french_clean_filename, translated_filename)

    output_file = open(output_filename, "w")
    output_file.write(output)
    output_file.close()


