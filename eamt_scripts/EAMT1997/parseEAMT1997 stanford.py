# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import urllib.parse
import spacy
import csv
from bs4 import BeautifulSoup

# save webpage
FILE_NAME = "EAMT1997"
URL = 'http://www.mt-archive.info/90/EAMT-1997-TOC.htm'
URL_PATH = "http://www.mt-archive.info/90/"

def save_page(url,file_name):
    
    response = urllib.request.urlopen(url)
    web_content = response.read()
    with open(file_name, 'wb') as f:
        f.write(web_content)

#save_page(URL,FILE_NAME)#Uncomment the first time you run this script

def hasPDF(p):
    if p.find_all(['a']):
        links = p.find_all(['a'])
        return(links[0]['href'])
    return None

def getTitle(p):
    if p.find_all(['a']):
        links=p.find_all(['a'])
        t=links[0].get_text()#.decompose()#.contents[0]
        return t
    return None

def getAuthors(p):
    doc=nlp(p.getText())
    #print(doc)
    Author=""
    for tok in doc.ents:
        if tok.label_=='PERSON':
            if 'KB' not in tok.text:
                Author+=tok.text+" "
    #print(Author)
    return Author

with open(FILE_NAME,'rb') as g:
    html = g.read()
bs = BeautifulSoup(html, "html.parser")
pagelines = bs.find_all(['p'])


nlp = spacy.load("en_core_web_sm")

with open(FILE_NAME+".csv",'w') as f:
    writer = csv.writer(f, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Title","Authors","Pdf"])

    for p in pagelines[5:]:
        pdf=hasPDF(p)
        if pdf:
            print(pdf)
            pdf=URL_PATH + pdf
        else:
            continue
        title=getTitle(p)
        if not title:
            continue
        authors=getAuthors(p)
        #if not authors:
        #    continue
        line=[title,authors,pdf]
        writer.writerow(line) 
        print(line)
