from urllib.request import urlopen
from bs4 import BeautifulSoup
import spacy
from spacy import displacy
from collections import Counter
import dateparser
import re
from urllib.parse import urlparse
f=open("confList1.csv",'w')
#Parse page
link="temp1"
#html = urlopen(link)
with open(link,'r') as g:
    html = g.read()
bs = BeautifulSoup(html, "html.parser")
pagelines = bs.find_all(['p'])
#NLP treatment
nlp = spacy.load("en_core_web_sm")

def getDate(doc):
    confTime={}
    for X in doc.ents:
        if X.label_=='DATE':
            try:
                ddata=dateparser.date.DateDataParser().get_date_data(X.text)
                dtype=ddata['period']
                dobj=ddata['date_obj']
                if dtype=="year":
                    dobj=ddata['date_obj']
                    confTime["year"]=dobj.year
                if dtype=="day" and dobj:
                    confTime["day"]=dobj.day
                    confTime["month"]=dobj.strftime("%b")
            except:
                pass
    return confTime
import csv
def normaliseSpace(text):
    if type(text) is list:
        text=" ".join(text)

    text=re.sub('\s+'," ",text)
    text=text.strip()
    return text

def isTOC(a):
    a=a.lower()
    return "table" in a and "content" in a

def formatDate(d):
    return "{}/{}/{}".format(d.setdefault("year", " "), d.setdefault("month", " "), d.setdefault("day", " "))

writer = csv.writer(f, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
log=csv.writer(open("log.csv","w"), delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer.writerow(["Conference Title", "Year", "Time","has TOC?","Link"])
#Look at each line <p> of html file
confName=""

for line in pagelines[5:]:
    #Check if there is a new conference name in bold
    boldText=[b.getText() for b in line.find_all(['b'])]
    currName=normaliseSpace(boldText)
    links=line.find_all(['a'])
    toc = [ a for a in links if isTOC(a.getText())]
    tocURL=""
    hasTable="no"
    if toc:
        hasTable="yes"
        tocURL=urlparse(toc[0]['href']).path
    if currName:
        confName=currName

    doc=nlp(line.getText())
    confTime=getDate(doc)
    backupYear=re.findall("19\d\d|20|d\d",line.getText())
    if 'year' in confTime:
        writer.writerow([confName, confTime['year'], formatDate(confTime),hasTable,tocURL])
    elif backupYear:
        writer.writerow([confName, backupYear,formatDate(confTime),hasTable,tocURL])
    else:
        log.writerow([confName, "N/A", formatDate(confTime),hasTable,tocURL])
