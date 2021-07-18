#!/usr/bin/python3
from csv import reader
import os
from collections import Counter

def main () :
    file = os.getcwd() + "/CSV/Total.csv"
    empty_count = 0
    else_count = 0
    anchors = []
    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        for row in csv_reader :
            anchor = row[2]
            anchors.append(anchor)
            if (anchor == "") :
                empty_count+=1
            # elif (" " not in anchor and "\t" not in anchor and "ECLI" not in anchor and ":" not in anchor) :
            #     if (anchor != "conclusie") :
            #         if not (anchor[0].isupper()) :
            #             if not (anchor.isdigit()) :
            #                 anchors.append(anchor)
            #                 print(row)
            #                 else_count+=1
    # print("Else: ",else_count)
    print("Empty anchor text: ",empty_count)
    print('Frequencies: ',Counter(anchors).most_common(100))

main()
