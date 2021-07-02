#!/usr/bin/python3
from bs4 import BeautifulSoup
import os

folder = os.getcwd() + "/DataSets/OpenDataUitspraken_full" # Veranderen later

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

for file in os.listdir(folder) :
    total+=1
    xmlFile = open(folder + '/' + file, encoding="utf8")
    xml = BeautifulSoup(xmlFile, features="xml")
    xmlFile.close()

    if (xml.uitspraak) :
        judgment+=1
        if (xml.inhoudsindicatie) :
            judgmentAbstract+=1
        else :
            judgmentNoAbstract+=1
    elif (xml.conclusie) :
        conclusion+=1
        if (xml.inhoudsindicatie) :
            conclusionAbstract+=1
        else :
            print(file) # Mag later ook weg
            conclusionNoAbstract+=1
    else :
        empty+=1
        if (xml.inhoudsindicatie) :
            emptyAbstract+=1
        else :
            emptyNoAbstract+=1

print("Total files: ",total) # N.B. RDF always present, cardinality = 1 in documentation
print("judgment: ",judgment)
print("judgmentAbstract: ",judgmentAbstract)
print("judgmentNoAbstract: ",judgmentNoAbstract)
print("conclusion: ",conclusion)
print("conclusionAbstract: ",conclusionAbstract)
print("conclusionNoAbstract: ",conclusionNoAbstract)
print("empty: ",empty)
print("errorAbstract: ",emptyAbstract)
print("errorNoAbstract: ",emptyNoAbstract)
print("Usable: ",(total-emptyNoAbstract))