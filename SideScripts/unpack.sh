#!/bin/sh
# This script unzips all files in the 'OpenDataUitspraken' folder so that 
# we are left with just one folder with all court decisions.
# Run this outside the "OpenDataUitspraken" folder.
# This script can be run by typing: "sh unpack.sh OpenDataUitspraken"
foldername=$1
rm -rf $foldername/2016/201601 # Removes random folder that is the only non-zipped folder
rm $foldername/info.txt # Removes info.txt, this contains .
find $foldername -name \*.zip -exec unzip -d $foldername {} \; # Unzips all zipped folders.
rm -r $foldername/*/ # Removes all folders that contained the zipped folders.
#After running this script, this script can be removed.