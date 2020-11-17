from spacy.lang.de import German
from spacy.pipeline import EntityRuler
from spacy.matcher import PhraseMatcher
from spacy.matcher import Matcher
from spacy.tokens import Span

from pathlib import Path
import ujson
import jsonlines

nlp = German()
ruler = EntityRuler(nlp)
# nlp = spacy.load("M:/Projekt/HortiSem/tmp_model_v1")



# define the file path and output file path
base_path = Path("M:\Projekt\HortiSem")
patterns_path = base_path/'data/dictionary_jsonl'

# get a list of all the files with .dsv
all_pattern_files = patterns_path.glob('*.jsonl')

for f in all_pattern_files:
    with jsonlines.open(f) as reader:
        ruler.add_patterns(reader)
        nlp.add_pipe(ruler,name=f"entity_ruler_{f.stem}")


print(nlp.pipeline)

# class EntityMatcher(object):
#     # name = "entity_matcher"

#     def __init__(self, nlp, terms, label):
#         patterns = [nlp.make_doc(text) for text in terms]
#         self.matcher = PhraseMatcher(nlp.vocab)
#         self.matcher.add(label, None, *patterns)

#     def __call__(self, doc):
#         matches = self.matcher(doc)
#         for match_id, start, end in matches:
#             span = Span(doc, start, end, label=match_id)
#             doc.ents = list(doc.ents) + [span]
#         return doc


# # for f in all_csv_files:   
# #     reader = csv.DictReader(open(f, 'r'),delimiter=',')   
# #     pattern_terms=[row["KODETEXT"] for row in  reader]
# #     entity_matcher = EntityMatcher(nlp, pattern_terms, f"{f.stem}")
# #     nlp.add_pipe(entity_matcher, name=f"entity_matcher_{f.stem}",after="ner")

# def add_regex_entities(doc):
#     label_z = "Zeit"
#     regex_expression_z = r"\d{1,2}\.\d{1,2}\.\d{2,4}"
    
#     spans = []
#     for match in re.finditer(regex_expression_z, doc.text):  # find match in text
#         start, end = match.span()  # get the matched token indices
#         span = doc.char_span(start, end, label=label_z)
#         spans.append(span)
        
#     label_b = "BBCH_Stadium"
#     regex_expression_b = r"BBCH(\s?\d+)\s?(\/|\-|(bis)?)\s?(\d+)?"
#     for match in re.finditer(regex_expression_b, doc.text):  # find match in text
#         start, end = match.span()  # get the matched token indices
#         span = doc.char_span(start, end, label=label_b)
#         spans.append(span)

#     doc.ents = list(doc.ents) + spans
#     return doc

# nlp.add_pipe(add_regex_entities, name="add_regex_match",before="ner")

# # def add_regex_entities(doc):
#     regex_expression = r"BBCH(\s?\d+)\s?(\/|\-|(bis)?)\s?(\d+)?"
#     spans = []
#     for match in re.finditer(regex_expression, doc.text):  # find match in text
#         start, end = match.span()  # get the matched token indices
#         span = doc.char_span(start, end, label="BBCH_Stadium")
#         spans.append(span)
#     doc.ents = list(doc.ents) + spans
#     return doc

doc = nlp("BBCH 15, Fliegen, Flugbrand . Brandenburg, in Berlin, Schnecken")

print([(ent.text, ent.label_) for ent in doc.ents])

nlp.to_disk(base_path/"rule_model")