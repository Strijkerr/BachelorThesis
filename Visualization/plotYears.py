#!/usr/bin/python3
import os
import matplotlib.pyplot as plt
from collections import Counter

years = []
cwd = os.getcwd()
folder = cwd + "/DataSets/OpenDataUitspraken"

for file in os.listdir(folder) : # Loop door elke file in de folder en stop het jaartal uit de titel in een list
    years.append(file.split('_')[3])

def frequencies () :
    temp = Counter(years)
    # temp = Counter(years).most_common() # Sort most common
    temp2 = dict(temp)
    print(temp2[0] + ':' + temp2[-1])
    print(temp2) # Print frequencies of court decision per year
    count = 0
    for i in temp2 :
        if (int(i) <= 1993) :
            count+=temp2[i]
    print(count) # Court decisions, years 1911-1993

years.sort() # Sort years ascending
plt.xlabel("Year")
plt.ylabel("Court decisions")
plt.xticks(rotation=90)
years_set = set(years)
years_bins = len(years_set) # Get unique year numbers
plt.hist(years, bins = years_bins)
plt.show()

frequencies()