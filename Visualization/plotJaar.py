#!/usr/bin/python3
import sys
import os
import matplotlib.pyplot as plt
from collections import Counter

years = []
folder = sys.argv[1]

for file in os.listdir(folder) : # Loop door elke file in de folder en stop het jaartal uit de titel in een list
    years.append(file.split('_')[3])

# temp = Counter(years).most_common()
# temp2 = dict(temp)
# print(temp2) # Om frequencies te printen
# count = 0
# for i in temp2 :
#     if (int(i) <= 1993) :
#         count+=temp2[i]
# print(count) # Om alle arresten tot en met 1993 te tellen
years.sort() # sorteer lijst met jaartallen oplopend
plt.xlabel("Jaar")
plt.ylabel("Arresten per jaar")
plt.xticks(rotation=90)
years_set = set(years)
years_bins = len(years_set) # Krijg aantal unieke jaartallen
plt.hist(years, bins = years_bins)
plt.show()