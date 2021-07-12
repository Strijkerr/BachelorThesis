#!/usr/bin/python3
from csv import reader
import csv
import os
from collections import Counter
from lxml import etree

def findReference(file,row,rows) :
    parser = etree.parse(file)
    root = parser.getroot()
    judgment = root.find("{http://www.rechtspraak.nl/schema/rechtspraak-1.0}uitspraak") # One 'uitspraak' section in court decision
    if (judgment is None) :
        judgment = root.find("{http://www.rechtspraak.nl/schema/rechtspraak-1.0}conclusie") # One 'conclusie' section in court decision
    abstract = root.find("{http://www.rechtspraak.nl/schema/rechtspraak-1.0}inhoudsindicatie") # One abstract section in court decision

    if (abstract is not None) :
        for el in abstract.iter():
            if (el.text is not None) :
                if (row[2] in el.text) :
                    row.append(el.text)
                    rows.append(row)
                    return(1)
            if (el.tail is not None) :
                if (row[2] in el.tail) :
                    row.append(el.tail)
                    rows.append(row)
                    return(1)
    if (judgment is not None) :
        for el in judgment.iter():
            if (el.text is not None) :
                if (row[2] in el.text) :
                    row.append(el.text)
                    rows.append(row)
                    return(1)
            if (el.tail is not None) :
                if (row[2] in el.tail) :
                    row.append(el.tail)
                    rows.append(row)
                    return(1) 
    return(0)

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
    cwd = os.getcwd()
    file = cwd + "/CSV/Normal.csv"

    self = cwd + "/CSV/Self.csv"
    future = cwd + "/CSV/Future.csv"
    recent = cwd + "/CSV/Recent.csv"

    self_rows = []
    future_rows = []
    recent_rows = []

    self_found = 0
    future_found = 0
    recent_found = 0

    normal_found = 0

    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        for row in csv_reader :
            count+=1
            xmlDecision = cwd + "/DataSets/OpenDataUitspraken/" + row[0].replace(":","_") + ".xml"
            #normal_found+=findReference(xmlDecision,row)
            if (row[0] == row[1]) :
                self_found+=findReference(xmlDecision,row,self_rows)
            if (row[1].split(":")[3] > row[0].split(":")[3]) :
                future_found+=findReference(xmlDecision,row,future_rows)
            if (row[0].split(":")[3] == "2019") :
                if ("ECLI" not in row[2]) :
                    recent_found+=findReference(xmlDecision,row,recent_rows)
            
    print("Self-references: ",len(self_rows),"\tFound: ",self_found)
    print("Future references: ",len(future_rows),"\tFound: ",future_found)
    print("Recent references: ",len(recent_rows),"\tFound: ",recent_found)
    #print("Total references: ",count,"\tFound: ",normal_found)
    writeToCSV(self,self_rows)
    writeToCSV(future,future_rows)
    writeToCSV(recent,recent_rows)

main()