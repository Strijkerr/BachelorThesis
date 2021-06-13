#!/usr/bin/python3
import csv
import os
import random

folder = os.getcwd()
file = folder + "/CSV/SelfRef.csv"

with open(file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    rows = [row for row in csv_reader] 
    randomRows = random.sample(rows,5)
    for row in randomRows :
        print("ECLI: " + row[0])
        print("Ref_ECLI: " + row[1])
        print("Citation: '" + row[2] + "'")
        print("Paragraph: '" + row[3] + "'")
        print('\n')