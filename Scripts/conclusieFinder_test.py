#!/usr/bin/python3
from bs4 import BeautifulSoup
import os

cwd = os.getcwd()
folder = cwd + "/DataSets/OpenDataUitspraken"

total = 0
conclusieCount = 0
conclusieCount2 = 0
geenConclusie = 0
geenConclusie2 = 0
geenConclusie3 = 0

for file in os.listdir(folder) :
    total+=1
    xmlFile = open(folder + '/' + file, encoding="utf8")
    xml = BeautifulSoup(xmlFile, features="xml")
    xmlFile.close()
    try :
        if (xml.conclusie) :
            conclusieCount+=1
            if (xml.conclusie.getText()) :
                conclusieCount2+=1
            else :
                print("Error in file: " + file)
    except :
        geenConclusie+=1

print("Total files: ",total)
print("Files with conclusie: ",conclusieCount)
print("Files with conclusie2: ",conclusieCount2)
print("Files with no conclusion: ",geenConclusie)