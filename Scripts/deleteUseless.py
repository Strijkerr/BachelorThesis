#!/usr/bin/python3
import os
import xml.etree.ElementTree as ET

def main () :
    count = 0
    folder = os.getcwd() + "/DataSets/OpenDataUitspraken"
    for file in os.listdir(folder) :
        tree = ET.parse(folder + '/' + file)
        root = tree.getroot()
        if not (root.find('{http://www.rechtspraak.nl/schema/rechtspraak-1.0}uitspraak')
        or root.find('{http://www.rechtspraak.nl/schema/rechtspraak-1.0}inhoudsindicatie')
        or root.find('{http://www.rechtspraak.nl/schema/rechtspraak-1.0}conclusie')) :
            os.remove(folder + '/' + file)
        else :
            count+=1
    print("Files left: ",count)

main ()