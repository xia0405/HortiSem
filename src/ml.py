import spacy
from spacy.lang.de import German
from spacy.pipeline import EntityRuler
from spacy.matcher import PhraseMatcher
from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy.language import Language

from pathlib import Path
import jsonlines
import re


nlp = spacy.load("M:/Projekt/HortiSem/tmp_model_v2")
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


# pattern_bbch = [{'TEXT':{"REGEX":"BBCH(\s?\d+)\s?(\/|\-|(bis)?)\s?(\d+)?"}}] 
# matcher = Matcher(nlp.vocab, validate=True)
# matcher.add("BBCH_Stadium", None, pattern_bbch)

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

# entity_matcher = EntityMatcher(nlp, pattern_bbch, f"{f.stem}")
# #     nlp.add_pipe(entity_matcher, name=f"entity_matcher_{f.stem}",after="ner")

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


# class RegexMatcher(object):
#     # name = "entity_matcher"

#     def __init__(self, nlp, regex_expression, label):
#         self.nlp = nlp
#         self.regex_expression = regex_expression
#         self.label = label

#     def __call__(self, doc):
#         spans = []
#         for match in re.finditer(self.regex_expression, doc.text):  # find match in text
#             start, end = match.span()  # get the matched token indices
#             span = doc.char_span(start, end, label=self.label)
#             spans.append(span)
#         doc.ents = list(doc.ents) + spans  
#         return doc
    
#     def to_disk(self, path, **kwargs):       
#         # This will receive the directory path + /my_component        
#         data_path = path / "data.json"        
#         with data_path.open("w", encoding="utf8") as f:            
#             f.write(json.dumps(self.data))

#     def from_disk(self, path, **cfg):        
#          # This will receive the directory path + /my_component        
#         data_path = path / "data.json"        
#         with data_path.open("r", encoding="utf8") as f:            
#             self.data = json.loads(f)        
#         return self

# nlp.add_pipe(RegexMatcher(nlp,regex_expression=r"BBCH(\s?\d+)\s?(\/|\-|(bis)?)\s?(\d+)?",label="BBCH_Stadium"), name="regex_bbch",before="ner")
# nlp.add_pipe(RegexMatcher(nlp,regex_expression=r"\d{1,2}\.\d{1,2}\.\d{2,4}",label="Zeit"), name="regex_zeit",before="ner")

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


print(nlp.pipe_names)

# # def add_regex_entities(doc):
#     regex_expression = r"BBCH(\s?\d+)\s?(\/|\-|(bis)?)\s?(\d+)?"
#     spans = []
#     for match in re.finditer(regex_expression, doc.text):  # find match in text
#         start, end = match.span()  # get the matched token indices
#         span = doc.char_span(start, end, label="BBCH_Stadium")
#         spans.append(span)
#     doc.ents = list(doc.ents) + spans
#     return doc

doc = nlp("BBCH 15, Fliegen, Flugbrand . Brandenburg, in Berlin, Schnecken, 12.1.2025")

print([(ent.text, ent.label_) for ent in doc.ents])

nlp.to_disk(base_path/"hybrid_model")
# nlp.to_disk(base_path/"rule_model")