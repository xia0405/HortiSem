import pymongo
import os
import re

import spacy
from spacy import displacy
from pdfPreprocessing import pdf_converter

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["hortisemDB"]
mycol = mydb["warndienstmeldung"]

# ML model with rules based
nlp = spacy.load("C:/Users/xia.he/Project/Projekt/HortiSem/src/Spacy3/rule_based_matching/ml_rule_model")

# define the paths of input pdf files and the desired output in jsonl format
# pdf_dir = r'C:\Users\xia.he\Project\Projekt\HortiSem\data\WD-Meldungen2019\BB\Jahr2020\Feldbau\FB_04_20.pdf'
pdf_dir = r"C:\Users\xia.he\Project\Projekt\HortiSem\data\WD-Meldungen2019\MV\Neubrandenburg\2017\F.05_2017 Rapsschädlinge Frühjahr.pdf"
# text_dir = r'M:\Projekt\HortiSem\data\input_text\Feldbau_MV_Rostock_2015.jsonl'

text, pdfName = pdf_converter(pdf_dir)

def predict(text, nlp_model):
    # text = re.sub(r'(\n{2,})|(\f)','',text)  
    doc = nlp_model(text)
    
    entities = {
        "Kultur": [], 
        "Erreger": [],
        "Mittel": [],
        "BBCH_Stadium": [],
        "Auftreten":[],
        "Witterung":[],
        "Ort": [],
        "Zeit": []
    }

    for ent in doc.ents:
        if ent.text in entities[ent.label_]:
            pass
        else:
            entities[ent.label_].append(ent.text)

    return entities
    

entities = predict(text,nlp)

fileDict = {
    "pdfName": pdfName,
    "pdfPath": pdf_dir,
    "state": entities["Ort"][0],
    "date": entities["Zeit"][0],
    "entities": entities
}

mycol.insert_one(fileDict)

# const entitySchema = {
#     pdfName: String,
#     pdfPath: String,
#     state: String,
#     datum: Date,
#     entities: {
#         kultur: [String],
#         erreger: [String],
#         mittel: [String],
#         bbchStadium: [String],
#         ort: [String],
#         zeit: [String]
#     }
# }

print(mydb.list_collection_names())



