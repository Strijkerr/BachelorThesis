#!/usr/bin/python3
import os
import xml.etree.ElementTree as ET
import sys

def main () :
    files_left = 0
    files_deleted = 0
    folder = sys.argv[1]
    for file in os.listdir(folder) :
        tree = ET.parse(folder + '/' + file)
        root = tree.getroot()
        if not (root.find('{http://www.rechtspraak.nl/schema/rechtspraak-1.0}uitspraak')
        or root.find('{http://www.rechtspraak.nl/schema/rechtspraak-1.0}inhoudsindicatie')
        or root.find('{http://www.rechtspraak.nl/schema/rechtspraak-1.0}conclusie')) :
            os.remove(folder + '/' + file)
            files_deleted+=1
        else :
            files_left+=1
    print("Files deleted: ",files_deleted)
    print("Files left: ",files_left)

main () # Deze functie nog een keer testen na update