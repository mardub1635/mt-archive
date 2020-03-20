# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import urllib.parse
import sys
import csv
import spacy
from bs4 import BeautifulSoup
from nameparser import HumanName
import pandas as pd
from urllib.parse import urljoin
import re
# save webpage
FILE_NAME = sys.argv[0]
FILE_NAME = FILE_NAME.split("_")[1].replace(".py", "")
print(FILE_NAME)


def save_page(url, file_name):
    response = urllib.request.urlopen(url)
    web_content = response.read()
    with open(file_name, 'wb') as f:
        f.write(web_content)


def get_url(code_conf):
    df = pd.read_csv("../ConferenceList.csv", delimiter=',')
    row = df.loc[df['file_name'] == code_conf]
    conf_type = row.Type
    if conf_type.item() == 'PDF':
        print("WARNING: PDF")
    else:
        print("Geting URL")
    return row.URL.item()


URL = get_url(FILE_NAME)
save_page(URL, FILE_NAME)  # Uncomment the first time you run this script


def has_pdf(p):
    if p.find_all(['a']):
        links = p.find_all(['a'])
        return links[0]['href']
    return None


def get_title(p):
    if p.find_all(['a']):
        links = p.find_all(['a'])
        t = links[0].get_text().replace("\n", " ")  # .decompose()#.contents[0]
        return t
    return None

def except_auth(p):
    if "Maegaard" in p.get_text():
        print(p)
        return ['Maegaard, Bente']
    else:
        return []

def get_authors(p):
    doc = nlp(p.getText())
    authors_list = except_auth(p)
    for tok in doc.ents:
        if tok.label_ == 'PERSON':
            print(tok.text)
            if 'KB' not in tok.text:
                author = HumanName(tok.text)
                author = author.last+", "+author.first+" "+author.middle
                author = author.strip()
                authors_list += [author]
    return " and ".join(authors_list)

def namify(line):
    line=re.split(', | and|,and|,|&',line)
    line=list(filter(None,line))
    authors_list=[]
    for name in line:
        if 'KB' not in name:
            author = HumanName(name)
            author = author.last+", "+author.first+" "+author.middle
            author = author.strip()
            authors_list += [author]
    return " and ".join(authors_list)

def remove_digit(text):
    return "".join(filter(lambda x: not x.isdigit(), text))

def is_subtitle(p):
    if p.b:
        return [p.b.text.replace("\n", " ")]

with open(FILE_NAME, 'rb') as g:
    html = g.read()
bs = BeautifulSoup(html, "html.parser")
page_lines = bs.find_all(['p'])


nlp = spacy.load("en_core_web_sm")
with open(FILE_NAME+".tsv", 'w') as f:
    writer = csv.writer(f, delimiter='\t', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Title", "Authors", "Pdf", "Presentation", "Volume_Name", "Raw webtext"])
    presentation=None 
    vol=None 

    for i in range(len(page_lines)-1):
        p = page_lines[i]
        if is_subtitle(p):
            vol=is_subtitle(p)
            writer.writerow(vol)
            vol=vol[0]
            continue
        raw_text = p.get_text().replace("\n", " ")
        pdf = has_pdf(page_lines[i])
        if not pdf:
            continue
        pdf = urljoin(URL, pdf)
        authors = page_lines[i+1].get_text()
        authors = remove_digit(authors)
        authors = authors.strip().strip(".")
        authors = namify(authors)
        title = get_title(p)
        line = [title, authors, pdf,presentation,vol, raw_text]
        writer.writerow(line)
        
    for i in range(18):
        j=i+109
        p=page_lines[j]
        authors=get_authors(p)
        if not authors:
            continue
        title=get_title(p)#page_lines[j-1].get_text().replace("\n"," ")
        print(authors)
        line=[title,authors]
        writer.writerow(line)
