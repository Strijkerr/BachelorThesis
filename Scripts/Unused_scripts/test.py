#!/usr/bin/python3
from lxml import etree
import os

def main () :
    cwd = os.getcwd()
    lidodata = cwd + "/DataSets/lidodata"
    aboutNone = 0
    count = 0 
    parser = etree.iterparse(lidodata, events=('start','end'))
    
    for event, element in parser: # Loop through lidodata
        about = element.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about') # The 'about' attribute represents the content of the node
        if (about == None) :
            aboutNone+=1
        elif ("https://linkeddata.overheid.nl/front/portal/component/get-document-with-refs" in about): # Filter for Dutch court cases
            print(about)
            for all in element :
                print(all.tag)
                print(all.text)
            count+=1
        element.clear() # Frees memory

    print(count)
main()
