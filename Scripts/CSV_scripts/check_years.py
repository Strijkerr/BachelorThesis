#!/usr/bin/python3
from csv import reader
import os
from collections import Counter

def main () :
    file = os.getcwd() + "/CSV/Excluded.csv"
    
    total_count = 0
    years = []
    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip field header
        for row in csv_reader : 
            total_count+=1
            year = row[0].split('_')[3]
            if (int(year) < 2019) :
                years.append('<= 2018')
            else :
                years.append(year)
                
    print("Total: ",total_count)      
    print("Years: ",Counter(years).most_common())

main()
