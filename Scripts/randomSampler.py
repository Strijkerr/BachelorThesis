#!/usr/bin/python3
import csv
import os
import random

file = os.getcwd() + "/CSV/SelfRef.csv"
samples = 5

with open(file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    rows = [row for row in csv_reader] 
    randomRows = random.sample(rows,samples)
    for row in randomRows : 
        print("ECLI: " + row[0])
        print("Ref_ECLI: " + row[1])
        print("Citation: '" + row[2] + "'")
        print("Paragraph: '" + row[3] + "'" + '\n')