### python script for aggregating and modifying space deliminate txt files from UniDec and import into Scinamic
import shutil
import os
import time
from datetime import datetime
import pandas as pd
import numpy as np
from pathlib import Path
import csv


RootDir1 = input("Enter UniDec Data Location: ")

# MAKE DIR TO STORE MASS FILES AND FORMATED FILES
filenaming = datetime.today().strftime("%Y_%m_%d")
if not os.path.exists(filenaming + "_UniDec_mass"):
    os.mkdir(filenaming + "_UniDec_mass")
if not os.path.exists(filenaming + "_Scinamic_Import"):
    os.mkdir(filenaming + "_Scinamic_Import")
targetDir1 = (filenaming + "_UniDec_mass")
targetDir2 = (filenaming + "_Scinamic_Import")

## AGGREGATE ALL UNIDEC GENERATED MASS LIST TXT FILES
for root, dirs, files in os.walk((os.path.normpath(RootDir1)), topdown=False):
        for name in files:
            if name.endswith('mass.txt'):
                print("moving... " + name)
                SourceFolder = os.path.join(root, name)
                shutil.copy2(SourceFolder, targetDir1) #copies csv to new folder

# REFORMAT MASS LIST TXT FILES TO SCINAMIC COMPATIBLE FORMAT
reformat = 0
for filename in os.listdir(targetDir1):
    if filename.endswith(".txt"):
        print("formating..." + filename)
        df = pd.read_csv(targetDir1 + "/" + filename, delimiter = " ", header = None)
        
        # Add empty column
        df1 = pd.DataFrame([[np.nan] * len(df.columns)], columns=df.columns)
        
        # Add two empty rows
        for i in range(1): 
             df = df1.append(df, ignore_index=True)

        # Add column headers     
        df.columns = ['X(Daltons)','Y(Counts)']

        # Grab the file name without the "_mass" text at end, removing last 9 characters
        filename_new = filename.replace("_mass", "")
        print(filename_new)
    
        # Save new csv file to Sinamic Import folder
        df.to_csv(targetDir2 + "/" + filename_new + ".csv")

        # Count number of files processed
        reformat= reformat + 1

# Print confirmation of files processed
print("\nNumber of files reformated for Scinamic: " + str(reformat))
time.sleep(5)
