#!/usr/bin/python3
import time
from lxml import etree
import os
import csv
import re

seconds = time.time()
count = 0 
emptyCitation = 0
citationCount = 0
emptyReference = 0
futureReference = 0
referenceError = 0
missingReference = 0
decisionList = []
errorList = []

#file = "DataSets/lidodata"
file = "DataSets/finalDecisions"
folder = os.getcwd() + '/'
folder2 = folder + "DataSets/OpenDataUitspraken/" # Uitkijken, als je de map als argument meegeeft aan de functie, dan geef je die meestal mee zonder / op het einde
csvTotal = folder + "Total.csv"
csvFuture = folder + "Future.csv"

rows = []
rows_f = []
fields = ["ECLI","Ref_ECLI","Anchor text","Paragraph"]

def makeFolder (folderName) :
    if not os.path.exists(folderName) : # Create folder and subfolders if they don't exist already
        os.makedirs(folderName)

def writeToCSV (csvDestination,rows,fields) :
    with open(csvDestination, 'w') as csvFile: # Seperated by in libreoffie can't be tab
        csvWriter = csv.writer(csvFile) 
        csvWriter.writerow(fields) 
        csvWriter.writerows(rows)

def writeToRows(ECLI,file,citation,future) :
    referenceFound = False
    parser2 = etree.parse(file)
    root = parser2.getroot()
    abstract = root.find("{http://www.rechtspraak.nl/schema/rechtspraak-1.0}inhoudsindicatie") # Always only one abstract section in court decision.
    decision = root.find("{http://www.rechtspraak.nl/schema/rechtspraak-1.0}uitspraak") # Always only one 'uitspraak' section in court decision.

    if (abstract is not None) :
        for child in abstract.findall(".//") : # All subelements in all levels beneath current node
            if child.text is not None :
                if (citation in child.text) :
                    referenceFound = True
                    row = [ECLI,ref_ECLI,citation,child.text]
                    if (future) :
                        rows_f.append(row)
                    else :
                        rows.append(row)
    
    if (decision is not None) :
        if (ECLI == "ECLI:NL:HR:1984:AC8252" and citation == "NJ 1982, 411") :
            for el in decision.iter():
                if (el.text is not None and el.text != '' and el.text != '\n') :
                    print('%r' % (el.text))
        for child in decision.findall(".//") : # All subelements in all levels beneath current node
                # testString = etree.tostring((child))
                # if (citation in testString.decode()) :
                #     print(child)
            if child.text is not None :
                if (citation in child.text) :
                    referenceFound = True
                    row = [ECLI,ref_ECLI,citation,child.text]
                    if (future) :
                        rows_f.append(row)
                    else :
                        rows.append(row)
    return(referenceFound)

def printErrorlist() :
    if errorList :
        print("\nThe following ECLI's have not been parsed because of an error (in the dumpfile):")
    for i in errorList :
        print(i)

def printStats() :
    print("Total Dutch court rulings in LiDO dataset: ", count)
    print("Dutch court rulings with >= 1 ECLI citations in LiDO dataset that intersect with rechtspraak.nl dataset(~530k): ",len(decisionList))
    print("Final amount of court cases (intersections-doubles): ", len(set(decisionList)))
    print("Empty citations: ", emptyCitation)
    print("Empty references: ", emptyReference)
    print("Future references: ", futureReference)
    print("Reference ECLI format errors: ", referenceError)
    print("Citationcount/anchor texts: ", citationCount)
    print("Row count total: ", len(rows))
    print("Rows future count total: ", len(rows_f))
    print("References not found: ", ((missingReference-emptyCitation)-emptyReference))

try:
    parser = etree.iterparse(folder + file, events=('start','end')) # Iterparse for parsing large xml files because large xml files don't fit into memory as a whole
    try:
        for event, element in parser:
            about = element.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about') # The 'about' attribute represents the content of the node
            if (about != None and about.startswith("http://linkeddata.overheid.nl/terms/jurisprudentie/id/ECLI:NL")): # We only want Dutch court cases
                try: # Get name, filename and reference
                    ECLI = about.rsplit('/', 1)[1] # Get ECLI filename
                    ECLI_filename = ECLI.replace(':', '_') + ".xml" # Remove ':' from filenames
                    citations = element.findall('{http://linkeddata.overheid.nl/terms/}refereertAan') # Get all references found in the ECLI metadata
                    count+=1 # Reference count
                    try :  
                        run_once = True                
                        for ref in citations :
                            if (ref.text != None and "target=ecli" in ref.text) : # We only want rulings that contain ECLI references
                                try :
                                    if os.path.exists(folder2 + ECLI_filename) : # Check if the LiDO legal rulings with > 0 references to other rulings are in the rechtspraak.nl dataset
                                        try :
                                            citation = ref.text.split("opschrift=")[1]
                                            citationCount+=1
                                            if (run_once) :
                                                decisionList.append(ECLI) # Run once per ECLI
                                                run_once = False
                                            try : # Run per citation
                                                ref_ECLI = ref.text.split("uri=")[1].split('|')[0]
                                                makeRow = True
                                                if (citation == "" or citation == '\n') : # We only want references with an anchor text
                                                    emptyCitation+=1
                                                    makeRow = False
                                                if (ref_ECLI == "!" or ref_ECLI == '\n') : # We only want references that refer to something
                                                    emptyReference+=1
                                                    makeRow = False
                                                if (makeRow) :
                                                    year = ECLI.split(':')[3]
                                                    if (re.match(r"!?ECLI:.+:.+:\d\d\d\d:.+",ref_ECLI)) : # Check future references
                                                        ref_year = ref_ECLI.split(':')[3].split(':')[0]
                                                        if (int(ref_year) > int(year)) :
                                                            writeToRows(ECLI,folder2 + ECLI_filename,citation,True)
                                                            futureReference+=1
                                                    else : 
                                                        referenceError+=1 # Reference not in the right format
                                                    try :
                                                        if not writeToRows(ECLI,folder2 + ECLI_filename,citation,False) : # There might be more occurences of citations in the text     
                                                            #print(ECLI,citation)
                                                            missingReference+=1
                                                    except Exception as e :
                                                        print(e) # Never reaches
                                            except Exception as e :
                                                print(e) # Never reaches
                                        except Exception as e :
                                            errorList.append(ECLI) # Hij pakt hier 10 ECLI's waarvan de verwijzing met findall niet goed gepakt wordt
                                except Exception as e :
                                    print(e) # Never reaches
                    except Exception as e :
                        print(e) # Never reaches
                except Exception as e :
                    print(e) # Never reaches
            element.clear() # Clear element from dump file, frees up memory
    except Exception as e :
        print(e) # Never reaches
except Exception as e :
    print(e) # Never reaches

if not os.path.exists(csvTotal) :
    writeToCSV(csvTotal,rows,fields)
if not os.path.exists(csvFuture) :
    writeToCSV(csvFuture,rows_f,fields)

printStats()
#printErrorlist()
print("Seconds:",time.time()-seconds)