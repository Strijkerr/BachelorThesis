#!/usr/bin/python3
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
    if (left != 0) :
        leftRange = str(defaultStart) + '-' + str(startingYear-1)
        var = input("To show years left of range like '" + leftRange + "' in plot, type 'yes': ")
        if (var == 'yes') :
            for i in range(left) :
                years.append(leftRange)
    if (right != 0) :
        rightRange = str(endingYear+1) + '-' + str(defaultEnd)
        var = input("To show years right of range like '" + rightRange + "' in plot, type 'yes': ")
        if (var == 'yes') :
            for i in range(right) :
                years.append(rightRange)
    plot(years)

def setRange (min, max) :
    print("Default range = " + str(min) + '-' + str(max))
    var = input("\nEnter range (e.g. 1995-2021): ")
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
            print("Start of range is larger than end of range, using default range")
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
    var = input("\nTo also print frequencies per year type 'yes': ")
    if (var == 'yes') :
        print(Counter(years))

start()