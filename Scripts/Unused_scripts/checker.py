#!/usr/bin/python3
from csv import reader
import os
import csv
import re



def main () :
    file = os.getcwd() + "/CSV/Vitale.csv"
    vitale = 0
    count = 0
    wordList = []
    with open(file, 'r') as total :
        csv_reader = reader(total)
        next(csv_reader) # Skip header
        regex = re.compile(r'\b{}\b \b(\w+)\b'.format("vitale")) 
        for row in csv_reader :
            count+=1
            for i in regex.findall(row[3]) :
                if (i in wordList) :
                    vitale+=1
                else :
                    os.system('clear')
                    print("False positives: ",vitale)     
                    print("Total: ",count)
                    print("\nWord: ",i)
                    print("\nSentence: ",row[3])
                    answer = input("\nTo add this word to exception list, type: `y'\n\nAnswer: ")
                    if (answer == 'y') :
                        wordList.append(i)
    print(wordList)

main()