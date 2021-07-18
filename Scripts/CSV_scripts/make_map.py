#!/usr/bin/python3
from csv import reader
import os
import shutil

def main () :
    count = 0
    anchor_text = "vitale"
    dedicated_csv = os.getcwd() + "/CSV/" + anchor_text + ".csv"
    if not os.path.exists(dedicated_csv) :
        print("CSV file: ",dedicated_csv," does not exist")
        exit()
    OpenDataUitspraken = os.getcwd() + "/DataSets/OpenDataUitspraken/"
    decicated_map = os.getcwd() + "/DataSets/" + anchor_text + '/' # For creating new map
    if not os.path.exists(decicated_map) :
        os.makedirs(decicated_map) # For creating new map
    with open(dedicated_csv, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        for row in csv_reader :
            count+=1
            filename = row[0].replace(':','_')+".xml"
            if not os.path.exists(decicated_map + filename) :
                shutil.copyfile(OpenDataUitspraken + filename,decicated_map + filename) # For creating new map
    print("Rows counted: ",count)

main()