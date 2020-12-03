# library to read the text from pdfs
import tika
tika.initVM()
from tika import parser

import os

import json
import re
import ujson
import warnings
warnings.filterwarnings("ignore")

# define the paths of input pdf files and the desired output in jsonl format
pdf_dir = r'M:\Projekt\HortiSem\data\WD-Meldungen2019\HE\Jahr2017\Feldbau'
text_dir = r'M:\Projekt\HortiSem\data\input_text\Feldbau_HE_2017.jsonl'

# # PDF file Prodigy streams generators
# def get_pdf_stream(pdf_dir):
#     for root, dirs, files in os.walk(pdf_dir):
#         for pdf_file in files:
#             path_to_pdf = os.path.join(root, pdf_file)
#             [stem, ext] = os.path.splitext(path_to_pdf)
#             if ext ==".pdf":
#                 pdf_contents = parser.from_file(path_to_pdf)
#                 yield {'text': pdf_contents["content"]}


# convert pdf to raw text and save in a dictionary with document IDs
def get_pdf_stream(pdf_dir):
    for root, dirs, files in os.walk(pdf_dir):
        for pdf_file in files:
            path_to_pdf = os.path.join(root, pdf_file)
            [stem, ext] = os.path.splitext(path_to_pdf)
            if ext ==".pdf":
                pdf_contents = parser.from_file(path_to_pdf)
                doc = pdf_contents["content"]
                 # split the doc into paragraphs
                # cleared_doc = re.sub(r'(\s{1,})','',doc) # clear text
                paragraphs = re.split(r'\.\s?\n{2,}',doc)

                # paragraph starts from 1
                par_id = 1
                # loop over each paragraph to assign a id
                for par in paragraphs:
                    cleared_par = re.sub(r'\n','',par)  # clear text (-\n)|
                    # cleared_par = re.sub(r'[W]\s','W',cleared_par)  # clear text
                    yield {'text': cleared_par,'meta':{'Source':pdf_file, 'Paragraph_id':par_id}}
                    par_id +=1  #update paragraph id


# Create a .jsonl file from the text
data = [ujson.dumps(text, escape_forward_slashes= False,ensure_ascii= False) for text in get_pdf_stream(pdf_dir)]
with open(text_dir,'w',encoding="utf-8") as f:
    f.write('\n'.join(data))
