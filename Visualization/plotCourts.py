#!/usr/bin/python3
import sys
import os
import matplotlib.pyplot as plt
from collections import Counter

codes = []
cwd = os.getcwd()
folder = cwd + "/DataSets/OpenDataUitspraken"

for file in os.listdir(folder) : # Loop door elke file in de folder en stop de gerechtscode uit de titel in een list
    codes.append(file.split('_')[2])

temp = Counter(codes).most_common() # Maak van list een list of tuples met frequency count
codes_dict = dict(temp) # Maak er een dict van zodat data 'plot-able' is

# ------------------------ Totaal van arresten bij rechtbanken en gerechtshoven -------------------------
countRB = 0
countGH = 0
deleteList = []
for i in codes_dict :
    if (i[:2] == 'RB') :
        countRB+=codes_dict[i]
        deleteList.append(i)
    elif (i[:2] == 'GH') :
        countGH+=codes_dict[i]
        deleteList.append(i)
for i in deleteList :
    del codes_dict[i]
codes_dict['RB'] = countRB
codes_dict['GH'] = countGH
temp = Counter(codes_dict).most_common() # Maak van list een list of tuples met frequency count
codes_dict = dict(temp)
# -------------------------------------------------------------------------------------------------------

plt.xlabel("Gerechtscode")
plt.ylabel("Arresten")
plt.xticks(rotation=90)
plt.bar(codes_dict.keys(), codes_dict.values())
print(codes_dict) # Print dict met frequency arresten per gerechtscode
plt.show() # Print bar plot