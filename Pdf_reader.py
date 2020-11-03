import spacy
import slate3k as slate
# from pathlib import Path
# import json
import re
# import ujson
import warnings
warnings.filterwarnings("ignore")

pdf_file = "M:\\Projekt\\HortiSem\\upload_folder\\WD-Gemuese_1.pdf"

nlp = spacy.load("M:/Projekt/HortiSem/tmp_model")


def pdf_converter(pdf_path):
    # Read pdf and convert to plain text
    with open(pdf_path, 'rb') as f:
        texts = slate.PDF(f)
    # join multiple pages into one text
    doc = ' '.join(texts)
    # clear text
    cleared_doc = re.sub(r'(\n{1,})|(\f)','',doc)  
    return cleared_doc



# # Read pdf and convert to plain text
# with open(pdf_file, 'rb') as f:
#     texts = slate.PDF(f)
# # join multiple pages into one text
# doc = ' '.join(texts)
# # clear text
# cleared_doc = re.sub(r'(\n{1,})|(\n\f)','',doc)  
# doc = nlp(cleared_doc)

def predict(text, nlp_model):
    doc = nlp_model(text)
    ents = []
    for ent in doc.ents:
        ents.append({"entity":ent.text, "label":ent.label_})
    return ents
    


ents = []
for ent in doc.ents:
    ents.append({"entity":ent.text, "label":ent.label_})

print(ents)
print(len(ents))