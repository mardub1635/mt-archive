# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""

This module contains all the common functions regularly used on the extraction task.


Author: Marie Dubremetz

"""

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
    """(String, String)->None
    
    given $url, opens its webpage to crawl its content and write it to the local file with
    name $file_name.

    Example:
    >>>save_page('http://www.mt-archive.info/00/AMTA-2002-TOC.htm', '2002.amta')
    None
    >>>ls .
    2002.amta
    """
    response = urllib.request.urlopen(url)
    web_content = response.read()
    with open(file_name, 'wb') as f:
        print("writing to "+file_name)
        f.write(web_content)
        print("done")


def get_url(code_conf,conference_page=None):
    """(String)->String
    
    given the name of a conference ($code_conf) returns the URL of this conference as a string.

    NOTE:
    This module opens the file ConferenceList.csv and gets the row where the conference that
    has the file name of the conference code. It also prints a warning if the conference is a PDF, 
    and returns the URL.
    
    Example:
    >>>get_url('2002.amta')
   'http://www.mt-archive.info/00/AMTA-2002-TOC.htm',
    """
    code_tab="../ConferenceList.csv"
    if conference_page==2:
        code_tab="../ConferenceList2.csv"
    df = pd.read_csv(code_tab, delimiter=',')
    row = df.loc[df['file_name'] == code_conf]
    conf_type = row.Type
    print(conf_type)
    if conf_type.item() == 'PDF':
        print("WARNING: PDF")
    else:
        print("Geting URL")
    return row.URL.item()


def unspace(text):
    """
    (String)->String
    given $text returns a copy without any useless white space characters.

    Example:
    >>>' Conference\nin machine translation:\xa0\xa0\xa0\xa0 a very difficult         problem. "
    'Conference in machine translation: a very difficult problem.
    """
    text = text.replace(u'\xa0', u' ').replace("\n", " ").replace("\r", " ")
    text = re.sub(' +', ' ', text)
    text = text.strip()
    text = text.strip("–")
    text = text.strip()
    return text

def has_pdf(p,i_link=0):
    """
    (bs4.element.Tag, int)->String
    Given  beautifulsoup element $p returns the target of the first anchor in $p. 
    If none is found returns None. Change i_link to other integer than 0 if you do not want to return the first link.

    NOTE:
    This module is typically used on each <p> tags on the html page and serves to 
    recognise and extract PDF and presentation of talks.

    Example:
    >>> <p>MT for business <i>John Doe</i>[<a href="Doe-2002.pdf">PDF</a>]</p>
    'Doe-2002.pdf'
    """
    if p.find_all(['a']):
        links = p.find_all(['a'])
        try:
            return links[i_link]['href']
        except:
            return None
    return None


def get_title(p):
    if p.find_all(['a']):
        links = p.find_all(['a'])
        t = unspace(links[0].get_text())  # .decompose()#.contents[0]
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

    line = remove_digit(line).replace("…", "").strip().strip(".").replace(":","").strip(';')
    line = line.strip("-").strip(".")
    line = unspace(line)
    
    line = re.split(', and|,and|, | and|,|&',line)
    line = list(filter(None, line))  # remove empty
    authors_list = []
    for author in line:
        author = author.strip()
        authors_list.append(author)
        
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
        italics=p.find_all('i')
        italic_text=""
        for it in italics:
            italic_text+=it.text+" "
            
        return unspace(italic_text)


def remove_parenthesised(text, exclude=None):
    if exclude == None:
        text = re.sub("\([^)]*\)", "", text)
        text = re.sub("\[[^]]*\]", "", text)
    if exclude == "(":
        text = re.sub("\[[^]]*\]", "", text)
    if exclude == "[":
        text = re.sub("\([^)]*\)", "", text)
    return text

def is_centered(p):
    try:

        if p['align']=='center':
            return unspace(p.text)
    except:
        return None
def has_bold(p):

    try:
        
        bolds=p.find_all('b')
        bold_text=""
        for b in bolds:
            bold_text+=b.text+" "
        return unspace(bold_text)
    except:
        return None

def finish_by_digit(p):
    if unspace(p.text[-1]).isdigit():
        return True


def has_pp(p):
    if "pp." in unspace(p.text):
        return True

def extract_pages(p):
    if type(p)!=str:
        text=p.text
    else:
        text=p
       
    pages=re.findall(r'(pp.d+-\d+|pp\d+|\d+-\d+|\d+)', text)[-1]
    
    return pages

def remove_page(text):
    pages=extract_pages(text)
    text=text.replace(pages,"")

    #remove_digit( unspace(text)).replace('pp.','')
    text=text.replace('pp.','').replace('p.','').replace(' . .','').replace('....','').replace('....','').strip('-').strip(' ... ').strip('…')
    text=unspace(text).strip(";").replace("… .","")
    return unspace(text)

def has_tag(p,tag):
    try:
        tags=p.find_all(tag)
        print(tags)
        tag_text=""
        for t in tags:
            tag_text+=t.text+" "
            
        return unspace(tag_text)
    except:
        return None
