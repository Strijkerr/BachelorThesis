#!/usr/bin/python3
import os
import re
import matplotlib.pyplot as plt
from collections import Counter

# main
def main () :
    folder = os.getcwd() + "/DataSets/OpenDataUitspraken"
    years = []
    left = 0
    right = 0
    for file in os.listdir(folder) : # Put the year from every filename in the folder into a list
        years.append(file.split('_')[3])
    defaultStart = int(min(years))
    defaultEnd = int(max(years))
    start, end = setRange(defaultStart,defaultEnd)
    if not (start == defaultStart and end == defaultEnd) :
        temp_years = []
        for i in years :
            year = int(i)
            if (year >= start and year <= end) :
                temp_years.append(i)
            elif (year < start) :
                left+=1
            else :
                right+=1
        years = temp_years
    printStats(years,start,end,left,right)
    years = showOutsideRange(years,start,end,left,right,defaultStart,defaultEnd)
    plot(years)

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

def showOutsideRange (years,start,end,left,right,defaultStart,defaultEnd) :
    if (left != 0) :
        leftRange = str(defaultStart) + '-' + str(start-1)
        var = input("To show years left of range like '" + leftRange + "' in plot, type 'yes': ")
        if (var == 'yes') :
            for i in range(left) :
                years.append(leftRange)
    if (right != 0) :
        rightRange = str(end+1) + '-' + str(defaultEnd)
        var = input("To show years right of range like '" + rightRange + "' in plot, type 'yes': ")
        if (var == 'yes') :
            for i in range(right) :
                years.append(rightRange)
    return(years)

# Print bar plot
def plot (years) :
    years.sort() # Sort years ascending
    plt.xlabel("Year")
    plt.ylabel("Court decisions")
    plt.xticks(rotation=90)
    years_set = set(years)
    years_bins = len(years_set) # Get unique year numbers
    plt.hist(years, bins = years_bins)
    plt.show()

# Print court decisions left and right of the requested range
def printStats (years,start,end,left,right) :
    print("Result:\n---------")
    if (left > 0) :
        print("Court decisions not counted to the left of",start,":",left) # Court decisions left of given range
    print("Court decisions from",start,"to",end,":",len(years)) # Court decisions in given range
    if (right > 0) :
        print("Court decisions not counted to the right of",end,":",right) # Court decisions to the right of given range
    var = input("\nTo also print frequencies per year type 'yes': ")
    if (var == 'yes') :
        print(Counter(years))

main()