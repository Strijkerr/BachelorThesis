#!/usr/bin/python3
import os
import matplotlib.pyplot as plt
from collections import Counter

court_codes = []
cwd = os.getcwd()
folder = cwd + "/DataSets/OpenDataUitspraken"

def alias (court_codes_dict) :
    court_codes_dict["District Courts"] = court_codes_dict.pop("RB")
    court_codes_dict["Courts of Appeal"] = court_codes_dict.pop("GH")
    court_codes_dict["'Kantongerechten'"] = court_codes_dict.pop("KT")
    court_codes_dict["Supreme Court"] = court_codes_dict.pop("HR")
    court_codes_dict["Council of State"] = court_codes_dict.pop("RVS")
    court_codes_dict["Central Court of Appeal"] = court_codes_dict.pop("CRVB")
    court_codes_dict["'College van Beroep \nvoor het bedrijfsleven'"] = court_codes_dict.pop("CBB")
    court_codes_dict["'Parket Hoge Raad'"] = court_codes_dict.pop("PHR")
    return court_codes_dict

def combine (court_codes_dict) :
    deleteList = []
    countRB = 0 # 'Rechtbanken'
    countGH = 0 # 'Gerechtshoven'
    countKT = 0 # 'Kantongerechten'
    countAntillen = 0 # 'Instanties Nederlandse Antillen'
    for i in court_codes_dict :
        if (i[:2] == 'RB') :
            countRB+=court_codes_dict[i]
            deleteList.append(i)
        elif (i[:2] == 'GH') :
            countGH+=court_codes_dict[i]
            deleteList.append(i)
        elif (i[:2] == 'KT') :
            countKT+=court_codes_dict[i]
            deleteList.append(i)
        elif (i[:4] != 'CRVB' and i[:3] != 'RVS' and i[:2] != 'HR' and i[:3] != 'PHR' and i[:3] != 'CBB') :
            countAntillen+=court_codes_dict[i]
            deleteList.append(i)
    for i in deleteList :
        del court_codes_dict[i]
    court_codes_dict["RB"] = countRB
    court_codes_dict["GH"] = countGH
    court_codes_dict["KT"] = countKT # Dissolved
    court_codes_dict["Judicial bodies of the \nNetherlands Antilles"] = countAntillen
    var = input("\nTo alias x axis type 'yes': ")
    if (var == 'yes') :
        court_codes_dict = alias(court_codes_dict)
    temp = Counter(court_codes_dict).most_common()
    return(dict(temp))

def plot (court_codes_dict,xAxis) :
    plt.xlabel(xAxis)
    plt.ylabel("Court decisions")
    plt.xticks(rotation=90)
    plt.bar(court_codes_dict.keys(), court_codes_dict.values())
    plt.show() # Print bar plot

def start () :
    xAxis = "Court code"
    for file in os.listdir(folder) : # Loop door elke file in de folder en stop de gerechtscode uit de titel in een list
        court_codes.append(file.split('_')[2])
    temp = Counter(court_codes).most_common() # Make from list a list of tuples with frequency count
    court_codes_dict = dict(temp) # Make it a dict so it is plotable
    var = input("\nTo combine all 'RB', 'GH', 'KT' and 'Antillen' court decisions in their respective class together type 'yes': ")
    if (var == 'yes') :
        court_codes_dict = combine(court_codes_dict)
        xAxis = "Courts"
    var = input("\nTo also print the frequencies in terminal type 'yes': ")
    if (var == 'yes') :
        print(court_codes_dict) # Print frequencies of court decisions per court
    plot(court_codes_dict,xAxis)
start()