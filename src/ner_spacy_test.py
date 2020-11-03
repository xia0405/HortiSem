import spacy
import slate3k as slate
from pathlib import Path
import json
import re
import ujson
import warnings
warnings.filterwarnings("ignore")

pdf_file = 'M:\Projekt\HortiSem\data\wm\BW\Jahr2015\Gemuesebau\WD-Gemuese_4.pdf'

nlp = spacy.load("M:/Projekt/HortiSem/tmp_model")

# Read pdf and convert to plain text
with open(pdf_file, 'rb') as f:
    texts = slate.PDF(f)
# join multiple pages into one text
doc = ' '.join(texts)

doc = nlp(doc)
#doc = nlp("Die Lauchminierfliege ist nach wie vor aktiv und verbreitet sich jetzt auch über größere Entfernungen.Wo noch nicht geschehen, sollten Winterzwiebel, Steckzwiebeln, junger Lauchetc. behandelt werden.")
# "Außer Raupen und Schnecken können in seltenen Fällen an weichen Kohlarten auch Ohrwürmer Lochfraß verursachen. Die Tiere findet man oft nur nach längerem Suchen im Schutz der Herzblätter. Dort erinnert der Schaden durch die ausgefransten Löcher und den krümeligen, dunklen Kot an Kohlmotten. Es fehlt aber das für Kohlmotten typische feine Gespinst.""

for ent in doc.ents:
    print(ent.text, ent.label_)