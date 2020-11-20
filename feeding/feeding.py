import pandas as pd 
import numpy as np
import os
import sys
sys.path.append("../to_bib")
from to_bib import *

try:
    new_path=sys.argv[1]
except:
    raise ValueError("Please, add the target path")

os.chdir(new_path)

df=pd.read_csv("human_classified.csv")

while True:
    entry=input("Please, give me the entry: ")
    label=input("Now the kind: ")
    print("adding ...")

    df.drop(['length_elements', 'length_string', 'n_digit', 'f_slah','parenthesis'], axis=1, inplace=True)

    df=df.append(pd.DataFrame({"obra":entry, "tipo":label}, index=[0])).reset_index(drop=True)

    df["length_elements"] = [len(k.split(". ")) for k in df["obra"]]
    df["length_string"] = [len(k) for k in df["obra"]]
    df["n_digit"] = [n_char(k, digit=True) for k in df["obra"]]
    df["f_slah"] = [n_char(k, char="/") for k in df["obra"]]
    df["parenthesis"] = [n_char(k, char="(") for k in df["obra"]]
    answer=input("Do you want to continue? (press q to quit)")
    if answer=='q':
        break
    else:
        continue

df.to_csv("human_classified.csv", index=False)

print(df.tail())
print("I just saved the new entry. If you want to undo it, just open the file and drop the appropriate rows.")
