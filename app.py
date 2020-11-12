# way to upload pdf file: endpoint
# way to save the pdf file
# way to convert pdf to proper input text
# function to NER model
# show the results

import os
import re
import shutil
import csv
from pathlib import Path
# import base64
import slate3k as slate
from ml import nlp

from spacy.matcher import PhraseMatcher
from spacy.tokens import Span

from typing import Optional
from typing import List


from fastapi import FastAPI, File, UploadFile
from fastapi import Request
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="{{HortiSem.Named_Entity_Recognition}}",
    version="1.0",
    description="{{HortiSem.project_short_description}}"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


UPLOAD_FOLDER = r"M:\Projekt\HortiSem\static\upload_folder"
# ALLOWED_EXTENTIONS = {'pdf'}
class EntityMatcher(object):
    # name = "entity_matcher"

    def __init__(self, nlp, terms, label):
        patterns = [nlp.make_doc(text) for text in terms]
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add(label, None, *patterns)

    def __call__(self, doc):
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            span = Span(doc, start, end, label=match_id)
            doc.ents = list(doc.ents) + [span]
        return doc

# define the file path
base_path = Path("M:\Projekt\HortiSem\data")
inputfile_path = base_path/'dictionary_BOD_csv'
# get a list of all the files with .dsv
all_csv_files = inputfile_path.glob('*.csv')

for f in all_csv_files:   
    reader = csv.DictReader(open(f, 'r'),delimiter=',')   
    pattern_terms=[row["KODETEXT"] for row in  reader]
    entity_matcher = EntityMatcher(nlp, pattern_terms, f"{f.stem}")
    nlp.add_pipe(entity_matcher, name=f"entity_matcher_{f.stem}",after="ner")

def add_regex_entities(doc):
    label = "Zeit"
    regex_expression = r"\d{1,2}\.\d{1,2}\.\d{4}"
    spans = []
    for match in re.finditer(regex_expression, doc.text):  # find match in text
        start, end = match.span()  # get the matched token indices
        span = doc.char_span(start, end, label=label)
        spans.append(span)
    doc.ents = list(doc.ents) + spans
    return doc

nlp.add_pipe(add_regex_entities, name="add_regex_match",before="ner")

# def add_regex_entities(doc):
#     regex_expression = r"BBCH(\s?\d+)\s?(\/|\-|(bis)?)\s?(\d+)?"
#     spans = []
#     for match in re.finditer(regex_expression, doc.text):  # find match in text
#         start, end = match.span()  # get the matched token indices
#         span = doc.char_span(start, end, label="BBCH_Stadium")
#         spans.append(span)
#     doc.ents = list(doc.ents) + spans
#     return doc

# add custom components
# nlp.add_pipe(add_regex_entities, name="add_regex_match",before="ner")

def pdf_converter(pdf_path):
    # Read pdf and convert to plain text
    with open(pdf_path, 'rb') as f:  
        texts = slate.PDF(f)
    # join multiple pages into one text
    doc = ' '.join(texts)
    # clear text
    cleared_doc = re.sub(r'(\n{1,})|(\f)','',doc)  
    return cleared_doc

def predict(text, nlp_model):
    doc = nlp_model(text)
    ents = []
    for ent in doc.ents:
        ents.append({"entity":ent.text, "label":ent.label_})
    return ents



@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_object = file.file
    #create empty file to copy the file_object to
    Pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    upload_folder = open(Pdf_path, 'wb+')
    shutil.copyfileobj(file_object, upload_folder)
    upload_folder.close()
  
    # Process the text
    input_text = pdf_converter(Pdf_path)
    # Predict
    ents = predict(input_text,nlp)
    print(ents)
    return {"filename": file.filename, "text":input_text,"ents":ents}
    
# @app.post(
#     "/entities_by_type", response_model=RecordsEntitiesByTypeResponse, tags=["NER"]
# )
# async def extract_entities_by_type(body: RecordsRequest):
#     """Extract Named Entities from a batch of Records separated by entity label.
#         This route can be used directly as a Cognitive Skill in Azure Search
#         For Documentation on integration with Azure Search, see here:
#         https://docs.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-interface"""

#     res = []
#     documents = []

#     for val in body.values:
#         documents.append({"id": val.recordId, "text": val.data.text})

#     entities_res = extractor.extract_entities(documents)
#     res = []

#     for er in entities_res:
#         groupby = defaultdict(list)
#         for ent in er["entities"]:
#             ent_prop = ENT_PROP_MAP[ent["label"]]
#             groupby[ent_prop].append(ent["name"])
#         record = {"recordId": er["id"], "data": groupby}
#         res.append(record)

#     return {"values": res}    

# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...)):
#     contents = await file.read()
#     blob = base64.b64decode(contents)
#     with open(os.path.join(UPLOAD_FOLDER, file.filename), 'wb') as outfile:
#         outfile.write(blob)
#     return {"filename": file.filename}

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

