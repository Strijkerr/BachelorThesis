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
selfReference =0
decisionList = []
errorList = []

lidodata = "DataSets/lidodata"
BachelorThesis = os.getcwd() + '/'
OpenDataUitspraken = BachelorThesis + "DataSets/OpenDataUitspraken/" # Uitkijken, als je de map als argument meegeeft aan de functie, dan geef je die meestal mee zonder / op het einde

csvFile = {
    "total": BachelorThesis + "CSV/Total.csv",
    "future": BachelorThesis + "CSV/Future.csv",
    "empty_citations": BachelorThesis + "CSV/EmptyC.csv",
    "empty_references": BachelorThesis + "CSV/EmptyR.csv",
    "missing_references": BachelorThesis + "CSV/Missing.csv",
    "reference_format_error": BachelorThesis + "CSV/RefError.csv",
    "self_reference": BachelorThesis + "CSV/SelfRef.csv"
}

rows = {
    "total": [],
    "future": [],
    "empty_citations": [],
    "empty_references": [],
    "missing_references": [],
    "reference_format_error": [],
    "self_reference": []
}

def writeToCSV (csvDestination,rows) :
    fields = ["ECLI","Ref_ECLI","Anchor text","Paragraph"]
    with open(csvDestination, 'w') as csvFile: # Seperated by in libreoffie can't be tab
        csvWriter = csv.writer(csvFile) 
        csvWriter.writerow(fields) 
        csvWriter.writerows(rows)

def writeToRow(paragraph,row_type) :
    row = [ECLI,ref_ECLI,citation,paragraph]
    rows[row_type].append(row)
    return True

def findReference(file,row_type) :
    referenceFound = False
    parser2 = etree.parse(file)
    root = parser2.getroot()
    abstract = root.find("{http://www.rechtspraak.nl/schema/rechtspraak-1.0}inhoudsindicatie") # Max = one abstract section in court decision
    decision = root.find("{http://www.rechtspraak.nl/schema/rechtspraak-1.0}uitspraak") # Max = one 'uitspraak' section in court decision

    if (abstract is not None) :
        for el in abstract.iter():
            if (el.text is not None) :
                if (citation in el.text) :
                    referenceFound = writeToRow(el.text,row_type)
            if (el.tail is not None) :
                if (citation in el.tail) :
                    referenceFound = writeToRow(el.tail,row_type)
    
    if (decision is not None) :
        for el in decision.iter():
            if (el.text is not None) :
                if (citation in el.text) :
                    referenceFound = writeToRow(el.text,row_type)
            if (el.tail is not None) :
                if (citation in el.tail) :
                    referenceFound = writeToRow(el.tail,row_type)
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
    print("Self references: ", selfReference)
    print("Reference ECLI format errors: ", referenceError)
    print("Citationcount/anchor texts: ", citationCount)
    print("Row count total: ", len(rows["total"]))
    print("Rows future count total: ", len(rows["future"]))
    print("References not found: ", ((missingReference-emptyCitation)-emptyReference))
    # print("Length emptyC: ",len(rows["empty_citations"]))
    # print("Length emptyR: ",len(rows["empty_references"]))
    # print("Length missing: ",(len(rows["missing_references"])-len(rows["empty_references"])-len(rows["empty_citations"])))

try:
    parser = etree.iterparse(BachelorThesis + lidodata, events=('start','end')) # Iterparse for parsing large xml files because large xml files don't fit into memory as a whole
    try:
        for event, element in parser:
            about = element.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about') # The 'about' attribute represents the content of the node
            if (about != None and about.startswith("http://linkeddata.overheid.nl/terms/jurisprudentie/id/ECLI:NL")): # We only want Dutch court cases
                try: # Get name, filename and reference
                    ECLI = about.rsplit('/', 1)[1] # Get ECLI filename
                    ECLI_filename = ECLI.replace(':', '_') + ".xml" # Remove ':' from filenames
                    citations = element.findall('{http://linkeddata.overheid.nl/terms/}refereertAan') # Get all references found in the ECLI metadata
                    count+=1 # Reference countrows
                    try :  
                        run_once = True                
                        for ref in citations :
                            if (ref.text != None and "target=ecli" in ref.text) : # We only want rulings that contain ECLI references
                                try :
                                    if os.path.exists(OpenDataUitspraken + ECLI_filename) : # Check if the LiDO legal rulings with > 0 references to other rulings are in the rechtspraak.nl dataset
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
                                                    writeToRow("-","empty_citations")
                                                    makeRow = False
                                                if (ref_ECLI == "!" or ref_ECLI == '\n' or ref_ECLI == '') : # We only want references that refer to something
                                                    emptyReference+=1
                                                    findReference(OpenDataUitspraken + ECLI_filename,"empty_references") # Als hij hem hierin niet vind, dan is het aantal rows niet gelijk aan #emptyReference
                                                    makeRow = False
                                                if (makeRow) :
                                                    year = ECLI.split(':')[3]
                                                    if (ECLI == ref_ECLI) :
                                                        selfReference+=1
                                                        findReference(OpenDataUitspraken + ECLI_filename,"self_reference")
                                                    if (re.match(r"!?ECLI:.+:.+:\d\d\d\d:.+",ref_ECLI)) : # Check future references, also allows ECLIECLI formats
                                                        ref_year = ref_ECLI.split(':')[3].split(':')[0]
                                                        if (int(ref_year) > int(year)) :
                                                            findReference(OpenDataUitspraken + ECLI_filename,"future")
                                                            futureReference+=1
                                                    else : 
                                                        referenceError+=1 # Reference not in the right format
                                                        findReference(OpenDataUitspraken + ECLI_filename,"reference_format_error")
                                                    try :
                                                        if not findReference(OpenDataUitspraken + ECLI_filename,"total") : # There might be more occurences of citations in the text     
                                                            writeToRow("-","missing_references")
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

for file in csvFile :
    if not os.path.exists(csvFile[file]) :
        writeToCSV(csvFile[file],rows[file])

printStats()
printErrorlist()
print("Seconds:",time.time()-seconds)