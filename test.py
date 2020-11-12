from spacy.tokens import Span
import re
import spacy
from ml import nlp
import csv
from pathlib import Path

# regex_expression = r"BBCH(\s?\d+)(\s?\/?\-?\s?(bis\s)?)(\d+)?" #(\s?\d+)(\s?\/?\-?\s?(bis\s)?)(\d+)?
# def add_regex_entities(doc):
#     #entities = []
#     for match in re.finditer(regex_expression, doc.text):  # find match in text
#         start, end = match.span()  # get the matched token indices
#         span = doc.char_span(start, end, label="BBCH_Stadium")
#         doc.ents = list(doc.ents) + [span]
#     for ent in doc.ents:
#         print(ent.text,ent.label_)    
#     return doc

# text = " Vivendi 100 (1,2 l/ha) oder Effigo (0,35 l/ha) ab Vegetationsbeginn erfolgen. Bek ämpft werden u.a. Kamille und Hundskam ille, Kornblume, Kreuzkraut, Leguminosen und Disteln. Die beste W irkung wird im 2 – 4 Blattstadium der Unkr äuter erzielt. Aufwandmengenreduzierungen (z.B. 0,13 l/ha Lontrel 600, 110 g/ha Lontrel 720 SG, 0,8 l/ha Vivendi 100)"

# doc = nlp(text)
# add_regex_entities(doc)


# define the file path
base_path = Path("M:\Projekt\HortiSem\data")
with open( base_path/'dictionary_BOD_csv'/'Witterung.csv', 'r') as f:
    reader = csv.DictReader(f,delimiter=',')   
    weather_terms=[row["KODETEXT"] for row in  reader]
    print(weather_terms)