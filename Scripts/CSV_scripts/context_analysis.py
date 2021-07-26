#!/usr/bin/python3
from csv import reader
import os
import re
from collections import Counter
import sys

def main () :
    anchor_text = sys.argv[2]
    file = sys.argv[1] + "/CSV/" + anchor_text + ".csv"
    if not os.path.exists(file) :
        print("Run '3' first\n")
        return
    total_rows = 0
    exception_rows = 0
    wordList = []
    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        var = input("Take word preceding (p) or following (f) the anchor text: ")
        if (var == 'p') :
            regexString = r'\b(\w+)\b \b{}\b'
        else :
            regexString = r'\b{}\b \b(\w+)\b'
        regex = re.compile(regexString.format(anchor_text))
        for row in csv_reader :
            total_rows+=1
            if (anchor_text == "Cichowski") :
                if ("griffier" in row[3]  or "rechter" in row[3] or "voorzitter" in row[3]) : # If anchor_text = 'Cichowski' e.g.
                    exception_rows+=1
            for i in regex.findall(row[3]) :
                wordList.append(i)
    print(Counter(wordList).most_common(10))
    print("Rows counted: ",total_rows)
    if (anchor_text == "Cichowski") :
        print("`Griffier', `rechter' or `voorzitter' in paragraph: ",exception_rows)

main()