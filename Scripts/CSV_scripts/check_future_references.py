#!/usr/bin/python3
from csv import reader
import os
from collections import Counter

def main () :
    file = os.getcwd() + "/CSV/Normal.csv"
    count = 0

    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        for row in csv_reader :
            count+=1
    print("Count: ",count)

main()