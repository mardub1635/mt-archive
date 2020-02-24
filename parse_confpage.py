from urllib.request import urlopen
from bs4 import BeautifulSoup
import spacy
from spacy import displacy
from collections import Counter

f=open("confList.csv",'w')
#Parse page
link="http://www.mt-archive.info/srch/conferences-1.htm"
html = urlopen(link)
bs = BeautifulSoup(html, "html.parser")
pagelines = bs.find_all(['p'])

#NLP treatment
nlp = spacy.load("en_core_web_sm")



#Look at each line of html file
confName=""
for line in pagelines[5:]:
    #Check if there is a new conference name in bold
    boldText=line.find_all(['b'])
    if len(boldText)!=0:
        confName=boldText[0].getText()
    doc=nlp(line.getText())
    print(dir(doc.ents))
    for X in doc.ents:
        if X.label_=='DATE':
            print(X)
            f.write(confName+";"+X.text)
