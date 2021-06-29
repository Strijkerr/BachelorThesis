#!/usr/bin/python3
from enum import EnumMeta
import os
import re
import matplotlib.pyplot as plt
from collections import Counter

cwd = os.getcwd()
folder = cwd + "/DataSets/OpenDataUitspraken"

def start () :
    years = []
    left = 0
    right = 0
    for file in os.listdir(folder) : # Put the year from every filename in the folder into a list
        years.append(file.split('_')[3])
    defaultStart = int(min(years))
    defaultEnd = int(max(years))
    startingYear, endingYear = setRange(defaultStart,defaultEnd)
    if not (startingYear == defaultStart and endingYear == defaultEnd) :
        new_years = []
        for i in years :
            year = int(i)
            if (year >= startingYear and year <= endingYear) :
                new_years.append(i)
            elif (year < startingYear) :
                left+=1
            else :
                right+=1
        years = new_years
    printStats(years,startingYear,endingYear,left,right)
    plot(years)

def setRange (min, max) :
    print("Default range = " + str(min) + '-' + str(max))
    var = input("\nEnter range (e.g. 1993-2021): ")
    if (re.match(r"\d\d\d\d-\d\d\d\d",var)) :
        startingYear = int(var.split('-')[0])
        endingYear = int(var.split('-')[1])
        if (startingYear <= endingYear) :
            if (startingYear >= min and endingYear <= max) :
                return(startingYear, endingYear)
            else :
                print("Input invalid, using default range")
                return(min, max)
        else :
            print("Begin of range is larger than end of range, using default range")
            return(min, max)
    else :
        print("Input invalid, using default range")
        return(min, max)   

def plot (years) :
    years.sort() # Sort years ascending
    plt.xlabel("Year")
    plt.ylabel("Court decisions")
    plt.xticks(rotation=90)
    years_set = set(years)
    years_bins = len(years_set) # Get unique year numbers
    plt.hist(years, bins = years_bins)
    plt.show()

def printStats (years,startingYear,endingYear,left,right) :
    print("Result:\n---------")
    if (left > 0) :
        print("Court decisions not counted to the left of",startingYear,":",left) # Court decisions left of given range
    print("Court decisions from",startingYear,"to",endingYear,":",len(years)) # Court decisions in given range
    if (right > 0) :
        print("Court decisions not counted to the right of",endingYear,":",right) # Court decisions to the right of given range
    var = input("Print frequencies per year, type 'yes': ")
    if (var == 'yes') :
        print(Counter(years))

start()