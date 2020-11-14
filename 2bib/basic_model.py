#!/usr/bin/env python
# coding: utf-8
print("Running k-neighborhood algorithm")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
#add path to import to_bib module
sys.path.append("/home/lucas/automata/to_bib")
from to_bib import *

os.chdir(sys.argv[1])

df = pd.read_csv('human_classified.csv')
df.rename({"tipo":"target"}, axis=1,inplace=True)
rep_target = {k:index for index,k in enumerate(df.target.unique())}
df.target.replace(rep_target, inplace=True)

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

scaler.fit(df.drop(["target","obra"], axis=1))
#std the data (knn don't work well when we have high heterogeneity of magnitudes among features)
scaled_features = scaler.transform(df.drop(["target","obra"],axis=1))

from sklearn.model_selection import train_test_split
X = scaled_features
y = df["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=101)

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=6)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

target_dict = {k: v for v, k in rep_target.items()}

def get_kind(entry):
    length_elements = len(entry.split(". "))
    length_string = len(entry)
    n_digit = n_char(entry, digit=True)
    f_slah = n_char(entry, char="/")
    parenthesis = n_char(entry, char="(")
    tab = pd.DataFrame({"length_elements": length_elements, "length_string": length_string,
                       "n_digit":n_digit, "f_slash":f_slah, "parenthesis":parenthesis}, index=[0])
    scaled_features = scaler.transform(tab)
    result = knn.predict(scaled_features)
    return target_dict[int(result)] 

user_df = pd.read_csv("references.csv")
user_df["tipo"] = [get_kind(k) for k in user_df["obra"]]
user_df.to_csv("machine_classified.csv", index=False)

print("Done")

