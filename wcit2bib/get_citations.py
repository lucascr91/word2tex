print("Identifying word style citation in text body")
import re
import pickle as pkl
import numpy as np
import os
import sys
from colorama import Fore, Style
from fuzzywuzzy import process
import pandas as pd
from unidecode import unidecode

try:
    new_path=sys.argv[1]
except:
    raise ValueError("Please, add the target path")

os.chdir(new_path)

f = open("main.tex" ,"r")
tex = f.read()
f.close()

f=open("references.bib", "r")
bibtex=f.read()
f.close()

def get_tag(one):
    """
    Get @ tag from a bibtex entry
    """
    try:
        result=re.findall(r"[a-z]+[0-9]{4}[a-z]+",one)[0]
        return result
    except:
        print("Problem with: ")
        print(one)


def clean(name: pd.Series):
    """
    Normalize strings
    """
    cleaned = (name.apply(str.lower)
                .apply(unidecode)
                .apply(str.lower)
                .apply(lambda x: re.sub(r'[^\w\d]', '', x))
                )
    return cleaned

#citations of the kind (AUTHOR, 2009) or (AUTHOR, 2009; ACEMOGLU, 2011)
entries = re.findall(r"(\(?[A-Z]+,\s*[0-9]{4}[\);])", tex)

#get the list of bibtex entries
lista_bib = bibtex.split("\n\n")[:-1]

#get tags of each bibtex entry
tag_bib=[get_tag(k) for k in lista_bib]

df=pd.DataFrame({"word_entry":entries})
df.drop_duplicates(inplace=True)

#get best match of a entry in text among all bib entries
df["best_match"]=[process.extractOne(k,tag_bib)[0] for k in clean(df.word_entry)]
df["best_match"]=["\\cite{{{}}}".format(k) for k in df["best_match"]]

#merge several authors case
for index, entrie in enumerate(entries):
    if entrie[-1]==";":
        entries[index] = entries[index]+ " " +entries[index+1]
        entries.remove(entries[index+1])

citations=entries

def tagofmany(entries_many):
    """
    Get a dictionary of word (key) and latex (value) style citations for entries with many authors
    """
    n_entries=len(entries_many)
    new_tags=[]
    tuple_list=[]
    for k in range(n_entries):
        case = entries_many[k].split(';')
        lenght_case=len(case)
        authors=[]
        for m in range(lenght_case):
            if m==0:
                author=get_tag(df[df.word_entry==case[m]+")"]["best_match"].values[0])
                authors.append(author)
            elif m==lenght_case-1:
                author=get_tag(df[df.word_entry=="("+case[m].strip()]["best_match"].values[0])
                authors.append(author)
            else:
                author=get_tag(df[df.word_entry==case[m].strip()]["best_match"].values[0])
                authors.append(author)
        if (len(authors)==1) | (len(authors)==0):
            print(Fore.YELLOW+"WARNING: Cannot find more than one author in {}. Check function!".format(case))
            print("Here what I found: ")
            print(authors)
            print(Style.RESET_ALL)
        elif len(authors)==2:
            new_tag=r'{},{}'.format(*[get_tag(j) for j in authors])
            new_tags.append(new_tag)
        elif len(authors)==3:
            new_tag=r'{},{},{}'.format(*[get_tag(j) for j in authors])
            new_tags.append(new_tag)
        elif len(authors)==4:
            new_tag=r'{},{},{},{}'.format(*[get_tag(j) for j in authors])
            new_tags.append(new_tag)
        else:
            print(Fore.YELLOW+"WARNING: Too many authors in citation {}".format(case) + Style.RESET_ALL)
        new_tags=["\\cite{{{}}}".format(i) for i in new_tags]
        case_tuple=(entries_many[k],new_tags[0])
        tuple_list.append(case_tuple)
    return tuple_list

# new_entry="\\cite{{{}}}".format(new_tag)
more_authors=[k for k in citations if k.__contains__(";")]

new_entries=tagofmany(more_authors)
df=df.append(pd.DataFrame({"word_entry":[k[0] for k in new_entries],"best_match":[k[1] for k in new_entries]}))
df.reset_index(drop=True, inplace=True)
df["length_wentry"]=[len(k) for k in df.word_entry]
df.sort_values("length_wentry", ascending=False, inplace=True)

df.to_csv("crossref.csv", index=False)
