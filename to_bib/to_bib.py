#!/usr/bin/env python
# coding: utf-8

#########################
#This code create a class of objects named Reference. Instances of this class are bibliographic references. The main class' method is self.bib which generates
# a bibtex entry for the instantiated reference.

#author: Lucas Cavalcanti Rodrigues
#email: lucas.ecomg@gmail.com
#########################
import pandas as pd
import numpy as np
import os
import sys
import warnings
from colorama import Fore, Style
import re
from fuzzywuzzy import process

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
number_nb=28
knn = KNeighborsClassifier(n_neighbors=number_nb)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

target_dict = {k: v for v, k in rep_target.items()}

t_names=[]

for k in np.unique(y_test):
    t_names.append(target_dict[k])

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

def get_authors(entry):
    elements=entry.replace("\xa0", " ").split('. ')
    return [k for k in elements[0].split(';')]


def get_title(entry):
    elements=entry.replace("\xa0", " ").split('. ')
    try:
        if len(elements[1])>2:
            return elements[1]
        elif len(elements[2])>2:
            return elements[2]
        elif len(elements[3])>2:
            return elements[3]
        else:
            return ''
    except:
        return ''
        

def get_year(entry):
        try:
            years=re.findall(r'[0-9]{4}\.',entry)
            if len(years)==1:
                return years[0][:-1]
            else:
                return years[-2][:-1]
        except:
            return ''

def get_address(entry):
    try:
        candidates=re.findall(r'\. [A-Z][a-z]+[^:]+',entry)[0].split('. ')
        #the address is given by the candidate whose value is different from title
        address=[k for k in candidates if (k!=process.extractOne(get_title(entry),candidates)[0]) & (k!='')]
        if len(address)==1:
            return address[0]
        else:
            return ''
    except:
        return ''

def get_publisher(entry):
    address=get_address(entry)
    if address!='':
        try:
            query=r'{}[^\.,]+'.format(address)
            candidate=re.findall(query, entry)[0]
            publisher=candidate.replace(address,'').replace(':','')
            return publisher.strip()
        except:
            return ''
    else:
        return ''

    

def get_dict(entry):
    dict_args={}
    dict_args["kind"]=get_kind(entry)
    dict_args["authors"]=get_authors(entry)
    dict_args["title"]=get_title(entry)
    dict_args["year"]=get_year(entry)
    dict_args["address"]=get_address(entry)
    dict_args["publisher"]=get_publisher(entry)

    return dict_args


def n_char(record:str, char="", digit=False):
    """
    This function get the number of characters of certain kind from a string
    """
    if digit or char!="":
        if digit:
            n = len([k for k in record if k.isdigit()])
        else:
            n = len([k for k in record if k==char])
    else:
        raise ValueError("Please select a character")
    return n


def title_format(name):
    """"
    This customized title function transform names in title format while keeping prepositions like "de" and "das" in lowercase
    """
    person_names = [k.title() if len(k)>3 else k for k in name.split(' ')]
    return ' '.join(person_names)

class Reference:
    def __init__(self, kind, authors: list, title, year, address = "", publisher = "", 
    journal = "", number="",pages="",month="", volume = "",series="",edition="",isbn="", subtitle="",howpublished = "",
    school = "", organization = "", chapter = "", booktitle = ""):
        self.authors = authors
        self.title = title
        self.address = address
        self.publisher = publisher
        self.year = year
        self.kind = kind
        self.journal = journal
        self.number = number
        self.pages = pages
        self.month = month
        self.volume = volume
        self.serie = series
        self.edition = edition
        self.isbn = isbn
        self.subtitle = subtitle
        self.howpublished = howpublished
        self.school = school
        self.organization = organization
        self.chapter = chapter
        self.booktitle = booktitle

    def author_tag(self, n=0):
        """
        Get authors tag based on index (0 is first author, 1 is the second author and so on)
        """
        names = self.authors[n].split(' ')
        #if the second name starts with something like "de" or "das"
        if len(names[0])<=3:
            names[0] = names[0] + names[1]
        else:
            pass

        return names[0].lower()
    
    def filled(self):
        """
        Get a list of the arguments that were filled
        """
        return [k for k in self.__dict__.keys() if len(self.__dict__[k])!=0]


    def bib(self):
        """
        Create a bibtex entry
        """
        #create list of strings with elements like "title = The Black Swan", except for "kind" and "authors"
        list_bib = ["{0} = {{{1}}}, \n".format(k,self.__dict__[k]) for k in self.filled() if (k!="kind") & (k!="authors")]
        #create authors element (of course, there is a clever way to do this, but I'm tired now)
        if len(self.authors)==1:
            str_authors = "{{{}}}, \n".format(self.authors[0])
            str_authors = "author = " + str_authors
        elif len(self.authors)==2:
            str_authors = "{{{} and {}}}, \n".format(*[name for name in self.authors])
            str_authors = "author = " + str_authors
        elif len(self.authors)==3:
            str_authors = "{{{} and {}  and {}}}, \n".format(*[name for name in self.authors])
            str_authors = "author = " + str_authors
        elif len(self.authors)==4:
            str_authors = "{{{} and {}  and {} and {}}}, \n".format(*[name for name in self.authors])
            str_authors = "author = " + str_authors
        elif len(self.authors)==5:
            str_authors = "{{{} and {}  and {} and {} and {}}}, \n".format(*[name for name in self.authors])
            str_authors = "author = " + str_authors
        else:
            warnings.warn(Fore.YELLOW + "There are more than 5 authors here. Please entry \"{}\" manually".format(self.title) + Style.RESET_ALL, WARNING)
            str_authors = "author = a lot, \n"
        #create tag (tag are elements like @book{taleb2007black,})
        tag_title = self.title.split(' ')[0].lower()
        if len(self.authors)==1:
            tag = "@{0}{{{1}{2}{3},\n".format(self.kind, self.author_tag(0),self.year,tag_title)
        elif len(self.authors)==2:
            tag = "@{0}{{{1}{2}{3}{4},\n".format(self.kind, self.author_tag(0), self.author_tag(1),self.year,tag_title)
        else:
            tag = "@{0}{{{1}atal{2}{3},\n".format(self.kind, self.author_tag(0),self.year,tag_title)
        #add tag to list
        tag = tag.replace(",","").replace("\n","")+",\n"
        list_bib.insert(0,tag)
        list_bib.insert(1,str_authors)
        list_bib[-1] = list_bib[-1].replace(", \n","\n} \n\n")

        return "".join(list_bib)

    def __repr__(self):
        return self.title
    
    def __str__(self):
        return self.title

class WARNING(UserWarning):
    pass