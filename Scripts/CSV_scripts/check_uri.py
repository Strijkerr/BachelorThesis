#!/usr/bin/python3
from csv import reader
import csv
import os
import re
import sys
from collections import Counter

def writeToCSV (rows) :
    fields = ["ECLI","Ref_ECLI","Anchor text"]
    csvFile = os.getcwd() + "/CSV/Normal.csv"
    if not os.path.exists(csvFile) :
        with open(csvFile, 'w') as csvOpen: 
            csvWriter = csv.writer(csvOpen) 
            csvWriter.writerow(fields) 
            for row in rows :
                csvWriter.writerows([row])

def printStats(normal_count,exclamationMark_count,multiple_count1,multiple_count2,empty_count,tilde_count,other_count,total_count) :
    print("Total count: ",total_count)
    print("Regular ECLI in uri: ",normal_count)
    print("Exclamantion Mark count: ",exclamationMark_count)
    print("Multiple ECLIS with `! infront of them: ",multiple_count1)
    print("Multiple ECLIS: ",multiple_count2)
    print("Empty target: ", empty_count)
    print("Tilde at end: ",tilde_count)
    print("Other count: ",other_count)

def court_type (court) :
    if (court.startswith("RB")) :
        return("RB")
    elif (court.startswith("GH")) :
        return("GH")
    elif (court == "CRVB" or court == "RVS" or court == "HR" or court == "CBB" or court == "PHR") :
        return(court)
    else :
        return("Other")

def main () :
    file = sys.argv[1]
    courts = []

    printList = []
    new_rows = []
    normal_count = 0
    exclamationMark_count = 0
    multiple_count1 = 0
    multiple_count11 = 0
    multiple_count2 = 0
    empty_count = 0
    tilde_count = 0
    other_count = 0
    total_count = 0

    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        for row in csv_reader :
            total_count+=1
            court = row[0].split(':')[2]
            courts.append(court_type(court))
            target = row[1]
            if (target == '!') :
                exclamationMark_count+=1
            elif (target == "") :
                empty_count+=1
            elif (target.endswith("~")) :
                tilde_count+=1
            elif ("ECLI" not in target or "<" in target) :
                other_count+=1
            elif ("!" in target and "ECLI" in target) :
                years_here = []
                courts_here = []
                for i in row[1].split("!")[1:] :
                    years_here.append(i.split(":")[3])
                    courts_here.append(i.split(":")[2])
                if (len(set(years_here)) == 1 and len(set(courts_here)) == 1) : # All ECLIs and court types are the same within 1 uri
                    multiple_count11+=1
                printList.append(row[2])
                multiple_count1+=1
            elif ('!' not in target and target.count("ECLI") > 1) :
                printList.append(row[2])
                multiple_count2+=1
            elif (re.match(r"ECLI:..:.+:\d\d\d\d:.+",target)) : # ECLI, court code = 2 characters, court code 1-7 characters, year = 4 digits, unique number = max 25 characters
                new_rows.append(row)
                normal_count+=1

    printStats(normal_count,exclamationMark_count,multiple_count1,multiple_count2,empty_count,tilde_count,other_count,total_count)
    print("\nReference count vs. court", Counter(courts).most_common())
    print("\nSame year and court in the uri's of ambiguous references",multiple_count11)
    writeToCSV(new_rows)
    print("\nTop 100 most common anchor texts for ambiguous references: ",Counter(printList).most_common(100))

main()
