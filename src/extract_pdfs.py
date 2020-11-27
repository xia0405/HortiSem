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
pdf_dir = r'M:\Projekt\HortiSem\data\test_data'
text_dir = r'M:\Projekt\HortiSem\data\input_text\test_data.jsonl'

# PDF file Prodigy streams generators
def get_pdf_stream(pdf_dir):
    for root, dirs, files in os.walk(pdf_dir):
        for pdf_file in files:
            path_to_pdf = os.path.join(root, pdf_file)
            [stem, ext] = os.path.splitext(path_to_pdf)
            if ext ==".pdf":
                pdf_contents = parser.from_file(path_to_pdf)
                yield {'text': pdf_contents["content"]}


# Create a .jsonl file from the text
data = [ujson.dumps(text, escape_forward_slashes= False,ensure_ascii= False) for text in get_pdf_stream(pdf_dir)]
with open(text_dir,'w',encoding="utf-8") as f:
    f.write('\n'.join(data))


# # convert pdf to raw text and save in a dictionary with document IDs
# def get_pdf_stream(pdf_dir):
#     pdf_dir = Path(pdf_dir)
#     #doc_id = 1   # document ID start with 1
#     for pdf_file in pdf_dir.iterdir():
#         par_id = 1
#         # read PDF to a list of texts 
#         file_obj = pdf_file.open('rb')
#         texts = slate.PDF(file_obj)
#         # join multiple pages into one text
#         doc = ' '.join(texts)
#         # split the doc into paragraphs
#         cleared_doc = re.sub(r'(\n\s{2,})|(\n\f)','',doc)  # clear text

#         paragraphs = re.split(r'\n{2,}',cleared_doc)

#         # loop over each paragraph to assign a id
#         for par in paragraphs:
#             cleared_par = re.sub(r'\n|(-\n)','',par)  # clear text
#             cleared_par = re.sub(r'[W]\s','W',cleared_par)  # clear text
#             yield {'text': cleared_par,'meta':{'Source':f'{pdf_file.stem}.pdf', 'Paragraph_id':par_id}}
#             par_id +=1  #update paragraph id
# #         #doc_id +=1 # update document ID 

# # convert pdf to raw text and save in a dictionary with document IDs
# def get_pdf_stream(pdf_dir):
#     pdf_dir = Path(pdf_dir)
#     for pdf_file in pdf_dir.iterdir():
#         par_id = 1
#         # read PDF to a list of texts 
#         file_obj = pdf_file.open('rb')
#         texts = slate.PDF(file_obj)
#         # join multiple pages into one text
#         doc = ' '.join(texts)
#         # split the doc into paragraphs
#         cleared_doc = re.sub(r'(\n{1,})|(\f)|(\n-)','',doc)  # clear text

#         paragraphs = re.split(r'\s{2,}',cleared_doc)

#         # loop over each paragraph to assign a id
#         for par in paragraphs:
#             cleared_par = re.sub(r'-\n','',par)  # clear text
#             cleared_par = re.sub(r'[W]\s','W',cleared_par)  # clear text
#             yield {'text': cleared_par,'meta':{'Source':f'{pdf_file.stem}.pdf', 'Paragraph_id':par_id}}
#             par_id +=1  #update paragraph id






# # Create a .jsonl file from the text
# def write_jsonl(file_path, pdf_dir):
#     data = [ujson.dumps(text, escape_forward_slashes= False,ensure_ascii= False) for text in get_pdf_stream(pdf_dir)]
#     Path(file_path).open('w',encoding="utf-8").write('\n'.join(data))

# write_jsonl(text_dir,pdf_dir)


