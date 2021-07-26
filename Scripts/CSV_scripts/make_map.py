#!/usr/bin/python3
from csv import reader
import os
import shutil
import sys

def main () : # Can be used to make map with all ECLIs that refer to anchor text case. One can then visualize the characteristics of the map with visualization tools (e.g. areas of law distribution of vitale case)
    count = 0
    anchor_text = sys.argv[1]
    dedicated_csv = os.getcwd() + "/CSV/" + anchor_text + ".csv"
    if not os.path.exists(dedicated_csv) :
        print("CSV file: ",dedicated_csv," does not exist")
        exit()
    OpenDataUitspraken = os.getcwd() + "/DataSets/OpenDataUitspraken/"
    decicated_map = os.getcwd() + "/DataSets/" + anchor_text + '/'
    if not os.path.exists(decicated_map) :
        os.makedirs(decicated_map) # For creating new map
    with open(dedicated_csv, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        for row in csv_reader :
            count+=1
            filename = row[0].replace(':','_')+".xml"
            if not os.path.exists(decicated_map + filename) :
                shutil.copyfile(OpenDataUitspraken + filename,decicated_map + filename) # Copy to map
    print("Rows counted: ",count)

main()