import csv
import json
from pathlib import Path
import ujson
# read multiple files under one folder
from glob import glob 


# define the file path and output file path
base_path = Path("M:\Projekt\HortiSem\data")

inputfile_path = base_path/'entity_vocabulary_raw'
patterns_filepath = base_path/'entity_patterns'

# get a list of all the files with .csv or .tsv, two groups
all_input_files = inputfile_path.glob('*.tsv')
     
# a function to read one csv file or tsv file
def read_csv(file,label):
    # read csv into a dictionary
    reader = csv.DictReader(open(file,'r'),delimiter='\t')
    
    for row in reader:
        if '(' in row["KODETEXT"]:
            yield {"label":label,"pattern": row["KODETEXT"].split("(")[0].replace('"','')} # only german language
            yield {"label":label,"pattern": row["KODETEXT"].replace('"','')}  # german (latain name)
        else: 
            yield {"label":label,"pattern": row["KODETEXT"].replace('"','')}

# write multiple output files in JSONL format
for f in all_input_files:
    data = [ujson.dumps(text, escape_forward_slashes= False,ensure_ascii= False) for text in read_csv(f,f.stem)]
    Path(patterns_filepath,f"{f.stem}.jsonl").open('w',encoding="utf-8").write('\n'.join(data))
   

# # a function to read one csv file
# def read_csv(file,label):
#     # read csv into a dictionary
#     reader = csv.DictReader(open(file,'r'),delimiter=',')
#     for row in reader:
#         yield {"label":label,"pattern": row["KODETEXT"]} 
# # write all patterns into one Jsonl file
# new_patterns = []
# for f in all_input_files:
#     for text in read_csv(f,f.stem):
#         data = ujson.dumps(text, escape_forward_slashes= False,ensure_ascii= False)
#         new_patterns.append(data)
# Path(patterns_filepath ,"ABO_patterns.jsonl").open('w',encoding="utf-8").write('\n'.join(new_patterns))


