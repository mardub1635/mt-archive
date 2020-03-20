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


def unspace(text):
    text = text.replace(u'\xa0', u' ').replace("\n", " ")
    text = re.sub(' +', ' ', text)
    return text


def get_title(p):
    if p.find_all(['a']):
        links = p.find_all(['a'])
        t = links[0].get_text().replace("\n", " ").replace(
            "  ", " ")  # .decompose()#.contents[0]
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
            if 'KB' not in tok.text:
                author = HumanName(tok.text)
                author = author.last+", "+author.first+" "+author.middle
                author = author.strip()
                authors_list += [author]
    return " and ".join(authors_list)


def remove_digit(text):
    return "".join(filter(lambda x: not x.isdigit(), text))


def namify(line):
    line = remove_digit(line).replace("…", "").strip().strip(".")
    line = line.strip()
    line = re.split(', | and|,and|,|&', line)
    line = list(filter(None, line))  # remove empty
    authors_list = []
    for name in line:
        if 'KB' not in name:
            author = HumanName(name)
            author = author.last+", "+author.first+" "+author.middle
            author = author.strip()
            authors_list += [author]
    return " and ".join(authors_list)


def is_subtitle(p):
    if p.b:

        subtitle = p.b.text.replace("\n", " ").strip()
        if len(subtitle) > 2:
            return p.b.text.replace("\n", " ")


def get_parenthesis(s):
    mo = re.search(r'\[(.*)\]', s)
    if mo:
        return mo.group(1)
    return ''


def has_italic(p):
    if p.i:
        return p.i


with open(FILE_NAME, 'rb') as g:
    html = g.read()
bs = BeautifulSoup(html, "html.parser")
page_lines = bs.find_all(['p'])


nlp = spacy.load("en_core_web_sm")
vol = None
with open(FILE_NAME+".tsv", 'w') as f:
    writer = csv.writer(f, delimiter='\t', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Title", "Authors", "Pdf", "Presentation",
                     "Volume_Name", "Raw_webtext"])

    vol = None
    presentation = None
    for i in range(len(page_lines)-2):
        j = 1
        p = page_lines[i]
        p1 = page_lines[i+1]

        if is_subtitle(p):
            vol = is_subtitle(p)
            writer.writerow([vol])
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
            
        print(p1.text)
        pdf = urljoin(URL, pdf)
        authors = namify(p1.get_text())
        title = unspace(title)
        line = [title, authors, pdf, presentation, vol, raw_text]
        writer.writerow(line)
