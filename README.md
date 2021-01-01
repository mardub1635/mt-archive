# Ingestion of the MT-archive website

- [Introduction](#Introduction)
- [Problem](#Problem)
- [Description](#Description)
- [Source](#Source)
- [Usage](#Usage)

## Introduction

Association for Computational Linguistics (ACL) is the biggest association gathering research groups and conference literature about NLP. One mission of ACL consists in providing a centralised database of all the conference/journal paper on the computational linguistics domain: [ACL anthology](https://www.aclweb.org/anthology/).

The goal of this project is to incorporate the data from an old archive website: [MT-archive.info](http://www.mt-archive.info/) into the ACL anthology.
    Mt-archive.info is an “Electronic repository and bibliography of articles, [...] in machine translation [...]”. It is one of the largest sources of free scientific literature used by the Machine Translation (MT) community.

## Problem
[This website](http://www.mt-archive.info/) based on the initiative of John Hutchins seems not to be curated any longer (last update was March 2017). Many of the entries registered in it are not accessible by other means. This archive relies on the maintenance of its sole author.

To remedy this we have extracted the data from inconsistent html/pdf files to consistent machine-readable TSV files. Those files are stored in this repository and are waiting to be transferred into the [ACL anthology](https://www.aclweb.org/anthology/).

To constitute the current repository we had to process:

- 202 proceedings of 25+ conferences and workshops extracted from HTML or PDF into TSV files
- 5172 contributions by 4700+ authors
- 19 PDFs of proceedings split into 100+ individual papers
- Over 60 years of archives with the oldest papers aged 68 years old

A more complete report of the work can be consulted here:

[Ingestion of the MT archive website](https://docs.google.com/document/d/1yJRzxHQ_r316HRdC8z9IoeML_zVmAV08T2KsqXk3az4/edit?usp=sharing)




## Description

This repository contains data stored as tsv files collected from the mt-archive.info.
We based the collect on those two conference lists:
- [http://www.mt-archive.info/srch/conferences-1.htm](http://www.mt-archive.info/srch/conferences-1.htm)
- [http://www.mt-archive.info/srch/conferences-2.htm](http://www.mt-archive.info/srch/conferences-2.htm)

For a more structured collect we represent these two conference lists in this spreadsheet:
[MT Archive Conference List](https://docs.google.com/spreadsheets/d/1fpxmdV_BPwR6BQHyU9VJQxXeSOmy4__5nQCHBEviyAw/edit?usp=sharing)
For each conference there is a URL that opens the page of a table of content. We  collect all the data from it in a structured way:  (i.e., Title of each paper - Authors - Link to the PDF)
And we store these data in a .tsv file named after the conference code.


## Source

In the current repository you will find:
* "data/" a folder containing subfolders named after conferences. Inside those folders you will find ".tsv" files named according to the code date.conference.tsv for instance data/bcs/1994.bcs.tsv
* "script/" a folder containing scripts that help transforming a webpage into a tsv file. Note that each web page is unique. Thus in my collect, I used as much scripts as pages (around 200!). For the sake of simplicity, I leave here only an example script "parse_2002.amta.py"+"common.py". You can find the other scripts in my [non-official repo](https://github.com/mardub1635/mt-archive-workdir/).
* "script/parse_2002.amta.py" an example of script to transform a table of content (TOC) page ([AMTA-2002 in this case](http://www.mt-archive.info/00/AMTA-2002-TOC.htm))
* "script/common.py" script listing functions used by "parse_2002.amta.py to parse the TOC
* "script/parse_confpage.py" a script to convert the list of conference into a .tsv
* "script/ingest_tsv.py" a script to transform the resulted .tsv files into a proper folder containing the downloaded pdf + the xml files necessary for the conference anthology.



## Usage

The most important documents are in data/.

Under "data/" each conference has a folder which is named after a code that is listed on the spreadsheet [MT Archive Conference List](https://docs.google.com/spreadsheets/d/1fpxmdV_BPwR6BQHyU9VJQxXeSOmy4__5nQCHBEviyAw/edit?usp=sharing) (see column B "Conference Code").

Inside each folder are the ".tsv" files. The names of those files are listed in [MT Archive Conference List](https://docs.google.com/spreadsheets/d/1fpxmdV_BPwR6BQHyU9VJQxXeSOmy4__5nQCHBEviyAw/edit?usp=sharing) (see column O "file_name").

Further instructions can be found on the official repo of the [ACL anthology](https://github.com/acl-org/acl-anthology).

+ Author's repository github: @mardub1635 
+ Archive and project manager github: @mjpost