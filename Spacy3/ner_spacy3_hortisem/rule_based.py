import spacy
from spacy.language import Language

nlp = spacy.load("M:/Projekt/HortiSem/Spacy3/ner_spacy3_hortisem/training/model-best")

@Language.component("add_regex_macth")
def add_regex_entities(doc):
    label_z = "Zeit"
    regex_expression_z = r"\d{1,2}\.\d{1,2}\.\d{2,4}"
    
    spans = []
    for match in re.finditer(regex_expression_z, doc.text):  # find match in text
        start, end = match.span()  # get the matched token indices
        span = doc.char_span(start, end, label=label_z)
        spans.append(span)
        
    label_b = "BBCH_Stadium"
    regex_expression_b = r"BBCH(\s?\d+)\s?(\/|\-|(bis)?)\s?(\d+)?"
    for match in re.finditer(regex_expression_b, doc.text):  # find match in text
        start, end = match.span()  # get the matched token indices
        span = doc.char_span(start, end, label=label_b)
        spans.append(span)

    doc.ents = list(doc.ents) + spans
    return doc

nlp.add_pipe("add_regex_match",before="ner")


doc = nlp("BBCH 15, Fliegen, Flugbrand . Brandenburg, in Berlin, Schnecken, 12.1.2025")

print([(ent.text, ent.label_) for ent in doc.ents])

nlp.to_disk(base_path/"test_model")
