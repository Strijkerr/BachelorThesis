#!/usr/bin/python3
import sys
import os
import time
from bs4 import BeautifulSoup
from collections import Counter
import matplotlib.pyplot as plt

#folder = sys.argv[1]
folder = "/home/jonathan/Desktop/OpenDataUitspraken"
seconds = time.time()
delimiter = "; "
subjects_all = []
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

plt.xlabel("Rechtsgebieden")
plt.ylabel("Arresten")
plt.xticks(rotation=90)
plt.bar(subject_dict.keys(), subject_dict.values())
print(subject_dict) # Print dict met frequency arresten per rechtsgebied
plt.show() # Print bar plot
print("Seconds:",time.time()-seconds)