#!/usr/bin/python3
import os

def main () :
    file1 = os.getcwd() + '/DataSets/lidodata'
    file2 = os.getcwd() + '/DataSets/test'
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
                        if (printing) :
                            print("Error")
                        printing = True
                        output_file.write(line)
                    elif (printing and line == "</rdf:Description>\n") :
                        printing = False
                        output_file.write(line)
                    elif (printing) :
                        output_file.write(line)
            output_file.write("</rdf:RDF>")

def resetFile (file2) :
    create = open(file2, 'w')
    create.close()

main()