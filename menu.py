#!/usr/bin/python3
# Source for download progress bar: https://stackoverflow.com/questions/37573483/progress-bar-while-download-file-over-http-with-requests
# Manual source 'OpenDataUitspraken.zip' dataset: https://www.rechtspraak.nl/Uitspraken/paginas/open-data.aspx
# After a manual download, place the .zip file inside 'BachelorThesis/DataSets/' before continuing with this program
# Manual source 'lidodata.gz' dataset: https://data.overheid.nl/en/dataset/linked-data-overheid
# After a manual download, place the .gz file inside 'BachelorThesis/DataSets/' before continuing with this program
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

CSV_total = cwd + "/CSV/Total.csv"

def download (url,zip) :
    today = str(date.today())
    if not os.path.exists(zip) :
        response = requests.get(url, stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0))
        print(total_size_in_bytes)
        block_size = 1024
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
            print("Unzipping succesful, gz file removed")
        else :
            print("'" + lidodata + "' already exists, please delete first before unzipping again.\n")

def main () :
    if os.path.exists(cwd + "/DataSets/info.txt") :
        with open(cwd + "/DataSets/info.txt",'r') as f :
            print(f.read())
    while True :
        print("------------------------------------------------------")
        print("----------------------MAIN MENU----------------------")
        print("------------------------------------------------------\n")
        print("1. Setup menu")
        print("2. TABLES and FIGURES 'OpenDataUitspraken'")
        print("3. CSV TOOLS")
        print("4. Exit")
        var = input('\nEnter action: ')
        if (var == '1') :
            menu_setup()
        elif (var == '2') :
            menu_tools()
        elif (var == '3') :
            menu_edit()
        elif (var == '4') :
            print("Program ended.")
            return  

def menu_edit () :
    if os.path.exists(OpenDataUitspraken) :
        while True :
            print("------------------------------------------------------")
            print("---------------------CSV TOOLS--------------------")
            print("------------------------------------------------------\n")
            print("1. Print most common anchor texts in extracted references")
            print("2. Print reference statistics and more")
            print("3. Make dedicated csv for 1 anchor text")
            print("4. Context analysis anchor text")
            print("5. Check future references")
            print("6. Make map of court decision in which anchor text is cited")
            print("7. Exit to main menu")
            var = input('\nEnter action: ')
            if (var == '1') :
                seconds = timer(True)
                subprocess.call(['python3','Scripts/CSV_scripts/most_common_anchors.py',CSV_total])
                print("Seconds:",time.time()-seconds)
            if (var == '2') :
                seconds = timer(True)
                subprocess.call(['python3','Scripts/CSV_scripts/check_uri.py',CSV_total])
                print("Seconds:",time.time()-seconds)
            if (var == '3') :
                var2 = input('\nEnter anchor text: ')
                seconds = timer(True)
                subprocess.call(['python3','Scripts/CSV_scripts/make_dedicated_csv.py',cwd,var2])
                print("Seconds:",time.time()-seconds)
            if (var == '4') :
                var2 = input('\nEnter anchor text: ')
                seconds = timer(True)
                subprocess.call(['python3','Scripts/CSV_scripts/context_analysis.py',cwd,var2])
                print("Seconds:",time.time()-seconds)
            if (var == '5') :
                seconds = timer(True)
                subprocess.call(['python3','Scripts/CSV_scripts/future_references.py',cwd])
                print("Seconds:",time.time()-seconds)
            if (var == '6') :
                var2 = input('\nEnter anchor text: ')
                seconds = timer(True)
                subprocess.call(['python3','Scripts/CSV_scripts/make_map.py',var2])
                print("Seconds:",time.time()-seconds)
            elif (var == '7') :
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
        print("3. Remove all court decisions that have no textual parts in them from `OpenDataUitspraken' (< 25 minutes ETA)")
        print("4. Download 'lidodata.gz' (+~1.4GB needs to be available) (ETA < 7 minutes)")
        print("5. Unzip `lidodata.gz` (+~38.2GB needs to be available) (ETA < 11 minutes)")
        print("6. Extract case law references from `lidodata' to a CSV (ETA < 80 minutes)")
        print("7. Exit to main menu")
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
            seconds = timer(True)
            subprocess.call(['python3','Scripts/filter_OpenDataUitspraken.py',OpenDataUitspraken])
            print("Seconds:",time.time()-seconds)
        elif (var == '4') :
            seconds = timer(False)
            download(lidodata_url,lidodata_gz)
            print("Seconds:",time.time()-seconds)
        elif (var == '5') :
            seconds = timer(False)
            gzip()
            print("Seconds:",time.time()-seconds)
        elif (var == '6') :
            seconds = timer(True)
            subprocess.call(['python3','Scripts/extract.py',OpenDataUitspraken,cwd,lidodata])
            print("Seconds:",time.time()-seconds)   
        elif (var == '7') :
            return   

def menu_tools () :
    if os.path.exists(OpenDataUitspraken) :
        while True :
            print("-------------------------------------------------------")
            print("--------TABLES and FIGURES 'OpenDataUitspraken'--------")
            print("-------------------------------------------------------\n")
            print("1. Get court-decision count (< 3 seconds ETA)")
            print("2. Overview existence of judgments/advisory opinions and abstracts in dataset (< 90 minutes ETA)")
            print("3. Overview references found in metadata of files in dataset")
            print("4. Plot graph (court decisions against years) (exit figure to continue)")
            print("5. Plot graph (court decisions against courts) (exit figure to continue)")
            print("6. Plot graph (court decisions against areas of law) (exit figure to continue)")
            print("7. Exit to main menu")
            var = input('\nEnter action: ')
            if (var == '1') :
                seconds = timer(True)
                subprocess.call(['sh', cwd + '/Scripts/Shell_scripts/count_files.sh',OpenDataUitspraken])
                print("Seconds:",time.time()-seconds)
            elif (var == '2') :
                seconds = timer(True)
                subprocess.call(['python3','Scripts/check_structure.py',OpenDataUitspraken])
                print("Seconds:",time.time()-seconds)
            elif (var == '3') :
                seconds = timer(True)
                subprocess.call(['python3','Scripts/check_references.py',OpenDataUitspraken])
                print("Seconds:",time.time()-seconds)
            elif (var == '4') :
                subprocess.call(['python3','Visualization/plot_years.py',OpenDataUitspraken])
            elif (var == '5') :
                subprocess.call(['python3','Visualization/plot_courts.py',OpenDataUitspraken])
            elif (var == '6') :
                subprocess.call(['python3','Visualization/plot_areas.py',OpenDataUitspraken])
            elif (var == '7') :
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
            subprocess.call(['sh', cwd + '/Scripts/Shell_scripts/unpack.sh',OpenDataUitspraken])
            os.remove(OpenDataUitspraken_zip)
            print("Unzipping & unpacking succesful, zip has been removed")
        else :
            print("'" + OpenDataUitspraken + "' already exists, please delete first before unzipping again.\n")
main()