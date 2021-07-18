#!/usr/bin/python3
from csv import reader
import sys
from collections import Counter

def main () :
    file = sys.argv[1]
    total_count = 0
    empty_count = 0
    else_count = 0
    anchors = []
    anchors2 = []
    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        for row in csv_reader :
            total_count+=1
            anchor = row[2]
            anchors.append(anchor)
            if (anchor == "") :
                empty_count+=1
            elif (" " not in anchor and "\t" not in anchor and "ECLI" not in anchor and ":" not in anchor) :
                if (anchor != "conclusie") :
                    if not (anchor[0].isupper()) :
                        if not (anchor.isdigit()) :
                            anchors2.append(anchor)
                            else_count+=1
    print("Total anchor texts: ",total_count)
    print("Anchor texts without capital that are not numbers: ",else_count)
    print("Empty anchor text: ",empty_count)
    print('\nTop 100 most common anchor texts that are words without capital, nor numbers : ',Counter(anchors2).most_common(100))
    print('\nTop 100 most common anchor texts: ',Counter(anchors).most_common(100))

main()
