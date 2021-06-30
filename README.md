# BachelorThesis
Code for bachelor thesis project 2020/2021 by Jonathan Strijker

For more information about this project, see the full thesis at: "https://theses.liacs.nl/xxxxxxxxxxx"

This project requires 29+36GB of free space as it has to download big datasets from external sources.

Several libraries might be needed to run everything, terminal should signal which ones might be missing.

For opening this project in Visual Studio Code or any other IDE with a file tracker, add '**/OpenDataUitspraken/**' to the 'watcher exclude' (too many files to track otherwise). However, project sometimes still unstable in Visual Studio Code if the 'OpenDataUitspraken' dataset has not yet been slimmed down. 

TIP: the datasets used in this project contain > 2.8 million files. After deleting those after one is done using this project, emptying the trash folder through the user interface in linux might be buggy. Using the 'trash-empty' command in terminal from the trash-cli (sudo apt install trash-cli) library is a possible solution to this problem.

**SETUP**

If running for the first time, git clone this project in your map of choice by typing this in the terminal:
1. git clone "https://github.com/Kroonkurk/BachelorThesis.git"

When the cloning is complete, go to the working directory 'BachelorThesis'.

2. cd BachelorThesis 

Launch 'menu.py' from the working directory to go through the steps of setting up the datasets. Launching can be done by typing the following in the terminal:

3. python3 menu.py

'1' Should be pressed to enter the setup menu.

4. 1

From the setup menu you can download the dataset by entering '1'. You can unzip and unpack it with '2'. 

After going through these steps, one can exit the 'setup menu' by pressing '3'. 

5. 1

6. 2

7. 3

One can then go to the edit 'OpenDataUitspraken' menu by pressing '2' in the main menu.

8. 2

From the edit menu, one can remove the court decisions that are without abstract and without judgment from the dataset. One can go back to the main menu by pressing '2'.

9. 1

10. 2

From the main menu, one can choose to open the 'OpendataUitspraken' tools to use certain tools on the dataset.

11. 3

From this menu, one can use tools to see certain characteristics about the dataset.

<!-- At this point, the datasets should be ready for visualization & analysis -->

One can end the program by pressing '4' in the main menu.

12. 4
