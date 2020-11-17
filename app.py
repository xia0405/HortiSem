# way to upload pdf file: endpoint
# way to save the pdf file
# way to convert pdf to proper input text
# function to NER model
# show the results

import os
import re
import shutil
import csv
# import base64
import slate3k as slate

import spacy

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

# ML model
# nlp = spacy.load("M:/Projekt/HortiSem/tmp_model_v1")

# rule model using statistics
nlp = spacy.load("M:/Projekt/HortiSem/rule_model")
# ALLOWED_EXTENTIONS = {'pdf'}

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
    
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

