# way to upload pdf file: endpoint
# way to save the pdf file
# way to convert pdf to proper input text
# function to NER model
# show the results

import os
import re
import shutil
# import base64
import slate3k as slate
from ml import nlp

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

