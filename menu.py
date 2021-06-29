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
folder = cwd + "/DataSets/OpenDataUitspraken"
folder_zip = folder + '.zip'
LiDO_file = cwd + "/DataSets/lidodata"
url = "https://static.rechtspraak.nl/PI/OpenDataUitspraken.zip"

def download_1 () :
    if not os.path.exists(folder_zip) :
        response = requests.get(url, stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0)) # Misschien dit wegschrijven naar info.txt om te checken voor updates bij volgende download
        block_size = 1024 #1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(folder_zip, 'wb') as file:
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
        print("'" + folder_zip + "' already exists, please delete first before redownloading.\n")

def download_2 () :
    if not os.path.exists(LiDO_file) :
        response = requests.get(url, stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0)) # Misschien dit wegschrijven naar info.txt om te checken voor updates bij volgende download
        block_size = 1024 #1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(folder_zip, 'wb') as file:
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
        print("'" + folder_zip + "' already exists, please delete first before redownloading.\n")

def filter () :
    if os.path.exists(folder) :
        subprocess.call(['python3','Scripts/filterAbstractsJudgments.py'])
    else :
        print("'" + folder + "' does not exist yet, please download/unzip it first.\n")

def getCount () :
    subprocess.call(['sh', cwd + '/Scripts/countFiles.sh',folder])

def menu () :
    while True :
        print("------------------------------------------------------")
        print("----------------------MAIN MENU----------------------")
        print("------------------------------------------------------\n")
        print("1. Activate setup menu")
        print("2. Edit 'OpenDataUitspraken'")
        print("3. Tools 'OpenDataUitspraken'")
        print("4. Exit")
        var = input('\nEnter action: ')
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
        print("1. Remove all court decisions that have no abstract and no judgment from 'OpenDataUitspraken' (< 25 minutes ETA)")
        print("2. Exit")
        var = input('\nEnter action: ')
        if (var == '1') :
            seconds = timer(False)
            filter()
            print("Seconds:",time.time()-seconds)
        elif (var == '2') :
            return    

def overview () :
    subprocess.call(['python3','Scripts/overviewAbstractsJudgments.py'])

def plotYears () :
    subprocess.call(['python3','Visualization/plotYears.py'])

def setupMenu () :
    while True :
        if os.path.exists(folder_zip) :
            string1 = "(Done)"
        else :
            string1 = ''
        if os.path.exists(folder) :
            string2 = "(Done)"
        else :
            string2 = ''
        print("------------------------------------------------------")
        print("----------------------SETUP MENU----------------------")
        print("------------------------------------------------------\n")
        print("1. " + string1 + " Download 'OpenDataUitspraken.zip' (+~5.4GB needs to be available)")
        print("2. " + string2 + " Unzip and unpack 'OpenDataUitspraken.zip' (+~24GB needs to be available)")
        print("3. Exit setup")
        var = input('\nEnter action: ')
        if (var == '1') :
            seconds = timer(False)
            download_1()
            print("Seconds:",time.time()-seconds)
        elif (var == '2') :
            seconds = timer(False)
            unzip()
            print("Seconds:",time.time()-seconds)
        elif (var == '3') :
            return     

def subMenu () :
    if os.path.exists(folder) :
        while True :
            print("-------------------------------------------------------")
            print("---------------Tools 'OpenDataUitspraken'--------------")
            print("-------------------------------------------------------\n")
            print("1. Get court-decision count (< 3 seconds ETA)")
            print("2. Overview existence of abstracts and judgments in dataset (< 90 minutes ETA)")
            print("3. Plot graph (court decisions against years) (< 5 seconds, exit figure to continue)")
            print("4. Plot graph (court decisions against courts)")
            print("5. Plot graph (court decisions against areas of law)")
            print("6. Exit scripts")
            var = input('\nEnter action: ')
            if (var == '1') :
                seconds = timer(True)
                getCount()
                print("Seconds:",time.time()-seconds)
            elif (var == '2') :
                seconds = timer(True)
                overview()
                print("Seconds:",time.time()-seconds)
            elif (var == '3') :
                seconds = timer(True)
                plotYears()
                print("Seconds:",time.time()-seconds)
            elif (var == '4') :
                seconds = timer(True)
                print("No implementation yet")
                print("Seconds:",time.time()-seconds)
            elif (var == '5') :
                seconds = timer(True)
                print("No implementation yet")
                print("Seconds:",time.time()-seconds)
            elif (var == '6') :
                print("Scripts ended.")
                return     
    else :
        print("'" + folder + "' does not exist yet, please download/unzip it first.\n")
        return

def timer (result) :
    seconds = time.time()
    print("Started: " + time.ctime(seconds))
    if (result) :
        print("Result:\n---------")
    return seconds

def unzip () :
    if not os.path.exists(folder_zip) :
        print("'" + folder_zip + "' does not exist yet, please download it first.\n")
    else :
        if not os.path.exists(folder) :
            print("Unzipping & unpacking")
            subprocess.call(['unzip',folder_zip,'-d',folder])
            subprocess.call(['sh', cwd + '/Scripts/unpack.sh',folder])
        else :
            print("'" + folder + "' already exists, please delete first before redownloading.\n")

if os.path.exists(cwd + "/DataSets/info.txt") :
    with open(cwd + "/DataSets/info.txt",'r') as f :
        print(f.read())

menu()