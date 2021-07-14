#!/usr/bin/python3
from csv import reader
import csv
import os
from collections import Counter
from lxml import etree

def findReference(file,row,rows) :
    newRow = row.copy()
    parser = etree.parse(file)
    root = parser.getroot()
    return_value = 0
    judgment = root.find("{http://www.rechtspraak.nl/schema/rechtspraak-1.0}uitspraak") # One 'uitspraak' section in court decision
    if (judgment is None) :
        judgment = root.find("{http://www.rechtspraak.nl/schema/rechtspraak-1.0}conclusie") # One 'conclusie' section in court decision
    abstract = root.find("{http://www.rechtspraak.nl/schema/rechtspraak-1.0}inhoudsindicatie") # One abstract section in court decision

    if (abstract is not None) :
        for el in abstract.iter():
            if (el.text is not None) :
                if (row[2] in el.text) :
                    newRow.append(el.text)
                    rows.append(newRow)
                    return_value = 1
                    newRow = row.copy()
            if (el.tail is not None) :
                if (row[2] in el.tail) :
                    newRow.append(el.tail)
                    rows.append(newRow)
                    return_value = 1
                    newRow = row.copy()
    if (judgment is not None) :
        for el in judgment.iter():
            if (el.text is not None) :
                if (row[2] in el.text) :
                    newRow.append(el.text)
                    rows.append(newRow)
                    return_value = 1
                    newRow = row.copy()
            if (el.tail is not None) :
                if (row[2] in el.tail) :
                    newRow.append(el.tail)
                    rows.append(newRow)
                    return_value = 1
                    newRow = row.copy()
    return(return_value)

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
    anchor_text = "vitale"
    file = cwd + "/CSV/Total.csv"
    reference_csv = cwd + "/CSV/" + anchor_text + ".csv"
    reference_rows = []
    reference_found = 0
    reference_count = 0

    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        for row in csv_reader :
            count+=1
            xmlDecision = cwd + "/DataSets/OpenDataUitspraken/" + row[0].replace(":","_") + ".xml"
            if (row[2] == anchor_text) :
                reference_count+=1
                reference_found+=findReference(xmlDecision,row,reference_rows)
            
    print("Total references: ",reference_count,"\tReferences found: ",reference_found,"\tReferences to check: ",len(reference_rows))
    writeToCSV(reference_csv,reference_rows)

main()