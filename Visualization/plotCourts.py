#!/usr/bin/python3
import os
import re
import matplotlib.pyplot as plt
from collections import Counter

# Combines all 'RB*' cases together and combines all 'GH*' cases together.
def combine (court_codes_dict) :
    deleteList = []
    countRB = 0 # 'Rechtbanken'
    countGH = 0 # 'Gerechtshoven'
    for i in court_codes_dict :
        if (i[:2] == 'RB') :
            countRB+=court_codes_dict[i]
            deleteList.append(i)
        elif (i[:2] == 'GH') :
            countGH+=court_codes_dict[i]
            deleteList.append(i)
    for i in deleteList :
        del court_codes_dict[i]
    court_codes_dict["RB"] = countRB
    court_codes_dict["GH"] = countGH
    temp = Counter(court_codes_dict).most_common()
    return(dict(temp))

# Print bar plot
def plot (court_codes_dict) :
    plt.xlabel("Court code")
    plt.ylabel("Court decisions")
    plt.xticks(rotation=90)
    plt.bar(court_codes_dict.keys(), court_codes_dict.values())
    plt.show()

# Main
def main () :
    folder = os.getcwd() + "/DataSets/OpenDataUitspraken"
    court_codes = []
    
    years = []
    for file in os.listdir(folder) : 
        years.append(file.split('_')[3])
    defaultStart = int(min(years)) # To get default starting year
    defaultEnd = int(max(years)) # To get default ending year
    start, end = setRange(defaultStart,defaultEnd)

    for file in os.listdir(folder) : # Put all court codes from the files in the dataset in one list
        year = int(file.split('_')[3])
        if (year >= start and year <= end) :
            court_codes.append(file.split('_')[2])
    temp = Counter(court_codes).most_common() # Make from list a list of tuples with frequency count
    court_codes_dict = dict(temp) # Make it a dict so it is plotable
    var = input("\nTo combine all decisions from the 'District Courts' and 'Courts of Appeal' respectively, type 'yes': ")
    if (var == 'yes') :
        court_codes_dict = combine(court_codes_dict)
    var = input("\nTo also print the frequencies in terminal type 'yes': ")
    if (var == 'yes') :
        print(court_codes_dict) # Print frequencies of court decisions per court
    plot(court_codes_dict)

# Sets range e.g., 1911-2021. Checks if format is correct etc.
def setRange (min, max) :
    print("Default range = " + str(min) + '-' + str(max))
    var = input("\nEnter range (e.g. 1995-2021): ")
    if (re.match(r"\d\d\d\d-\d\d\d\d",var)) :
        start = int(var.split('-')[0])
        end = int(var.split('-')[1])
        if (start <= end) :
            if (start >= min and end <= max) :
                return(start, end)
            else :
                print("Input invalid, using default range")
                return(min, max)
        else :
            print("Start of range is larger than end of range, using default range")
            return(min, max)
    else :
        print("Input invalid, using default range")
        return(min, max)   
main()