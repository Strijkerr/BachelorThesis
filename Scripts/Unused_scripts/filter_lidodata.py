#!/usr/bin/python3
import os
import sys

def main () :
    count = 0
    file1 = sys.argv[1]
    file2 = os.getcwd() + '/DataSets/lidotest'
    resetFile(file2)
    with open(file1) as input_file :
        printing = False
        with open(file2, 'a') as output_file :
            for c,line in enumerate(input_file):
                print(c)
                if (c < 14) : 
                        output_file.write(line)
                else :                   
                    if (line.startswith("<rdf:Description rdf:about=\"http://linkeddata.overheid.nl/terms/jurisprudentie/id/ECLI:NL")) :
                        output_file.write(line)
                        count+=1
                        printing = True           
                    elif (printing and line != "\n") :
                        output_file.write(line)
                    elif (printing and line == "\n") :
                        output_file.write(line)
                        printing = False
            output_file.write("</rdf:RDF>")
    print("Nodes left: ",count)
    # os.remove(file1)
    # os.rename(file2, file1)

def resetFile (file2) :
    create = open(file2, 'w')
    create.close()

main()