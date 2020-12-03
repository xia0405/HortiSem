# way to upload pdf file: endpoint
# way to save the pdf file
# way to convert pdf to proper input text
# function to NER model
# show the results

import os
import re
import shutil
import csv
import tika
tika.initVM()
from tika import parser

import spacy

from typing import Optional
from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi import Request
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# from ml import nlp

# from spacy.language import Language
# # Language.factories["RegexMatcher"] = lambda nlp, **cfg: RegexMatcher(nlp, **cfg)
# Language.factories['entity_ruler_BOD_patterns'] = lambda nlp, **cfg: RegexMatcher(nlp,r"BBCH(\s?\d+)\s?(\/|\-|(bis)?)\s?(\d+)?","BBCH_Stadium")
# Language.factories['entity_ruler_patterns'] = lambda nlp, **cfg: RegexMatcher(nlp,r"\d{1,2}\.\d{1,2}\.\d{2,4}","Zeit")


app = FastAPI(
    title="{{HortiSem.Named_Entity_Recognition}}",
    version="1.0",
    description="{{HortiSem.project_short_description}}"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


UPLOAD_FOLDER = r"M:\Projekt\HortiSem\static\upload_folder"

# ML model
# nlp = spacy.load("M:/Projekt/HortiSem/tmp_model_v2")

# rule model using statistics
nlp = spacy.load("M:/Projekt/HortiSem/hybrid_model")
# ALLOWED_EXTENTIONS = {'pdf'}

def pdf_converter(pdf_path):
    # Read pdf and convert to plain text
    pdf_contents = parser.from_file(pdf_path)
    # clear text
    cleared_doc = re.sub(r'(\n{1,})|(\f)','',pdf_contents["content"])  
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
    
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

