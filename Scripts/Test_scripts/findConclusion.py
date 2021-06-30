#!/usr/bin/python3
from bs4 import BeautifulSoup
import os

cwd = os.getcwd()
folder = cwd + "/DataSets/OpenDataUitspraken_full"

total = 0
conclusieCount = 0
conclusieCount2 = 0
geenConclusie = 0
geenConclusie2 = 0
geenConclusie3 = 0
geenConclusie4 = 0

for file in os.listdir(folder) :
    total+=1
    xmlFile = open(folder + '/' + file, encoding="utf8")
    xml = BeautifulSoup(xmlFile, features="xml")
    xmlFile.close()
    try :
        if (xml.conclusie) :
            conclusieCount+=1
            try :
                if (xml.conclusie.getText()) :
                    conclusieCount2+=1
                else :
                    geenConclusie4+=1
            except :
                geenConclusie3+=1
        else :
            geenConclusie2+=1
    except :
        geenConclusie+=1

print("Total files: ",total)
print("Files with conclusie: ",conclusieCount)
print("Files with conclusie2: ",conclusieCount2)
print("Files with no conclusion: ",geenConclusie)
print("Files with no conclusion2: ",geenConclusie2)
print("Files with no conclusion3: ",geenConclusie3)
print("Files with no conclusion4: ",geenConclusie4)