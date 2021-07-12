#!/usr/bin/python3
from csv import reader
import csv
import os
from collections import Counter

def writeToCSV (csvFile,rows) :
    fields = ["ECLI","Ref_ECLI","Anchor text","Paragraph"]
    if not os.path.exists(csvFile) :
        with open(csvFile, 'w') as csvOpen: 
            csvWriter = csv.writer(csvOpen) 
            csvWriter.writerow(fields) 
            for row in rows :
                csvWriter.writerows([row])

def main () :
    count = 0
    file = os.getcwd() + "/CSV/Normal.csv"

    self = os.getcwd() + "/CSV/Self.csv"
    future = os.getcwd() + "/CSV/Future.csv"
    recent = os.getcwd() + "/CSV/Recent.csv"

    self_rows = []
    future_rows = []
    recent_rows = []

    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        for row in csv_reader :
            count+=1
            if (row[0] == row[1]) :
                self_rows.append(row)
            
            if (row[1].split(":")[3] > row[0].split(":")[3]) :
                future_rows.append(row)

            if (row[0].split(":")[3] == "2019") :
                if ("ECLI" not in row[2]) :
                    recent_rows.append(row)
                    print(row)
            
    print("Count: ",count)
    print("Self-references: ",len(self_rows))
    print("Future references: ",len(future_rows))
    print("Recent references: ",len(recent_rows))
    writeToCSV(self,self_rows)
    writeToCSV(future,future_rows)
    writeToCSV(recent,recent_rows)

main()