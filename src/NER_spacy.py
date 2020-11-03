import spacy
import ujson
from pathlib import Path

# Load german language model
nlp = spacy.load("de_core_news_sm")

def read_jsonl(file_path):
    """Read a .jsonl file and yield its contents line by line.
    file_path (unicode / Path): The file path.
    YIELDS: The loaded JSON contents of each line.
    """
    with Path(file_path).open('r', encoding='utf8') as f:
        for line in f:
            try:  # hack to handle broken jsonl
                yield ujson.loads(line.strip())
            except ValueError:
                continue

jsonl_dir = 'C:/Users/xia.he/Desktop/HortiSem/data/test_texts.jsonl'

#text = "Pflanzenschutzdienst des Landes Brandenburg Pflanzenschutzinformation Hinweis Feldbau 26/2020 Müllroser Chaussee 54 15236 Frankfurt (Oder) Fax: 0331 275484282 Bearbeiter: Kupfer/Sommerfeldt Telefon:  033702 / 211 36-92/-91 Wünsdorf, den 11.05.2020 Pflanzenschutzmittelinformationen Erweiterung der bestehenden Zulassung zum Einsatz gegen Blattläuse für das Insektizid Teppeki (Zulassungsnr. 025691-00) mit dem W irkstoff Flonicamid Das Bundesamt für Verbraucherschutz und Lebensmittelsicherheit (BVL) hat die bestehende Zulassung des Pflanzenschutzmittel Teppeki um zusätzliche Anwendungen erweitert: Für alle Anwendungen von Teppeki gilt für Auflage NB6621: „Das Mittel wird als bienengefährlich, außer bei Anwendung nach dem Ende des täglichen Bienenfluges in dem zu behandelnden Bestand bis 23.00 Uhr, eingestuft (B2). Es darf außerhalb dieses Zeitraums nicht auf blühende oder von Bienen beflogene Pflanzen ausgebracht werden; dies gilt auch für Unkräuter. Bienenschutzverordnung vom 22.  Juli 1992, BGBl.  I S.  1410, beachten.“ Zulassung für Notfallsituationen im Pflanzenschutz im Winterraps Beizmittel gegen Auflauferkrankungen: Vibrance OSR (Wirkstoffe Fludioxonil, Metalaxyl-M und Sedaxane) Das Inverkehrbringen und die Verwendung o.g. genannten Pflanzenschutzmittel werden gemäß Artikel 53 der Verordnung (EG) Nr. 1107/2009 des Europäischen Parlaments und des Rates vom 21. Oktober 2009 über das Inverkehrbringen von Pflanzenschutzmitteln und zur Aufhebung der Richtlinien 79/117/EWG und 91/414/EWG des Rates (ABl. L 309 vom 24. November 2009, S. 1), i. V. m. § 29 Abs. 1 Nr. 1 des Gesetzes zum Schutz der Kulturpflanzen (Pflanzenschutzgesetz – PflSchG) vom 6. Februar 2012 (BGBl. I S. 148, 1281), zuletzt geändert durch Artikel 4 Absatz 84 des Gesetzes vom 18. Juli 2016 (BGBl. I S. 1666), wie folgt zugelassen: Die Zulassung wird für die Zeit vom 1. Juni 2020 bis zum 28. September 2020 für 120 Tage erteilt. Die zugelassene Menge wird auf 3.750 Liter begrenzt. Alle Anwendungsbestimmungen (z.B. NT699-1) sowie die Bestimmungen zum Gesundheitsschutz sind strikt einzuhalten. Ohne Zustimmung ist die Weitergabe an Dritte –auszugsweise oder im Original- nicht gestattet. Seite 1 von 2 Anwendungsnr.SchadorganismusKulturAnwendungs-zeitpunktAnwendungs-häufigkeit025691-00/10-002Blattläuse als  VirusvektorenWintergersteBBCH 11-25 (Herbst-Winter)025691-00/10-001BlattläuseGetreide (Gerste, Hafer, Roggen, Triticale, Weizen)BBCH 39-77140 g/ha1 x pro Jahr/KulturAnwendunggegen Auflauferkrankungen in Winterraps (Ackerbau)vor der Saat, BBCH 00max. 1 xSaatgutbehandlung25 ml/Einheit) Saatgut) eine Einheit  Saatgut entsprichteiner Saatgutmenge von 1.000.000 Korn)17,5 ml/ha, entsprechend 700.000 Korn/haWartezeitFEinsatzAufwand"

for text in read_jsonl(jsonl_dir):
    doc = nlp(text['text'])
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_) 



