#!/usr/bin/python3
from csv import reader
import csv
import os
from collections import Counter
from lxml import etree

def findReference(file,row,rows) :
    newRow = row
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
                    newRow = row
            if (el.tail is not None) :
                if (row[2] in el.tail) :
                    newRow.append(el.tail)
                    rows.append(newRow)
                    return_value = 1
                    newRow = row
    if (judgment is not None) :
        for el in judgment.iter():
            if (el.text is not None) :
                if (row[2] in el.text) :
                    newRow.append(el.text)
                    rows.append(newRow)
                    return_value = 1
                    newRow = row
            if (el.tail is not None) :
                if (row[2] in el.tail) :
                    newRow.append(el.tail)
                    rows.append(newRow)
                    return_value = 1
                    newRow = row
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
    self_count = 0
    future_count = 0
    recent_count = 0

    normal_found = 0

    vitale = cwd + "/CSV/Vitale.csv"
    vitale_rows = 0
    vitale_found = 0
    vitale_count = 0

    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        for row in csv_reader :
            count+=1
            xmlDecision = cwd + "/DataSets/OpenDataUitspraken/" + row[0].replace(":","_") + ".xml"
            #normal_found+=findReference(xmlDecision,row)
            if (row[0] == row[1]) :
                self_count+=1
                self_found+=findReference(xmlDecision,row,self_rows)
            if (row[1].split(":")[3] > row[0].split(":")[3]) :
                future_count+=1
                future_found+=findReference(xmlDecision,row,future_rows)
            if (row[0].split(":")[3] == "2019") :
                if ("ECLI" not in row[2]) :
                    recent_count+=1
                    recent_found+=findReference(xmlDecision,row,recent_rows)
            if (row[2] == "vitale") :
                vitale_count+=1
                print
                vitale_found+=findReference(xmlDecision,row,vitale_rows)
            
    print("Self-references: ",self_count,"\tFound: ",self_found,"\tReferences to check: ",len(self_rows))
    print("Future references: ",future_count,"\tFound: ",future_found,"\tReferences to check: ",len(future_rows))
    print("Recent references: ",recent_count,"\tFound: ",recent_found,"\tReferences to check: ",len(recent_rows))
    print("Vitale references: ",vitale_count,"\tFound: ",vitale_found,"\tReferences to check: ",len(vitale_rows))
    #print("Total references: ",count,"\tFound: ",normal_found)
    writeToCSV(self,self_rows)
    writeToCSV(future,future_rows)
    writeToCSV(recent,recent_rows)
    writeToCSV(vitale,vitale_rows)

main()