import spacy
import re
from spacy import displacy

# ML model
# nlp = spacy.load("M:/Projekt/HortiSem/tmp_model_v2")

# ML model with rules based
nlp = spacy.load("C:/Users/xia.he/Project/Projekt/HortiSem/src/Spacy3/rule_based_matching/ml_rule_model")

def predict(text, nlp_model):
    text = re.sub(r'(\n{2,})|(\f)','',text)  
    doc = nlp_model(text)
    html = displacy.render(doc,style="ent", options=options)    
    ents = []
    for ent in doc.ents:
        ents.append({"entity":ent.text, "label":ent.label_})    
    return {"ents":ents,"html":html}

