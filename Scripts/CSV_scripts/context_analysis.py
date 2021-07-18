#!/usr/bin/python3
from csv import reader
import os
import re
from collections import Counter

def main () :
    anchor_text = "vitale"
    file = os.getcwd() + "/CSV/" + anchor_text + ".csv"
    total_rows = 0
    exception_rows = 0
    wordList = []
    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        regex = re.compile(r'\b{}\b \b(\w+)\b'.format(anchor_text)) 
        for row in csv_reader :
            total_rows+=1
            if ("griffier" in row[3]  or "rechter" in row[3] or "voorzitter" in row[3]) : # if anchor_text = 'Cichowski'
                exception_rows+=1
            for i in regex.findall(row[3]) :
                wordList.append(i)
    print(Counter(wordList).most_common(10))
    print("Rows counted: ",total_rows)
    print("`Griffier', `rechter' or `voorzitter' in paragraph: ",exception_rows)

main()