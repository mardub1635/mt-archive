# -*- coding: utf-8 -*-
import urllib.parse
from urllib.parse import urljoin
import sys
import csv
from bs4 import BeautifulSoup
from nameparser import HumanName
import pandas as pd
import spacy
from nltk.tag import StanfordNERTagger
from nltk.parse import CoreNLPParser
# save webpage
FILE_NAME = sys.argv[0]
FILE_NAME = FILE_NAME.split("_")[1].replace(".py", "")
print(FILE_NAME)


def save_page(url, file_name): 
    """
    saves the content of the webpage into a local file
    """
    response = urllib.request.urlopen(url)
    web_content = response.read()
    with open(file_name, 'wb') as f:
        f.write(web_content)


def get_url(code_conf):
    """
    returns the URL associated to the code of the conference
    this conference URL is extracted from the ConferenceList.csv in 
    the upper folder
    >>eamt.1994
    http://www.mt-archive.info/90/AMTA-1994-TOC.htm
    """
    conf_table = pd.read_csv("../ConferenceList.csv", delimiter=',')
    line = conf_table.loc[conf_table['file_name'] == code_conf]
    conf_type = line.Type
    if conf_type.item() == 'PDF':
        print("WARNING: PDF")
    else:
        print("Geting URL")
    return line.URL.item()


URL = get_url(FILE_NAME)
#save_page(URL, FILE_NAME)# Uncomment the first time you run this script


def has_pdf(p):
    if p.find_all(['a']):
        links = p.find_all(['a'])
        return links[0]['href']
    return None


def get_title(p):
    if p.find_all(['p']):
        titles = p.find_all(['p'])
        print(titles)
        for t in titles:
            t = t.get_text()#.decompose()#.contents[0]
            t = t.replace("--", "").replace("\n", " ").replace("*", "").strip()
        return t
    return None

print("Loading spacy model...")
nlp = spacy.load("en_core_web_sm")
print("Spacy done")
def get_authors(p):
    if p.find_all(['i']):
        italic= p.find_all(['i'])[0]
        #print(italic)
        author = HumanName(italic.get_text())
        author = author.last+", "+author.first
    else:
        return None
    return author

with open(FILE_NAME, 'rb') as g:
    HTML = g.read()
bs = BeautifulSoup(HTML, "html.parser")
page_lines = bs.find_all(['p'])



with open(FILE_NAME+".tsv", 'w') as f:
    writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Title", "Authors", "Pdf", "Raw webtext"])
    for i in range(len(page_lines)):
        
        p=page_lines[i]
        raw_text = p.get_text().replace("\n", " ")
        authors = get_authors(p)
        pdf=None
        if not authors:
            continue       
        title = page_lines[i-1].get_text().replace("\n", " ")
        line = [title, authors, pdf, raw_text]
        writer.writerow(line)

"""
    for p in page_lines[5:]:
        raw_text = p.get_text().replace("\n", "")
        pdf = has_pdf(p)
        title = p.get_text()#get_title(p)
        if not title:
            continue
        if pdf:
            print(pdf)
            pdf = get_title(p)
            pdf = urljoin(URL,pdf)
        authors = get_authors(p)
        line = [title, authors, pdf, raw_text]
        writer.writerow(line)
        """
