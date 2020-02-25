from urllib.request import urlopen
from bs4 import BeautifulSoup
import spacy
from spacy import displacy
from collections import Counter
import dateparser
f=open("confList1.csv",'w')
#Parse page
link="temp1"
#html = urlopen(link)
with open(link,'r') as g:
    html = g.read()
bs = BeautifulSoup(html, "html.parser")
pagelines = bs.find_all(['p'])
print(bs.getText)
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
                    confTime["month"]=dobj.month
            except:
                pass
    return confTime
import csv

writer = csv.writer(f, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
#Look at each line <p> of html file
confName=""
for line in pagelines[5:]:
    #Check if there is a new conference name in bold
    boldText=line.find_all(['b'])
    if len(boldText)!=0:
        confName=boldText[0].getText()
    doc=nlp(line.getText())
    confTime=getDate(doc)
    if 'year' in confTime:

        writer.writerow([confName, confTime['year'], confTime])
    else:
        writer.writerow([confName, 'N/A', confTime])
