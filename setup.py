#!/usr/bin/python3
# Source: https://stackoverflow.com/questions/37573483/progress-bar-while-download-file-over-http-with-requests
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

def unzip () :
    var = input("Type 'yes' to unzip: ")
    if (var == 'yes') :
        print("Unzipping")
        subprocess.call(['unzip',folder_zip,'-d',folder])
        #subprocess.call(['sh', cwd + '/SideScripts/unpack.sh',folder_zip])
    else :
        print("No action")

if not os.path.exists(folder) :
    if not os.path.exists(folder_zip) :
        print("'" + folder_zip + "' does not exist yet")
        val = input("Download 'Open Data van de Rechtspraak manually from https://www.rechtspraak.nl/Uitspraken/paginas/open-data.aspx\n"
        "or type: 'yes' to download dataset (~5.4GB zipped, ~24GB unzipped) from '" + url + "'\n")
        if (val == "yes") :
            response = requests.get(url, stream=True)
            total_size_in_bytes= int(response.headers.get('content-length', 0))
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
                    f.write("Date of download 'OpenDataUitspraken': " + today + '\n')
                unzip()
        else :
            print("No action")
    else :
        print("'" + folder + ".zip'" + " already exists")
        unzip()
else :
    print("Dataset exists")