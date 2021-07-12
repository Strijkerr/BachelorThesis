#!/usr/bin/python3
from csv import reader
import os
from collections import Counter

def main () :
    file = os.getcwd() + "/CSV/Total.csv"
    empty_count = 0
    else_count = 0
    newLine_count = 0
    anchors = []
    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        for row in csv_reader :
            anchor = row[2]
            anchors.append(anchor)
            if (anchor == "") :
                empty_count+=1
            elif (anchor == "Cichowski") :
                print(row[0],row[1],row[2])
            else :
                else_count+=1
    print("Empty anchor text: ",empty_count)
    print("New line count: ",newLine_count)
    print("Else: ",else_count)
    print('Frequencies: ',Counter(anchors).most_common(100))

main()
