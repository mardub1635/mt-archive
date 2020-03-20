# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from common import save_page, get_url, is_subtitle, has_pdf, namify, get_title, has_italic,unspace
import re
import csv
import spacy
from urllib.parse import urljoin
from bs4 import BeautifulSoup


# save webpage

FILE_NAME = sys.argv[0]
FILE_NAME = FILE_NAME.split("_")[1].replace(".py", "")
print(FILE_NAME)
URL = get_url(FILE_NAME)
save_page(URL, FILE_NAME)  # Uncomment the first time you run this script

with open(FILE_NAME, 'rb') as g:
    html = g.read()
bs = BeautifulSoup(html, "html.parser")
page_lines = bs.find_all(['p'])


nlp = spacy.load("en_core_web_sm")
track = None
with open(FILE_NAME+".tsv", 'w') as f:
    writer = csv.writer(f, delimiter='\t', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Title", "Authors", "Pdf", "Presentation",
                     "Volume_Name", "Raw_webtext"])

    for p in page_lines:

        #get the track
        if is_subtitle(p):
            print("assigne", track)
            track = is_subtitle(p)
            writer.writerow([track])

            continue

        raw_text = unspace(p.get_text())
        pdf = None
        #Skip presention line
        if has_pdf(p) and "presentation" not in p.text:
            pdf = has_pdf(p)
            pdf = urljoin(URL, pdf)
            #print(pdf)

        presentation = None
        if "presentation" in p.text:
            presentation = has_pdf(p)
            presentation = urljoin(URL, presentation)
        try:
             title = re.split(":", p.get_text())[1]
             title= re.split("--", title)[0]
             title = namify(title)
        except:
            continue
        
        
        print(has_italic(p))
        if not has_italic(p):
            continue
        authors=has_italic(p)
        authors=namify(authors)
        #authors=re.split(":", p.get_text())[0]
        
        line = [title, authors, pdf,presentation, track, raw_text]
        writer.writerow(line)
