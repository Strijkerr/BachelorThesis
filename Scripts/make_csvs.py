#!/usr/bin/python3
from lxml import etree
import os
import csv
import re
import sys

OpenDataUitspraken = sys.argv[1]
BachelorThesis = sys.argv[2]
lidodata = sys.argv[3]

emptyCitation = 0
citationCount = 0
emptyReference = 0
futureReference = 0
referenceError = 0
missingReference = 0
selfReference =0
decisionList = []
decisionList2 = []
errorList = []

aboutNone = 0
aboutECLI = 0 
decisionNotPresent = 0

refNone = 0
refElse = 0
aboutElse = 0

csvFile = {
    "total": BachelorThesis + "/CSV/Total.csv",
    "future": BachelorThesis + "/CSV/Future.csv",
    "empty_citations": BachelorThesis + "/CSV/EmptyC.csv",
    "empty_references": BachelorThesis + "/CSV/EmptyR.csv",
    "missing_references": BachelorThesis + "/CSV/Missing.csv",
    "reference_format_error": BachelorThesis + "/CSV/RefError.csv",
    "self_reference": BachelorThesis + "/CSV/SelfRef.csv"
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
    abstract = root.find("{http://www.rechtspraak.nl/schema/rechtspraak-1.0}inhoudsindicatie") # One abstract section in court decision
    decision = root.find("{http://www.rechtspraak.nl/schema/rechtspraak-1.0}uitspraak") # One 'uitspraak' section in court decision

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
    print("Total ECLI elements in LiDO dataset: ", aboutECLI)
    print("Dutch court rulings with in LiDO dataset that intersect with `OpenDataUitspraken` dataset: ",len(decisionList))
    print("Final amount of court cases (intersections-doubles): ", len(set(decisionList)))
    print("Dutch court rulings with in LiDO dataset that intersect with `OpenDataUitspraken` dataset and have > 0 ecli references: ",len(decisionList2))
    print("Final amount of court cases (intersections-doubles) and have > 0 ecli references: ", len(set(decisionList2)))
    print("Empty citations: ", emptyCitation)
    print("Empty references: ", emptyReference)
    print("Future references: ", futureReference)
    print("Self references: ", selfReference)
    print("Reference ECLI format errors: ", referenceError)
    print("Citationcount/anchor texts: ", citationCount)
    print("Total.csv row count total: ", len(rows["total"]))
    print("Future.csv row count total: ", len(rows["future"]))
    print("References not found: ", ((missingReference-emptyCitation)-emptyReference))

parser = etree.iterparse(lidodata, events=('start','end'))

for event, element in parser: # Loop through lidodata
    about = element.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about') # The 'about' attribute represents the content of the node
    if (about == None) :
        aboutNone+=1
    elif (about.startswith("http://linkeddata.overheid.nl/terms/jurisprudentie/id/ECLI:NL")): # Filter for Dutch court cases
        ECLI = about.rsplit('/', 1)[1] # Get ECLI
        ECLI_filename = '/' + ECLI.replace(':', '_') + ".xml" # Translate ECLI to ECLI filename in `OpenDataUitspraken'`
        aboutECLI+=1 # Count ECLI meta
        if os.path.exists(OpenDataUitspraken + ECLI_filename) : # Court decision must also exist in `OpenDataUitspraken`
            decisionList.append(ECLI) # Run once per ECLI
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
                        # Hier gewoon totaal wegscrijven?
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
                            if not findReference(OpenDataUitspraken + ECLI_filename,"total") : # There might be more occurences of references in the text     
                                writeToRow("-","missing_references")
                                missingReference+=1
                    except Exception as e :
                        errorList.append(ECLI) # 10 exceptions here
                else :
                    refElse+=1
        else :
            decisionNotPresent+=1
    else :
        aboutElse+=1
    element.clear() # Frees memory

for file in csvFile :
    if not os.path.exists(csvFile[file]) :
        writeToCSV(csvFile[file],rows[file])

print("Empty elements (useless)",aboutNone)  # Useless
print("Elements not ECLI (useless)",aboutElse) # Useless
print("Court decision not present in `OpenDataUitspraken': ",decisionNotPresent) # Useless
print("refNone",refNone) # Uitzoeken hoe dit kan
print("refElse",refElse) # Useless

print('\n')
printStats()
printErrorlist()