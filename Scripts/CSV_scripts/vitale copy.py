#!/usr/bin/python3
from csv import reader
import os
import re
from collections import Counter
import shutil

def main () :
    anchor_text = "Haviltex"
    file = os.getcwd() + "/CSV/" + anchor_text + ".csv"
    folder = os.getcwd() + "/DataSets/OpenDataUitspraken/"
    #folder2 = os.getcwd() + "/DataSets/" + "Cichowski/" # For creating new map
    #os.makedirs(folder2) # For creating new map
    count = 0
    count1 = 0
    wordList = []
    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        regex = re.compile(r'\b(\w+)\b \b{}\b'.format(anchor_text)) 
        for row in csv_reader :
            count+=1
            # if ("griffier" in row[3]  or "rechter" in row[3] or "voorzitter" in row[3]) :
            #     count1+=1
            filename = row[0].replace(':','_')+".xml"
            #shutil.copyfile(folder + filename,folder2 + filename) # For creating new map
            for i in regex.findall(row[3]) :
                wordList.append(i)
    print(Counter(wordList).most_common(100))
    print(count)
    print(count1)

main()