#!/usr/bin/env python
# coding: utf-8
print("Running k-neighborhood algorithm")
import pandas as pd
import numpy as np
import termplotlib as tpl
import seaborn as sns
import os
import sys
#add path to import to_bib module
sys.path.append("../to_bib")
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
number_nb=5
knn = KNeighborsClassifier(n_neighbors=number_nb)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

target_dict = {k: v for v, k in rep_target.items()}

t_names=[]

for k in np.unique(y_test):
    t_names.append(target_dict[k])

from sklearn.metrics import classification_report
print(classification_report(y_test, pred, target_names=t_names))

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

error_rate = []

for i in range(1,40):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train, y_train)
    pred_i = knn.predict(X_test)
    error_rate.append(np.mean(pred_i != y_test))

print("I'm using {} neighborhoods".format(str(number_nb)))
fig = tpl.figure()
fig.plot(range(1,40), error_rate)
fig.show()

print("Done")

