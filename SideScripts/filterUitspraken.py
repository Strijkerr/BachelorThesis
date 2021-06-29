#!/usr/bin/python3
import os
import xml.etree.ElementTree as ET
count = 0

cwd = os.getcwd()
folder = cwd + "/DataSets/OpenDataUitspraken"

for file in os.listdir(folder) :
    tree = ET.parse(folder + '/' + file)
    root = tree.getroot()
    if not (root.find('{http://www.rechtspraak.nl/schema/rechtspraak-1.0}uitspraak')
    or root.find('{http://www.rechtspraak.nl/schema/rechtspraak-1.0}inhoudsindicatie')) :
        os.remove(folder + '/' + file)
    else :
        count+=1
print("Files left: ",count)