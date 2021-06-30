#!/usr/bin/python3
# Source for download progress bar: https://stackoverflow.com/questions/37573483/progress-bar-while-download-file-over-http-with-requests
# Manual source 'OpenDataUitspraken' dataset: https://www.rechtspraak.nl/Uitspraken/paginas/open-data.aspx
# Manual source 'lidodata' dataset: https://data.overheid.nl/en/dataset/linked-data-overheid
from tqdm import tqdm
import requests
import os
import time
import subprocess
from datetime import date

cwd = os.getcwd()
OpenDataUitspraken = cwd + "/DataSets/OpenDataUitspraken"
OpenDataUitspraken_zip = OpenDataUitspraken + '.zip'
OpenDataUitspraken_url = "https://static.rechtspraak.nl/PI/OpenDataUitspraken.zip"
lidodata = cwd + "/DataSets/lidodata"
lidodata_gz = lidodata + '.gz'
lidodata_url = "https://data.overheid.nl/OpenDataSets/lido/lidodata.gz"

def download (url,zip) :
    today = str(date.today())
    if not os.path.exists(zip) :
        response = requests.get(url, stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0))
        print(total_size_in_bytes)
        block_size = 1024 #1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(zip, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong!")
        else :
            print("Dataset succesfully downloaded!\n")
            with open(cwd + "/DataSets/info.txt",'a') as f :
                f.write("Date of last download '" + zip + "': " + today + '\nBytes: ' + str(total_size_in_bytes) + '\n')
            f.close()
    else :
        print("'" + zip + "' already exists, please delete first before redownloading.\n")

def gzip () :
    if not os.path.exists(lidodata_gz) :
        print("'" + lidodata_gz + "' does not exist yet, please download it first.\n")
    else :
        if not os.path.exists(OpenDataUitspraken) :
            print("Unzipping")
            subprocess.call(['gzip','-d',lidodata_gz])
        else :
            print("'" + lidodata + "' already exists, please delete first before unzipping again.\n")

def menu () :
    if os.path.exists(cwd + "/DataSets/info.txt") :
        with open(cwd + "/DataSets/info.txt",'r') as f :
            print(f.read())
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
            menu_setup()
        elif (var == '2') :
            menu_edit()
        elif (var == '3') :
            menu_tools()
        elif (var == '4') :
            print("Program ended.")
            return  

def menu_edit () :
    if os.path.exists(OpenDataUitspraken) :
        while True :
            print("------------------------------------------------------")
            print("---------------EDIT 'OpenDataUitspraken'--------------")
            print("------------------------------------------------------\n")
            print("1. Remove all court decisions that have no abstract and no judgment from 'OpenDataUitspraken' (< 25 minutes ETA)")
            print("2. Exit to main menu")
            var = input('\nEnter action: ')
            if (var == '1') :
                seconds = timer(False)
                subprocess.call(['python3','Scripts/filterAbstractsJudgments.py'])
                print("Seconds:",time.time()-seconds)
            elif (var == '2') :
                return 
    else :
        print("'" + OpenDataUitspraken + "' does not exist yet, please download/unzip it first.\n")
        return

def menu_setup () :
    while True :
        print("------------------------------------------------------")
        print("----------------------SETUP MENU----------------------")
        print("------------------------------------------------------\n")
        print("1. Download 'OpenDataUitspraken.zip' (+~5.4GB needs to be available) (ETA < 9 minutes)")
        print("2. Unzip and unpack 'OpenDataUitspraken.zip' (+~24GB needs to be available) (ETA < 37 minutes")
        print("3. Download 'lidodata.gz' (+~1.4GB needs to be available) (ETA < 7 minutes")
        print("4. Unzip and unpack 'OpenDataUitspraken.zip' (+~38.2GB needs to be available) (ETA < 11 minutes)")
        print("5. Exit to main menu")
        var = input('\nEnter action: ')
        if (var == '1') :
            seconds = timer(False)
            download(OpenDataUitspraken_url,OpenDataUitspraken_zip)
            print("Seconds:",time.time()-seconds)
        elif (var == '2') :
            seconds = timer(False)
            unzip()
            print("Seconds:",time.time()-seconds)
        elif (var == '3') :
            seconds = timer(False)
            download(lidodata_url,lidodata_gz)
            print("Seconds:",time.time()-seconds)
        elif (var == '4') :
            seconds = timer(False)
            gzip()
            print("Seconds:",time.time()-seconds)
        elif (var == '5') :
            return   

def menu_tools () :
    if os.path.exists(OpenDataUitspraken) :
        while True :
            print("-------------------------------------------------------")
            print("---------------TOOLS 'OpenDataUitspraken'--------------")
            print("-------------------------------------------------------\n")
            print("1. Get court-decision count (< 3 seconds ETA)")
            print("2. Overview existence of abstracts and judgments in dataset (< 90 minutes ETA)")
            print("3. Plot graph (court decisions against years) (exit figure to continue)")
            print("4. Plot graph (court decisions against courts) (exit figure to continue)")
            print("5. Plot graph (court decisions against areas of law) (exit figure to continue)")
            print("6. Exit to main menu")
            var = input('\nEnter action: ')
            if (var == '1') :
                seconds = timer(True)
                subprocess.call(['sh', cwd + '/Scripts/countFiles.sh',OpenDataUitspraken])
                print("Seconds:",time.time()-seconds)
            elif (var == '2') :
                seconds = timer(True)
                subprocess.call(['python3','Scripts/overviewAbstractsJudgments.py'])
                print("Seconds:",time.time()-seconds)
            elif (var == '3') :
                subprocess.call(['python3','Visualization/plotYears.py'])
            elif (var == '4') :
                subprocess.call(['python3','Visualization/plotCourts.py'])
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
            #os.remove(OpenDataUitspraken_zip) # Aanzetten in final release
        else :
            print("'" + OpenDataUitspraken + "' already exists, please delete first before unzipping again.\n")
menu()