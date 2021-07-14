#!/usr/bin/python3
from csv import reader
import os
import csv

def writeToCSV (csvFile,row) :
    fields = ["ECLI","Ref_ECLI","Anchor text","Paragraph","TP"]
    if os.path.exists(csvFile) :
        with open(csvFile, 'a') as csvOpen: 
            csvWriter = csv.writer(csvOpen) 
            csvWriter.writerow(row)
    else :
        with open(csvFile, 'w') as csvOpen: 
            csvWriter = csv.writer(csvOpen) 
            csvWriter.writerow(fields) 
            csvWriter.writerow(row)
            

def main () :
    file = os.getcwd() + "/CSV/vitale.csv"
    file2 = os.getcwd() + "/CSV/vitale_new.csv"
    fp = 0
    tp = 0

    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        if os.path.exists(file2) :
            with open(file2, 'r') as total2 :
                csv_reader2 = reader(total2)
                next(csv_reader2) # Skip header
                for row2 in csv_reader2 :
                    if (row2[4] == '1') :
                        tp+=1
                    else :
                        fp+=1
                    next(csv_reader) # Make equal both CSV files
        for row in csv_reader :
            os.system('clear')
            print("Total: ",tp+fp)
            print("False positives: ",fp)     
            print("True positives: ",tp)
            print("\nAnchor text: ",row[2])
            print("\nSentence: ",row[3])
            answer = input("\nIs this a true positive, type: `y'\n\nAnswer: ")
            if (answer == 'y') :
                tp+=1
                row.append(1)
                writeToCSV(file2,row)
            else :
                fp+=1
                row.append(0)
                writeToCSV(file2,row)

main()