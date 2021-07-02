#!/usr/bin/python3
import os
from bs4 import BeautifulSoup
from collections import Counter
import matplotlib.pyplot as plt

# Print bar plot
def plot (subject_dict) :
    plt.xlabel("Rechtsgebieden")
    plt.ylabel("Arresten")
    plt.xticks(rotation=90)
    plt.bar(subject_dict.keys(), subject_dict.values())
    plt.show() 

# main
def main () :
    folder = os.getcwd() + "/DataSets/OpenDataUitspraken"
    delimiter = "; "
    subjects_all = []
    for file in os.listdir(folder) :
        subjects = []
        xmlFile = open(folder + '/' + file, encoding="utf8")
        xml = BeautifulSoup(xmlFile, features="xml")
        xmlFile.close()
        subjectFound = xml.find_all('dcterms:subject')
        if (subjectFound is None) :
            print(file)
        for c,i in enumerate(xml.find_all('dcterms:subject')) :
            # if (c == 1) :
            #     print(file)
            #     print(i)
            if (delimiter in i.getText()) :
                x = i.getText().split(delimiter)
                #print(x)
                for j in x :
                    subjects.append(j)
            else :
                #print(i.getText())
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
