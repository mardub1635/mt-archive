# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import urllib.parse
import spacy
import csv
import sys
from bs4 import BeautifulSoup
from nameparser import HumanName
import pandas as pd
from urllib.parse import urljoin

# save webpage
FILE_NAME = sys.argv[0]
FILE_NAME = FILE_NAME.split("_")[1].replace(".py","")
print(FILE_NAME)


def save_page(url,file_name):
    
    response = urllib.request.urlopen(url)
    web_content = response.read()
    with open(file_name, 'wb') as f:
        f.write(web_content)



def get_url(code_conf):
    df=pd.read_csv("../ConferenceList.csv",delimiter=',')
    line=df.loc[df['file_name'] == code_conf]
    conf_type=line.Type
    if conf_type.item()=='PDF':
        print("WARNING: PDF")
    else:
        print("Geting URL")
    return line.URL.item()

URL = get_url(FILE_NAME)
#URL_PATH = "http://www.mt-archive.info/90/"
save_page(URL,FILE_NAME)#Uncomment the first time you run this script
def hasPDF(p):
    if p.find_all(['a']):
        links = p.find_all(['a'])
        return(links[0]['href'])
    return None

def getTitle(p):
    #print(p.find_all(['b'])[0].get_text())
    if p.find_all(['b']):
        titles=p.find_all(['b'])
        for t in titles:
            t=t.get_text()#.decompose()#.contents[0]
            t=t.replace("--","").replace("\n"," ").replace("*","").strip()
        return t
    return None

def getAuthors(p):
    doc=nlp(p.getText())
    authors=[]
    for tok in doc.ents:
        if tok.label_=='PERSON':
            if 'KB' not in tok.text:
                author=HumanName(tok.text)
                author=author.last+", "+author.first
                authors+=[author]
    #print(authors)
    return " and ".join(authors)

with open(FILE_NAME,'rb') as g:
    html = g.read()
bs = BeautifulSoup(html, "html.parser")
pagelines = bs.find_all(['p'])


nlp = spacy.load("en_core_web_sm")
with open("test"+".tsv",'w') as f:
    writer = csv.writer(f, delimiter='\t',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Title","Authors","Pdf","Raw webtext"])
with open(FILE_NAME+".tsv",'w') as f:
    writer = csv.writer(f, delimiter='\t',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Title","Authors","Pdf","Raw webtext"])

    for p in pagelines[5:]:
        raw_text = p.get_text().replace("\n","")
        pdf=hasPDF(p)
        title=getTitle(p)
        if not title:
            continue
        if pdf:
            print(pdf)
            pdf=urljoin(URL,pdf)
        #else:
            #continue
        authors=getAuthors(p)
        line=[title,authors,pdf,raw_text]
        writer.writerow(line) 
        #print(line)