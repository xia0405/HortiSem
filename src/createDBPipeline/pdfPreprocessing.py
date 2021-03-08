# library to read the text from pdfs
import tika
tika.initVM()
from tika import parser
import os
import re

import warnings
warnings.filterwarnings("ignore")

def pdf_converter(pdf_path):
    # Read pdf and convert to plain text
    pdf_contents = parser.from_file(pdf_path)
    # clean text
    text = re.sub(r'(\n{1,})|(\f)','',pdf_contents["content"])  
    pdfName= os.path.basename(pdf_path)
    return text, pdfName

