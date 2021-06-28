#!/usr/bin/python3
import time
from bs4 import BeautifulSoup
import os

folder = "/media/jonathan/SSD/lido/OpenDataUitspraken"
seconds = time.time()

total = 0
rdfCount = 0
abstractCount = 0
abstractCount2 = 0
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
            print(file)
    try :
        if (xml.uitspraak.getText()) :
            weluitspraak+=1
            try :
                if (xml.inhoudsindicatie.getText()) :
                    weluitspraakwelinhood+=1
            except :
                weluitspraakgeeninhoud+=1
    except :
        geenuitspraak+=1
        try :
            if (xml.inhoudsindicatie.getText()) :
                geenuitspraakwelinhoud+=1
        except :
            geenuitspraakgeeninhoud+=1


print("Total files: ",total)
print("RDF: ",rdfCount)
print("abstractCount: ",abstractCount)
print("abstractCount2: ",abstractCount2)
print("uitspraakcount: ",uitspraakCount)
print("weluitspraak: ",weluitspraak)
print("weluitspraakwelinhood: ",weluitspraakwelinhood)
print("weluitspraakgeeninhoud: ",weluitspraakgeeninhoud)
print("geenuitspraak: ",geenuitspraak)
print("geenuitspraakwelinhoud: ",geenuitspraakwelinhoud)
print("geenuitspraakgeeninhoud: ",geenuitspraakgeeninhoud)
print("Seconds:",time.time()-seconds)