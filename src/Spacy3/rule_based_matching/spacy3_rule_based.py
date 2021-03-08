import spacy

import jsonlines
from pathlib import Path
import ujson
# read multiple files under one folder
from glob import glob 

nlp = spacy.load("M:/Projekt/HortiSem/Spacy3/ner_spacy3_hortisem/training/model-best")
ruler = nlp.add_pipe("entity_ruler")

# the path to the entity patterns
base_path = Path("M:\Projekt\HortiSem")
patterns_path = base_path/'data/entity_patterns'
all_pattern_files = patterns_path.glob('*.jsonl')

for f in all_pattern_files:
    new_ruler = ruler.from_disk(f)

nlp.to_disk("./ml_rule_model")

doc = nlp("BBCH 15, Fliegen, Flugbrand . Brandenburg, in Berlin, Schnecken, 12.1.2025")

print([(ent.text, ent.label_) for ent in doc.ents])

# for f in all_pattern_files:
#     with jsonlines.open(f) as reader:
#         ruler.add_patterns(reader)
#         nlp.add_pipe(ruler,name=f"entity_ruler_{f.stem}")