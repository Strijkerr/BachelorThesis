#!/usr/bin/python3
import time
from lxml import etree

seconds = time.time()

file = "lidodata"
folder = "/home/jonathan/Desktop/"

try :
    parser = etree.iterparse(folder + file, events=('start','end'))
    try :
        count = 0
        for event, element in parser:
            about = element.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about')
            if (about != None):
                count = count + 1
            element.clear()
    except Exception as e:
        print(e)
except Exception as e:
    print(e)
print(count)
print("Seconds:",time.time()-seconds)