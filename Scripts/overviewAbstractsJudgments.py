#!/usr/bin/python3
from bs4 import BeautifulSoup
import os

cwd = os.getcwd()
folder = cwd + "/DataSets/OpenDataUitspraken"

total = 0
rdfCount = 0
abstractCount = 0
abstractCount2 = 0
noabstract = 0
uitspraakCount = 0
weluitspraak = 0
weluitspraakwelinhood = 0
weluitspraakgeeninhoud = 0
geenuitspraak = 0
geenuitspraakwelinhoud = 0
geenuitspraakgeeninhoud = 0

for file in os.listdir(folder) :
    total+=1
    xmlFile = open(folder + '/' + file, encoding="utf8")
    xml = BeautifulSoup(xmlFile, features="xml")
    xmlFile.close()
    if (xml.RDF) :
        rdfCount+=1
    if (xml.uitspraak) :
        uitspraakCount+=1
    if (xml.inhoudsindicatie) :
        abstractCount+=1
        if (xml.inhoudsindicatie.getText()) :
            abstractCount2+=1
        else :
            print("Error in file: " + file)
    try :
        if (xml.uitspraak.getText()) :
            weluitspraak+=1
            try :
                if (xml.inhoudsindicatie.getText()) :
                    weluitspraakwelinhood+=1
                else :
                    weluitspraakgeeninhoud+=1 # For the "ECLI_NL_RBDHA_2016_2379.xml" exception
            except :
                weluitspraakgeeninhoud+=1
        else :
            geenuitspraak+=1 # No cases in dataset of 28/05/2021
    except :
        geenuitspraak+=1
        try :
            if (xml.inhoudsindicatie.getText()) :
                geenuitspraakwelinhoud+=1
            else :
                geenuitspraakgeeninhoud+=1 # No cases in dataset of 28/05/2021
        except :
            geenuitspraakgeeninhoud+=1

print("Total files: ",total)
print("Files with RDF: ",rdfCount)
print("Files with abstract: ",abstractCount)
print("Files with abstract *corrected: ",abstractCount2)
print("Files with judgment: ",uitspraakCount)
print("Files with judgment: ",weluitspraak)
print("Judgment and abstract: ",weluitspraakwelinhood)
print("Judgment, no abstract: ",weluitspraakgeeninhoud)
print("No judgment: ",geenuitspraak)
print("No judgment, abstract yes: ",geenuitspraakwelinhoud)
print("No judgment and no abstract: ",geenuitspraakgeeninhoud)