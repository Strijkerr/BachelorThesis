#!/usr/bin/python3
from bs4 import BeautifulSoup
import os
import sys

folder = sys.argv[1]
total = 0
court_decisions_references = 0
total_reference = 0
bwb_reference = 0
cvdr_reference = 0
ecli_reference = 0
eu_reference = 0
else_reference = 0

for c,file in enumerate(os.listdir(folder)) :
    total+=1
    xmlFile = open(folder + '/' + file, encoding="utf8")
    xml = BeautifulSoup(xmlFile, features="xml")
    xmlFile.close()

    referenceList = xml.find_all("dcterms:references")
    if (referenceList) :
        court_decisions_references+=1
        for i in referenceList :
            total_reference+=1
            attrsList = list(i.attrs)
            if (attrsList[1] == "ecli:resourceIdentifier") :
                ecli_reference+=1
            elif (attrsList[1] == "bwb:resourceIdentifier") :
                bwb_reference+=1
            elif (attrsList[1] == "cvdr:resourceIdentifier") :
                cvdr_reference+=1
            elif (attrsList[1] == "eu:resourceIdentifier") :
                eu_reference+=1
            else :
                else_reference+=1
                print(attrsList[1])

print("Total court decisions: ",total)
print("Court decisions with references: ", court_decisions_references)
print("Total of references found: ", total_reference)
print("ecli references: ",ecli_reference)
print("bwb references: ",bwb_reference)
print("cvdr references: ",cvdr_reference)
print("eu references: ", eu_reference)
print("Other type of references: ", else_reference)