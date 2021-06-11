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

#file = "lidodata"
file = "finalDecisions"
folder = "/home/jonathan/Desktop/"
folder2 = "/home/jonathan/Desktop/OpenDataUitspraken/" # Uitkijken, als je de map als argument meegeeft aan de functie, dan geef je die meestal mee zonder / op het einde
csvTotal = "/home/jonathan/Desktop/Total.csv"
csvFuture = "/home/jonathan/Desktop/Future.csv"

rows = []
rows_f = []
fields = ["ECLI","Ref_ECLI","Anchor text","Paragraph"]

def Patterns(citation) :
    # Bijna alles hier te vinden: https://documents.library.maastrichtuniversity.nl/open/c2de5acb-006a-4836-860a-eeb1fb721b94
    pattern_ECLI = r"(ECLI:(.+:)?.+:\d\d\d\d:.+)|(.+:.+:\d\d\d\d:.+)" # e.g. ECLI:NL:PHR:1981:AC3210
    pattern_BNB = r"BNB,? +\d\d\d\d" # "Beslissingen in belastingzaken, Nederlandse Belastingrechtspraak, afkorting BNB, is een juridisch vaktijdschrift voor Nederlandse jurisprudentie op het gebied van belastingrecht". - Wikipedia
    pattern_NJ = r"N\.?J\.? *\d\d\d\d" # "Nederlandse Jurisprudentie (NJ) is een tijdschrift waarin uitsluitend gerechtelijke uitspraken worden gepubliceerd." - wikipedia
    pattern_VN = r"V-?N,? +\d\d\d\d" 
    pattern_USZ = r"USZ,? +\d\d\d\d" # "Met het tijdschrift Uitspraken Sociale Zekerheid « USZ » heeft u snel inzicht in actuele socialezekerheidsrechtspraak!" SDU.nl
    pattern_LJN = r"LJN*" # "Het Landelijk Jurisprudentie Nummer of LJN is een unieke codering die tot juni 2013 gegeven werd aan elke gerechtelijke uitspraak in Nederland die werd gepubliceerd.", wikipedia
    pattern_RSV = r"RSV,? +\d\d\d\d" # RSV bevat alle belangrijke jurisprudentie op het terrein van de sociale zekerheid. Hier vindt u alle uitspraken die vanaf 1987 tot heden ook in het tijdschrift RSV gepubliceerd zijn. - navigator.nl
    pattern_TAR  = r"TAR,? +\d\d\d\d" # Tijdschrift voor Ambtenarenrecht
    pattern_JV = r"JV,? +\d\d\d\d" # Het tijdschrift Jurisprudentie Vreemdelingenrecht (JV)
    pattern_HR = r"(H\.?R\.? +\d)|(Hoge Raad,? .+)" # Hoge raad
    pattern_BR = r"BR,? +\d\d\d\d" # Het tijdschrift Bouwrecht staat in de markt bekend als hét maandblad voor rechtspraak en literatuur op het gebied van het bouwrecht. - https://www.wolterskluwer.nl
    pattern_IER = r"IER,? +\d\d\d\d" # Dit tijdschrift biedt informatie en opiniërende artikelen over auteursrecht, merkenrecht, octrooirecht, modellenrecht, kwekersrecht, handelsnaamrecht, onrechtmatige publicatie, het recht inzake misleidende reclame, mededingingsrecht en reclamerecht. - https://www.wolterskluwer.nl
    pattern_AB = r"AB,? +\d\d\d\d" # AB Rechtspraak Bestuursrecht is een tijdschrift waarin uitsluitend de belangrijkste uitspraken op het gebied van het Nederlandse bestuursrecht, milieurecht, ambtenarenrecht, bouwrecht, sociaal-verzekeringsrecht, onderwijsrecht en vreemdelingenrecht worden gepubliceerd. - wikipedia

    pattern_JB = r"JB,? +\d\d\d\d" # Jurisprudentie Bestuursrecht
    pattern_WFR = r"WFR,? +\d\d\d\d" # Weekblad voor Fiscaal Recht
    pattern_HvJ = r"(HvJ\)? .+)|(Hof van Justitie van \d)|(HvJEG .+)" # Hof van Justitie
    pattern_RvdW = r"RvdW,? \d\d\d\d" # Rechtspraak van de week
    pattern_RV = r"RV,? +\d\d\d\d" # Rechtspraak vreemdelingenrecht
    pattern_KG = r"KG,? +\d\d\d\d" # Kort geding (Tijdschrift is opgeheven per 1-1-2004. Opgegaan in Nederlandse Jurisprudentie feitenrechtspraak (NJF))
    pattern_NJO = r"NJO,? +\d\d\d\d" # NJ Onteigening (Tijdschrift is opgeheven.)
    pattern_DD = r"D\.?D\.? +\d\d" # Delikt en Delinkwent
    pattern_JAR = r"JAR,? +\d\d\d\d"
    pattern_VR = r"VR,? +\d\d\d\d"
    pattern_JSV = r"JSV,? +\d\d\d\d"
    pattern_EHRM = r"EHRM .*"
    pattern_FED = r"FED,? +\d\d\d\d"
    pattern_NTFR = r"NTFR,? +\d\d\d\d"
    pattern_rechtbank = r"rechtbank .+ van \d"
    pattern_Gerechtshof = r"(Gerechtshof (te )?.+ van \d)|(Hof .+ van \d)|(Hof .+ \d)"

    pattern_JABW = r"JABW,? +\d\d\d\d"
    pattern_NJB = r"NJB,? +\d\d\d\d"
    pattern_Belastingblad = r"Belastingblad +\d\d\d\d"
    pattern_EHRC = r"EHRC,? +\d\d\d\d"
    pattern_RZA = r"RZA,? +\d\d\d\d"
    pattern_Jur = r"(Jur. +\d\d\d\d)|(Jur. EG \d\d\d\d)|(Jurispr. \d\d\d\d)"
    pattern_FJR = r"FJR,? +\d\d\d\d"

    pattern_BIE = r"BIE,? +\d\d\d\d"
    pattern_PRG = r"PRG.? +\d\d\d\d"
    pattern_PJ = r"PJ,? +\d\d\d\d"
    pattern_ELRO = r"ELRO +.+"

    if not (re.match(pattern_ECLI, citation) or re.match(pattern_BNB, citation) or 
        re.match(pattern_NJ, citation) or re.match(pattern_VN, citation) or
        re.match(pattern_USZ, citation) or re.match(pattern_LJN, citation) or
        re.match(pattern_RSV, citation) or re.match(pattern_TAR, citation) or 
        re.match(pattern_HR, citation) or re.match(pattern_VR, citation) or 
        re.match(pattern_BR, citation) or re.match(pattern_IER, citation) or 
        re.match(pattern_AB, citation) or re.match(pattern_JB, citation) or 
        re.match(pattern_WFR, citation) or re.match(pattern_HvJ, citation) or 
        re.match(pattern_RvdW, citation) or re.match(pattern_RV, citation) or 
        re.match(pattern_KG, citation) or re.match(pattern_NJO, citation) or 
        re.match(pattern_DD, citation) or re.match(pattern_JAR, citation) or 
        re.match(pattern_FED, citation) or re.match(pattern_JSV, citation) or 
        re.match(pattern_EHRM, citation) or re.match(pattern_NTFR, citation) or 
        re.match(pattern_rechtbank, citation) or re.match(pattern_Gerechtshof, citation, re.IGNORECASE) or 
        re.match(pattern_JABW, citation) or re.match(pattern_NJB, citation) or 
        re.match(pattern_Belastingblad, citation) or re.match(pattern_EHRC, citation) or 
        re.match(pattern_RZA, citation) or re.match(pattern_EHRC, citation) or 
        re.match(pattern_Jur, citation) or re.match(pattern_FJR, citation) or 
        re.match(pattern_JV, citation) or re.match(pattern_BIE, citation) or 
        re.match(pattern_PJ, citation) or re.match(pattern_ELRO, citation) or 
        re.match(pattern_PRG, citation) or "nr." in citation or "no." in citation or 
        "nummer" in citation) :
        # if (citation.isnumeric()) :
        #     print(name[1])
        #     print(citation)
        #     print(ref_ECLI)
        print(citation)

def makeFolder (folderName) :
    if not os.path.exists(folderName) : # Create folder and subfolders if they don't exist already
        os.makedirs(folderName)

def writeToCSV (csvDestination,rows,fields) :
    with open(csvDestination, 'w') as csvFile: # Seperated by in libreoffie can't be tab
        csvWriter = csv.writer(csvFile) 
        csvWriter.writerow(fields) 
        csvWriter.writerows(rows)

def writeToRows(ECLI,file,citation,future) :
    # if (ECLI == "ECLI:NL:HR:1984:AC8252" and citation == "NJ 1982, 411") :
    #     print("hi")
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