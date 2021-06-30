#!/usr/bin/python3
import os
from bs4 import BeautifulSoup
from collections import Counter
import matplotlib.pyplot as plt

cwd = os.getcwd()
folder = cwd + "/DataSets/OpenDataUitspraken"
delimiter = "; "
subjects_all = []

def plot (subject_dict) :
    plt.xlabel("Rechtsgebieden")
    plt.ylabel("Arresten")
    plt.xticks(rotation=90)
    plt.bar(subject_dict.keys(), subject_dict.values())
    plt.show() # Print bar plot

def main () :
    for file in os.listdir(folder) :
        subjects = []
        xmlFile = open(folder + '/' + file, encoding="utf8")
        xml = BeautifulSoup(xmlFile, features="xml")
        xmlFile.close()
        for i in xml.find_all('dcterms:subject') :
            if (delimiter in i.getText()) :
                x = i.getText().split(delimiter)
                for j in x :
                    subjects.append(j)
            else :
                subjects.append(i.getText())
        for i in set(subjects) :
            subjects_all.append(i)
    subject_list = Counter(subjects_all).most_common() # Maak van list een list of tuples met frequency count
    subject_dict = dict(subject_list)
    var = input("\nTo also print the frequencies in terminal type 'yes': ")
    if (var == 'yes') :
        print(subject_dict) # Print frequencies of court decisions per area of law
    plot(subject_dict)

main()
