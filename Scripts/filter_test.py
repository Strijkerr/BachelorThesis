#!/usr/bin/python3
import os
import sys

def main () :
    file1 = os.getcwd() + '/DataSets/lidodata'
    file2 = os.getcwd() + '/DataSets/lidotest'
    resetFile(file2)
    with open(file1) as input_file :
        with open(file2, 'a') as output_file :
            for c,line in enumerate(input_file):
                print(c)
                output_file.write(line)                  

def resetFile (file2) :
    create = open(file2, 'w')
    create.close()

main()