#!/usr/bin/env python
# coding: utf-8

print("Creating features for k-neighborhood algorithm from input references")
import pandas as pd
import re
import os
import sys
#add path to import to_bib module
sys.path.append("../to_bib")
from to_bib import *

# df=pd.read_csv("human_classified.csv")

# df["length_elements"] = [len(k.split(". ")) for k in df["obra"]]
# df["length_string"] = [len(k) for k in df["obra"]]
# df["n_digit"] = [n_char(k, digit=True) for k in df["obra"]]
# df["f_slah"] = [n_char(k, char="/") for k in df["obra"]]
# df["parenthesis"] = [n_char(k, char="(") for k in df["obra"]]

# df.to_csv("human_classified.csv", index=False)

os.chdir(sys.argv[1])
df = pd.read_csv("references.csv")

df["length_elements"] = [len(k.split(". ")) for k in df["obra"]]
df["length_string"] = [len(k) for k in df["obra"]]
df["n_digit"] = [n_char(k, digit=True) for k in df["obra"]]
df["f_slah"] = [n_char(k, char="/") for k in df["obra"]]
df["parenthesis"] = [n_char(k, char="(") for k in df["obra"]]

df.to_csv("features.csv", index=False)
print("Done")
