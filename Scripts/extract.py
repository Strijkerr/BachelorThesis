#!/usr/bin/python3
from lxml import etree
import os
import csv
import sys
from collections import Counter

def checkExcluded (decisionList,OpenDataUitspraken) :
    years = []
    temp_count = 0
    for file in os.listdir(OpenDataUitspraken) :
        if (file not in decisionList) :
            temp_count+=1
            year = file.split('_')[3]
            if (int(year) < 2019) :
                years.append('<= 2018')
            else :
                years.append(year)
    print("\nCourt decisions ecluded: ",temp_count)
    print("Court decisions excluded distribution over years: ",Counter(years).most_common())


def main () :
    OpenDataUitspraken = sys.argv[1]
    cwd = sys.argv[2]
    lidodata = sys.argv[3]

    citationCount = 0
    decisionList = []
    decisionList2 = []
    errorList = []
    refNone = 0
    refElse = 0
    aboutElse = 0
    csvFile = cwd + "/CSV/Total.csv"
    rows = []
    aboutNone = 0
    aboutECLI = 0 
    decisionNotPresent = 0
    parser = etree.iterparse(lidodata, events=('start','end'))
    
    for event, element in parser: # Loop through lidodata
        about = element.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about') # The 'about' attribute represents the content of the node
        if (about == None) :
            aboutNone+=1
        elif (about.startswith("http://linkeddata.overheid.nl/terms/jurisprudentie/id/ECLI:NL")): # Filter for Dutch court cases
            ECLI = about.rsplit('/', 1)[1] # Get ECLI
            ECLI_filename = ECLI.replace(':', '_') + ".xml" # Translate ECLI to ECLI filename in `OpenDataUitspraken'`
            aboutECLI+=1 # Count ECLI meta
            if os.path.exists(OpenDataUitspraken + '/' +  ECLI_filename) : # Court decision must also exist in `OpenDataUitspraken`
                decisionList.append(ECLI_filename) # Run once per ECLI
                references = element.findall('{http://linkeddata.overheid.nl/terms/}refereertAan') # Get all references in that node
                run_once = True             
                for ref in references : # Loop through all* references
                    if (ref.text == None) :
                        refNone+=1
                    elif ("target=ecli" in ref.text) : # Filter for ECLI references
                        if (run_once) :
                            decisionList2.append(ECLI)
                            run_once = False
                        try :
                            citation = ref.text.split("opschrift=")[1]
                            ref_ECLI = ref.text.split("uri=")[1].split('|')[0]
                            citationCount+=1
                            row = [ECLI,ref_ECLI,citation]
                            rows.append(row)
                        except Exception as e :
                            errorList.append(ECLI) # 9 exceptions here
                    else :
                        refElse+=1
            else :
                decisionNotPresent+=1
        else :
            aboutElse+=1
        element.clear() # Frees memory
    printStats(aboutECLI,decisionList,decisionList2,citationCount,aboutNone,aboutElse,decisionNotPresent,refNone,refElse)
    printErrorlist(errorList)
    writeToCSV(csvFile,rows,["ECLI","Ref_ECLI","Anchor text"])
    checkExcluded(decisionList,OpenDataUitspraken)

def printErrorlist(errorList) :
    if errorList :
        print("\nThe following ECLI's have not been parsed because of an error (in the dumpfile):")
        for i in errorList :
            print(i)

def printStats(aboutECLI,decisionList,decisionList2,citationCount,aboutNone,aboutElse,decisionNotPresent,refNone,refElse) :
    print("Total ECLI elements in LiDO dataset: ", aboutECLI)
    print("Dutch court rulings with in LiDO dataset that intersect with `OpenDataUitspraken` dataset: ",len(decisionList))
    print("Final amount of court cases (intersections-doubles): ", len(set(decisionList)))
    print("Dutch court rulings with in LiDO dataset that intersect with `OpenDataUitspraken` dataset and have > 0 ecli references: ",len(decisionList2))
    print("Final amount of court cases (intersections-doubles) and have > 0 ecli references: ", len(set(decisionList2)))
    print("Citations: ", citationCount)
    print("Empty elements (useless)",aboutNone)  # Useless
    print("Elements not ECLI (useless)",aboutElse) # Useless
    print("Court decision not present in `OpenDataUitspraken': ",decisionNotPresent) # Useless
    print("refNone",refNone) # Uitzoeken hoe dit kan, waarom zijn deze None
    print("refElse",refElse) # Useless

def writeToCSV (csvFile,rows,fields) :
    if not os.path.exists(csvFile) :
        with open(csvFile, 'w') as csvOpen: # Seperated by in libreoffie can't be tab
            csvWriter = csv.writer(csvOpen) 
            csvWriter.writerow(fields) 
            csvWriter.writerows(rows)

main()
