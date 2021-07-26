#!/usr/bin/python3
from csv import reader
import csv
from collections import Counter
import os
import sys
csv.field_size_limit(sys.maxsize)

def courtType (court_code,court_list) :
    if (court_code.startswith("RB")) :
        court_list.append("RB")
    elif (court_code.startswith("GH")) :
        court_list.append("GH")
    else :
        court_list.append(court_code)

def main () :
    file = sys.argv[1] + "/CSV/Normal.csv"
    if not os.path.exists(file) :
        print("Run '2' first\n")
        return
    total_count = 0
    courts = []
    courts2 = []
    anchor = []
    count = 0
    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        for row in csv_reader :
            total_count+=1
            target = row[1].split(":")[2]
            courtType(target,courts2)
            if (int(row[0].split(":")[3]) < int(row[1].split(":")[3])) :
                count+=1
                anchor.append(row[2])
                courtType(target,courts)
    print("Total anchor texts: ",total_count)
    print(Counter(courts).most_common())
    print(Counter(anchor).most_common(10))
    print("Count2: ",count)
    print(Counter(courts2).most_common())
main()
