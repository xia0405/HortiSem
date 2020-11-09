import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
import slate3k as slate
# from pathlib import Path
# import json
import re
# import ujson
import warnings
warnings.filterwarnings("ignore")

pdf_file = "M:\\Projekt\\HortiSem\\static\\upload_folder\\FB_19_18.pdf"


text = "Winterraps, BBCH 14-119, BBCH31, BBCH 2 - 7, es ist sehr trocken, Die Schädlinge treten vereinzelt."

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

weather_terms = ("trocken","nachtfrostfreie Perioden","milde Winter","milde Witterung","frühlingshaft warme Witterung","Unwetter")
auftreten_terms = ("vereinzelt","geringe Häufigkeit","sporadisch","örtlich","häufiger Befall")
resistenz_terms = ("Resistenzmanagement","Resistenzen gegenüber Wirkstoffen", "tendenzielle Zunahme von Resistenzen","FOP-Resistenz","Resistenzentwicklung","resistente Rassen","Wirkort-Resistenz")

regex_expression = r"BBCH(\s?\d+)(\s?\/?\-?\s?)(\d+)?"

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

def add_regex_entities(doc):
    #entities = []
    for match in re.finditer(regex_expression, doc.text):  # find match in text
        start, end = match.span()  # get the matched token indices
        span = doc.char_span(start, end, label="BBCH_Stadium")
        doc.ents = list(doc.ents) + [span]
    return doc

def predict(text, nlp_model):
    doc = nlp_model(text)
    ents = []
    for ent in doc.ents:
        ents.append({"entity":ent.text, "label":ent.label_})
    return ents


# load the model
nlp = spacy.load("M:/Projekt/HortiSem/tmp_model")
# Process the text    
# text = pdf_converter(pdf_file)
# add custom components
nlp.add_pipe(add_regex_entities, name="add_regex_match",before="ner")

entity_matcher_w = EntityMatcher(nlp, weather_terms, "Witterung")
entity_matcher_auf = EntityMatcher(nlp, auftreten_terms, "Auftreten")
entity_matcher_r = EntityMatcher(nlp, resistenz_terms, "Resistenz")

nlp.add_pipe(entity_matcher_w, name="entity_matcher_w",after="ner")

nlp.add_pipe(entity_matcher_auf,name="entity_matcher_auf", after="ner")

nlp.add_pipe(entity_matcher_r, name="entity_matcher_r",after="ner")

# Predict
ents = predict(text,nlp)

print(ents)
print(len(ents))

print(nlp.pipe_names)

