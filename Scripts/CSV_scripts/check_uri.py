#!/usr/bin/python3
from csv import reader
import os
import re
from collections import Counter

def printStats(normal_count,exclamationMark_count,multiple_count1,multiple_count2,empty_count,tilde_count,other_count,total_count,else_count) :
    print("Normal ECLI count: ",normal_count)
    print("Exclamantion Mark count: ",exclamationMark_count)
    print("Multiple ECLIS with `! infront of them: ",multiple_count1)
    print("Multiple ECLIS: ",multiple_count2)
    print("Empty target: ", empty_count)
    print("Tilde at end: ",tilde_count)
    print("Other count: ",other_count)
    print("Total count: ",total_count)
    print("Else count: ",else_count)

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
    file = os.getcwd() + "/CSV/Total.csv"
    courts = []

    normal_count = 0
    exclamationMark_count = 0
    multiple_count1 = 0
    multiple_count2 = 0
    empty_count = 0
    tilde_count = 0
    other_count = 0
    total_count = 0
    else_count = 0

    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader)
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
                print("Weird target: ",target)
                other_count+=1
            elif ("!" in target and "ECLI" in target) :
                multiple_count1+=1
            elif ('!' not in target and target.count("ECLI") > 1) :
                multiple_count2+=1
            elif (re.match(r"ECLI:..:.+:\d\d\d\d:.+",target)) : # ECLI, court code = 2 characters, court code 1-7 characters, year = 4 digits, unique number = max 25 characters
                normal_count+=1
            else :
                else_count+=1
    print("\nFrequencies of references vs. court", Counter(courts).most_common(),'\n')
    printStats(normal_count,exclamationMark_count,multiple_count1,multiple_count2,empty_count,tilde_count,other_count,total_count,else_count)

main()
