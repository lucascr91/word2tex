print("Creating citations database")

import pandas as pd 
import re
import pickle as pkl 
from fuzzywuzzy import process
import os
import sys


os.chdir(sys.argv[1])

f=open("references.bib", "r")
bibtex=f.read()
f.close()

def get_tag(one):
    try:
        result=re.findall(r"[a-z]+\d{4}[a-z]+",one)[0]
        return result
    except:
        print("Problem with: ")
        print(one)


with open('citations.pkl', 'rb') as handle:
    citations = pkl.load(handle)

#get the list of bibtex entries
lista_bib = bibtex.split("\n\n")[:-1]

tag_bib=[get_tag(k) for k in lista_bib]

tag_text = [k.lower().replace(",","") for k in citations]

citations=["("+citation.replace(",",", ")+")" for citation in citations]

# for citation in citations:
#     print(citation)

df=pd.DataFrame({"word_citation":citations, "tag_text": tag_text})

#get best match of a entry in text among all bib entries
df["best_match"]=[process.extractOne(k,tag_bib)[0] for k in tag_text]
df["best_match"]=["\\cite{{{}}}".format(k) for k in df["best_match"]]


df.drop("tag_text", axis=1,inplace=True)
df.to_csv("crossref.csv", index=False)

print("Done")