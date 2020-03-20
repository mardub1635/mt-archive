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

def unspace(text):
    text = text.replace(u'\xa0', u' ').replace("\n", " ")
    text = re.sub(' +', ' ', text)
    return text

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
            if 'KB' not in tok.text:
                author = HumanName(tok.text)
                author = author.last+", "+author.first+" "+author.middle
                author = author.strip()
                authors_list += [author]
    return " and ".join(authors_list)


def remove_digit(text):
    return "".join(filter(lambda x: not x.isdigit(), text))


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
    line = unspace(line)
    line = line=re.split(', and|,and|, | and|,|&',line)
    line = list(filter(None, line))  # remove empty

    authors_list = []
    print(line)
    for author in line:
        author = author.strip()
        authors_list.append(author)
        print(authors_list)
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
