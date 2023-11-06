### python script for aggregating and modifying space deliminate txt files from UniDec and import into Scinamic

import shutil
import os
import time
from datetime import datetime
import pandas as pd
import numpy as np
from pathlib import Path
import csv

def unidecmass_format(path):

    # Make destination directory for formated mass files
    filenaming = datetime.now().strftime("%Y_%m_%d" + "_" + "%H%M%S")
    parent = os.path.dirname(path)
    targetDir = parent + "/" + filenaming + "_Scinamic_Import"
    os.mkdir(targetDir)

    reformat = 0
    ## AGGREGATE ALL UNIDEC GENERATED MASS LIST TXT FILES
    for root, dirs, files in os.walk((os.path.normpath(path)), topdown=False):
            for name in files:
                if name.endswith('mass.txt'):
                    print("\ncopying... " + name)
                    SourceFolder = os.path.join(root, name)
                    shutil.copy2(SourceFolder, targetDir)

                    print("formating... " + name)

                    df = pd.read_csv(targetDir + "/" + name, delimiter = " ", header = None)

                    # Add empty column
                    df1 = pd.DataFrame([[np.nan] * len(df.columns)], columns=df.columns)

                    # Add column headers     
                    df.columns = ['X(Daltons)','Y(Counts)']

                    #  # Add empty row
                    df.loc[0] = ""

                    # Grab the file name without the "_mass" text at end, removing last 9 characters
                    filename_new = name.replace("_mass.txt", "")

                     # Save new csv file to Sinamic Import folder
                    df.to_csv(targetDir + "/" + filename_new + ".csv")

                    # Count number of files processed
                    reformat= reformat + 1

                    # Delete text file
                    os.remove(targetDir + "/" + name)

    # Print confirmation of files processed
    print("\nNumber of files reformated for Scinamic: " + str(reformat))


print("This script groups UniDec 'mass.txt' files and reformats for Scinamic import.")

# Request file location
path = input("Enter UniDec data location: ")

unidecmass_format(path)

time.sleep(5)
