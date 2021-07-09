#!/usr/bin/python3
from csv import reader
import os
import re

def printStats(total_count,exclamantionMark_count,else_count,normalECLI_count) :
    print('\n')
    print("Total count: ",total_count)
    print("Exclamantion Mark count: ",exclamantionMark_count)
    print("Normal ECLI count: ",normalECLI_count)
    print("Else count: ",else_count)

def main () :
    file = os.getcwd() + "/CSV/Total.csv"
    
    total_count = 0
    exclamationMark_count = 0
    normalECLI_count = 0
    else_count = 0

    with open(file, 'r') as total :
        csv_reader = reader(total)
        for row in csv_reader :
            total_count+=1
            if (row[1] == '!') :
                exclamationMark_count+=1
            elif (re.match(r"ECLI:..:.+:\d\d\d\d:.+",row[1])) : # ECLI, court code = 2 characters, court code 1-7 characters, year = 4 digits, unique number = max 25 characters
                normalECLI_count+=1
                print(row[1])
            else :
                else_count+=1
                
    printStats(total_count,exclamationMark_count,else_count,normalECLI_count)

main()
