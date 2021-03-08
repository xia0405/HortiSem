"""add a custom pipeline component to improve the accuracy."""
import spacy
from spacy.language import Language
from spacy.tokens import Span
import re

nlp = spacy.load(r"M:\Projekt\HortiSem\Spacy3\rule_based_matching\ml_rule_model")

@Language.component("add_regex_match")
def add_regex_entities(doc):   
    new_ents = []

    # label_z = "Zeit"
    # regex_expression_z = r"\d{1,2}\.\d{1,2}\.\d{2,4}"
    # for match in re.finditer(regex_expression_z, doc.text):  # find match in text
    #     start, end = match.span()  # get the matched token indices
    #     entity = Span(doc, start, end, label=label_z)
    #     new_ents.append(entity)
    #     # doc.ents += (entity,)
        
    label_b = "BBCH_Stadium"
    regex_expression_b = r"BBCH(\s?\d+)\s?(\/|\-|(bis)?)\s?(\d+)?"
    for match in re.finditer(regex_expression_b, doc.text):  # find match in text
        start, end = match.span()  # get the matched token indices
        entity = Span(doc, start, end, label=label_b)
        new_ents.append(entity)

    # doc.ents = list(doc.ents) + spans
    doc.ents = new_ents
    return doc

# Add the component after the NER
nlp.add_pipe("add_regex_match", after="ner")

# nlp.to_disk("./ml_rule_regex_model")

doc = nlp("BBCH 15, Fliegen, Flugbrand . Brandenburg, in Berlin, Schnecken, BBCH 13-48, BBCH 3 bis 34")

print([(ent.text, ent.label_) for ent in doc.ents])

