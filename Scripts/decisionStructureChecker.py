#!/usr/bin/python3
from bs4 import BeautifulSoup
import os
import sys

folder = sys.argv[1]
total = 0
judgment = 0
judgmentAbstract = 0
judgmentNoAbstract = 0
conclusion = 0
conclusionAbstract = 0
conclusionNoAbstract = 0
empty = 0
emptyAbstract = 0
emptyNoAbstract = 0

phr = 0
phr2 = 0
phr3 = 0

for file in os.listdir(folder) :
    total+=1
    xmlFile = open(folder + '/' + file, encoding="utf8")
    xml = BeautifulSoup(xmlFile, features="xml")
    xmlFile.close()

    court = file.split('_')[2]
    if (court == 'PHR') :
        phr+=1
    if (xml.uitspraak) :
        judgment+=1
        if (xml.inhoudsindicatie) :
            judgmentAbstract+=1
        else :
            judgmentNoAbstract+=1
    elif (xml.conclusie) :
        if (court == 'PHR') :
            phr2+=1
        else :
            phr3+=1
            print(file)
        conclusion+=1
        if (xml.inhoudsindicatie) :
            conclusionAbstract+=1
        else :
            conclusionNoAbstract+=1
    else :
        empty+=1
        if (xml.inhoudsindicatie) :
            emptyAbstract+=1
        else :
            emptyNoAbstract+=1

print("Total files: ",total) # N.B. RDF always present, cardinality = 1 in documentation
print("Judgments: ",judgment)
print("Judgment + abstract: ",judgmentAbstract)
print("Judgment + no abstract: ",judgmentNoAbstract)
print("Advisory opinion: ",conclusion)
print("Advisory opinion + abstract: ",conclusionAbstract)
print("Advisory opinion + no abstract: ",conclusionNoAbstract)
print("Empty third section: ",empty)
print("Empty third section + abstract: ",emptyAbstract)
print("Empty third section + no abstract: ",emptyNoAbstract)
print("Usable: ",(total-emptyNoAbstract))

print("`PHR' cases: ", phr)
print("Advisory opinion by `PHR': ", phr2)
print("Advisory opinion not by `PHR': ", phr3)