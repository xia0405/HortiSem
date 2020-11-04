import csv
import json
from pathlib import Path
import ujson
# read multiple files under one folder
from glob import glob 


# define the file path and output file path
base_path = Path("M:\Projekt\HortiSem\data")
inputfile_path = base_path/'dictionary_BBCH_Stadium'
outputfile_path = base_path/'dictionary_jsonl'

# get a list of all the files with .dsv
all_input_files = inputfile_path.glob('*.csv')

# a function to read one csv file
def read_csv(file):
    # read csv into a dictionary
    reader = csv.DictReader(open(file,'r'),delimiter=',')
    for row in reader:
        yield {"label":"BBCH_Stadium","pattern": row["KODETEXT"]} 
       
# # a function to read one csv file
# def read_csv(file,label):
#     # read csv into a dictionary
#     reader = csv.DictReader(open(file,'r'),delimiter=';')
    
#     for row in reader:
#         if '(' in row["KODETEXT"]:
#             yield {"label":label,"pattern": row["KODETEXT"].split("(")[0]} # only german language
#             yield {"label":label,"pattern": row["KODETEXT"]}  # german (latain name)
#         else: 
#             yield {"label":label,"pattern": row["KODETEXT"]}

#  write multiple output files in JSONL format
# for f in all_input_files:
#     data = [ujson.dumps(text, escape_forward_slashes= False,ensure_ascii= False) for text in read_csv(f,f.stem)]
    # Path(outputfile_path,f"{f.stem}.jsonl").open('w',encoding="utf-8").write('\n'.join(data))
   

# write all patterns into one Jsonl file
patterns_filepath = base_path/'patterns_jsonl'
new_patterns = []
for f in all_input_files:
    for text in read_csv(f):
        data = ujson.dumps(text, escape_forward_slashes= False,ensure_ascii= False)
        new_patterns.append(data)
Path(patterns_filepath ,"BBCH_patterns.jsonl").open('w',encoding="utf-8").write('\n'.join(new_patterns))


