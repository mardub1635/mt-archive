# -*- coding: utf-8 -*-
"""

This script is an example of how to generate a tsv file from an mt-archive conference page.
NOTE: 
-Make sure the conferenceList.csv file is present in the parent folder
-The name of the script is important, make sure to have the code of the conference between a '_' and the '.py'
 extension for instance: parse_2002.amta.py
-Make sure the common.py file is present in the same or the parent folder.

Author: Marie Dubremetz

"""
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
#save_page(URL, FILE_NAME)  # Uncomment the first time you run this script

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
            print("New track name:", track)
            track = is_subtitle(p)
            writer.writerow([track])

            continue

        raw_text = unspace(p.get_text())
        pdf = None

        if has_pdf(p) and "presentation" not in p.text:
            pdf = has_pdf(p)
            pdf = urljoin(URL, pdf)
            #print(pdf)
        title=get_title(p)
        presentation = None
        if "presentation" in p.text:
            presentation = has_pdf(p)
            presentation = urljoin(URL, presentation)
        title_authors=p.get_text().split('–')
        if not pdf:
            try:
                title=title_authors.split[0]
        
            except:
                pass
        authors=has_italic(p)
        if not authors:
            try:
                authors=title_authors[1].split('[')[0]

                
            except:
                pass
        if authors:    
            authors=namify(authors)
        if not authors and not title and not pdf:
            continue
        line = [title, authors, pdf,presentation, track, raw_text]
        print(line)
        writer.writerow(line)
