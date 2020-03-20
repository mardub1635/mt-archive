from nameparser import HumanName
import sys
import re
line=sys.argv[1]
def namify(line):
    line=re.split(', | and|,and|,',line)
    line=list(filter(None,line))
    print(line)
    authors_list=[]
    for name in line:
        if 'KB' not in name:
            author = HumanName(name)
            author = author.last+", "+author.first+" "+author.middle
            author = author.strip()
            authors_list += [author]
    return " and ".join(authors_list)
print(namify(line))