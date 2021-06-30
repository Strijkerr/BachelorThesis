#!/usr/bin/python3
# Source for download progress bar: https://stackoverflow.com/questions/37573483/progress-bar-while-download-file-over-http-with-requests
# Manual source 'OpenDataUitspraken' dataset: https://www.rechtspraak.nl/Uitspraken/paginas/open-data.aspx
from tqdm import tqdm
import requests
import os
import time
import subprocess
from datetime import date

today = str(date.today())
cwd = os.getcwd()
OpenDataUitspraken = cwd + "/DataSets/OpenDataUitspraken"
OpenDataUitspraken_zip = OpenDataUitspraken + '.zip'
url = "https://static.rechtspraak.nl/PI/OpenDataUitspraken.zip"
url2 = "https://data.overheid.nl/OpenDataSets/lido/lidodata.gz"
lidodata = cwd + "/DataSets/lidodata"
lidodata_gz = lidodata + '.gz'

def download_1 () :
    if not os.path.exists(OpenDataUitspraken_zip) :
        response = requests.get(url, stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0)) # Misschien dit wegschrijven naar info.txt om te checken voor updates bij volgende download
        block_size = 1024 #1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(OpenDataUitspraken_zip, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong!")
        else :
            print("Dataset succesfully downloaded!\n")
            with open(cwd + "/DataSets/info.txt",'w') as f :
                f.write("Date of last download 'OpenDataUitspraken': " + today + '\n')
    else :
        print("'" + OpenDataUitspraken_zip + "' already exists, please delete first before redownloading.\n")

def download_2 () :
    if not os.path.exists(lidodata_gz) :
        response = requests.get(url2, stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0)) # Misschien dit wegschrijven naar info.txt om te checken voor updates bij volgende download
        block_size = 1024 #1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(lidodata_gz, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong!")
        else :
            print("Dataset succesfully downloaded!\n")
            with open(cwd + "/DataSets/info.txt",'w') as f :
                f.write("Date of last download 'lidodata': " + today + '\n')
    else :
        print("'" + lidodata_gz + "' already exists, please delete first before redownloading.\n")

def filter () :
    if os.path.exists(OpenDataUitspraken) :
        subprocess.call(['python3','Scripts/filterAbstractsJudgments.py'])
    else :
        print("'" + OpenDataUitspraken + "' does not exist yet, please download/unzip it first.\n")

def getCount () :
    subprocess.call(['sh', cwd + '/Scripts/countFiles.sh',OpenDataUitspraken])

def menu () :
    while True :
        print("------------------------------------------------------")
        print("----------------------MAIN MENU----------------------")
        print("------------------------------------------------------\n")
        print("1. Activate setup menu")
        print("2. Edit 'OpenDataUitspraken'")
        print("3. Tools 'OpenDataUitspraken'\n")
        print("4. Exit")
        var = input('Enter action: ')
        if (var == '1') :
            setupMenu()
        elif (var == '2') :
            editMenu()
        elif (var == '3') :
            subMenu()
        elif (var == '4') :
            print("Program ended.")
            return    

def editMenu () :
     while True :
        print("------------------------------------------------------")
        print("---------------EDIT 'OpenDataUitspraken'--------------")
        print("------------------------------------------------------\n")
        print("1. Remove all court decisions that have no abstract and no judgment from 'OpenDataUitspraken' (< 25 minutes ETA)\n")
        print("2. Exit to main menu")
        var = input('Enter action: ')
        if (var == '1') :
            seconds = timer(False)
            filter()
            print("Seconds:",time.time()-seconds)
        elif (var == '2') :
            return    

def overview () :
    subprocess.call(['python3','Scripts/overviewAbstractsJudgments.py'])

def plotCourts () :
    subprocess.call(['python3','Visualization/plotCourts.py'])

def plotYears () :
    subprocess.call(['python3','Visualization/plotYears.py'])

def setupMenu () :
    while True :
        if os.path.exists(OpenDataUitspraken_zip) :
            string1 = "(Done)"
        else :
            string1 = '\t '
        if os.path.exists(OpenDataUitspraken) :
            string2 = "(Done)"
        else :
            string2 = '\t '
        if os.path.exists(lidodata_gz) :
            string3 = "(Done)"
        else :
            string3 = '\t '
        if os.path.exists(lidodata) :
            string4 = "(Done)"
        else :
            string4 = '\t '
        print("------------------------------------------------------")
        print("----------------------SETUP MENU----------------------")
        print("------------------------------------------------------\n")
        print("1. " + string1 + " Download 'OpenDataUitspraken.zip' (+~5.4GB needs to be available)")
        print("2. " + string2 + " Unzip and unpack 'OpenDataUitspraken.zip' (+~24GB needs to be available)")
        print("3. " + string3 + " Download 'lidodata.gz' (+~1.4GB needs to be available)")
        print("4. " + string4 + " Unzip and unpack 'OpenDataUitspraken.zip' (+~38.2GB needs to be available)\n")
        print("5. Exit to main menu")
        var = input('Enter action: ')
        if (var == '1') :
            seconds = timer(False)
            download_1()
            print("Seconds:",time.time()-seconds)
        elif (var == '2') :
            seconds = timer(False)
            unzip()
            print("Seconds:",time.time()-seconds)
        elif (var == '3') :
            seconds = timer(False)
            download_2()
            print("Seconds:",time.time()-seconds)
        elif (var == '4') :
            seconds = timer(False)
            print("No implementation yet")
            print("Seconds:",time.time()-seconds)
        elif (var == '5') :
            return     

def subMenu () :
    if os.path.exists(OpenDataUitspraken) :
        while True :
            print("-------------------------------------------------------")
            print("---------------TOOLS 'OpenDataUitspraken'--------------")
            print("-------------------------------------------------------\n")
            print("1. Get court-decision count (< 3 seconds ETA)")
            print("2. Overview existence of abstracts and judgments in dataset (< 90 minutes ETA)")
            print("3. Plot graph (court decisions against years) (exit figure to continue)")
            print("4. Plot graph (court decisions against courts) (exit figure to continue)")
            print("5. Plot graph (court decisions against areas of law) (exit figure to continue)\n")
            print("6. Exit to main menu")
            var = input('Enter action: ')
            if (var == '1') :
                seconds = timer(True)
                getCount()
                print("Seconds:",time.time()-seconds)
            elif (var == '2') :
                seconds = timer(True)
                overview()
                print("Seconds:",time.time()-seconds)
            elif (var == '3') :
                plotYears()
            elif (var == '4') :
                plotCourts()
            elif (var == '5') :
                print("No implementation yet")
            elif (var == '6') :
                return     
    else :
        print("'" + OpenDataUitspraken + "' does not exist yet, please download/unzip it first.\n")
        return

def timer (result) :
    seconds = time.time()
    print("Started: " + time.ctime(seconds))
    if (result) :
        print("Result:\n---------")
    return seconds

def unzip () :
    if not os.path.exists(OpenDataUitspraken_zip) :
        print("'" + OpenDataUitspraken_zip + "' does not exist yet, please download it first.\n")
    else :
        if not os.path.exists(OpenDataUitspraken) :
            print("Unzipping & unpacking")
            subprocess.call(['unzip',OpenDataUitspraken_zip,'-d',OpenDataUitspraken])
            subprocess.call(['sh', cwd + '/Scripts/unpack.sh',OpenDataUitspraken])
        else :
            print("'" + OpenDataUitspraken + "' already exists, please delete first before redownloading.\n")

if os.path.exists(cwd + "/DataSets/info.txt") :
    with open(cwd + "/DataSets/info.txt",'r') as f :
        print(f.read())

menu()