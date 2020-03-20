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
from common import save_page, get_url, is_subtitle, has_pdf, namify, get_title, has_italic,unspace, remove_parenthesised
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
presentation=None
with open(FILE_NAME+".tsv", 'w') as f:
    writer = csv.writer(f, delimiter='\t', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Title", "Authors", "Pdf", "Presentation",
                     "Volume_Name", "Raw_webtext"])

    for i in range(len(page_lines)-2):
        j = 1
        p = page_lines[i]
        p1 = page_lines[i+1]

        if is_subtitle(p):
            vol = is_subtitle(p)
            #writer.writerow([vol])
            continue

        raw_text = p.get_text().replace("\n", " ")
        pdf = None
        if has_pdf(p) and "presentation" not in p.text:
            pdf = has_pdf(p)
            print(pdf)
            title = get_title(p)
            if has_pdf(p1) and "presentation" not in p1.text:
                title2 = get_title(p1)
                title = title+" "+title2

                p2 = page_lines[i+2]
                j = 2
                p1 = p2

        if not pdf:
            continue

        while len(p1.text.strip()) <= 3:
            p1 = page_lines[i+j]
            j = j+1
            

        pdf = urljoin(URL, pdf)
        authors= remove_parenthesised( p1.get_text())
        authors = namify(authors)
        title = unspace(title)
        line = [title, authors, pdf, presentation, vol, raw_text]
        writer.writerow(line)
