#!/usr/bin/python3
# Source for download progress bar: https://stackoverflow.com/questions/37573483/progress-bar-while-download-file-over-http-with-requests
# Manual source 'OpenDataUitspraken' dataset: https://www.rechtspraak.nl/Uitspraken/paginas/open-data.aspx
from tqdm import tqdm
import requests
import os
import subprocess
from datetime import date

today = str(date.today())
cwd = os.getcwd()
folder = cwd + "/DataSets/OpenDataUitspraken"
folder_zip = folder + '.zip'
url = "https://static.rechtspraak.nl/PI/OpenDataUitspraken.zip"

if os.path.exists(cwd + "/DataSets/info.txt") :
    with open(cwd + "/DataSets/info.txt",'r') as f :
        print(f.read())

def menu () :
    while True :
        print("------------------------------------------------------")
        print("----------------------SETUP MENU----------------------")
        print("------------------------------------------------------\n")
        print("1. Download 'OpenDataUitspraken.zip' (+~5.4GB needs to be available)")
        print("2. Unzip and unpack 'OpenDataUitspraken.zip' (+~24GB needs to be available)")
        print("3. Filter for court decisions with an abstract/judgment in 'OpenDataUitspraken'")
        print("4. Activate script menu'")
        print("5. Exit")
        var = input('\nEnter action: ')
        if (var == '1') :
            download()
        elif (var == '2') :
            unzip()
        elif (var == '3') :
            filter()
        elif (var == '4') :
            subMenu()
        elif (var == '5') :
            print("Setup ended.")
            return     

def subMenu () :
    while True :
        print("------------------------------------------------------")
        print("----------------------SCRIPT MENU---------------------")
        print("------------------------------------------------------\n")
        print("1. Overview abstracts and judgments")
        print("2. Exit")
        var = input('\nEnter action: ')
        if (var == '1') :
            overview()
        elif (var == '2') :
            return     

def overview () :
    if os.path.exists(folder) :
        subprocess.call(['python3','overviewAbstractsJudgements.py'])
    else :
        print("'" + folder + "' does not exist yet, please download/unzip it first.\n")

def filter () :
    if os.path.exists(folder) :
        subprocess.call(['python3','filterUitspraken.py'])
    else :
        print("'" + folder + "' does not exist yet, please download/unzip it first.\n")


def unzip () :
    if not os.path.exists(folder_zip) :
        print("'" + folder_zip + "' does not exist yet, please download it first.\n")
    else :
        if not os.path.exists(folder) :
            print("Unzipping & unpacking")
            subprocess.call(['unzip',folder_zip,'-d',folder])
            subprocess.call(['sh', cwd + '/SideScripts/unpack.sh',folder])
        else :
            print("'" + folder + "' already exists, please delete first before redownloading.\n")

def download () :
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
menu()