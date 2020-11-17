
print("Creating bibtex file")
import pandas as pd 
import re
from colorama import Fore, Style
import os
from tqdm import tqdm
import sys
#add path to import to_bib module
sys.path.append("../to_bib")
from to_bib import *

os.chdir(sys.argv[1])

references_str = ""

df = pd.read_csv("machine_classified.csv")

references = df.obra.to_list()

not_found = []
titles = []
authors = []
years = []
for reference in references:
    try:
        year = re.findall(r"[\d]{4}",reference)[0]
    except:
        raise ValueError(Fore.RED + "I cannot find year in {}".format(reference) + Style.RESET_ALL)
    years.append(year)

for reference in tqdm(references):
    reference_list = reference.replace("\xa0", " ").split('. ')
    author = reference_list[0]
    author = title_format(author.strip())
    authors.append(author)
    title = reference_list[1]
    title = title_format(title.strip())
    titles.append(title)

df["author"] = authors
df["title"] = titles
df["year"] = years


lista_bib = [Reference(kind=df.tipo[k],
authors=[df.author[k]],
title=df.title[k],
year=df.year[k]).bib() for k in range(len(references))]

if sys.argv[2]=="basic":
    f = open("references.bib", "w")
    f.write("".join(lista_bib))
    f.close()
elif sys.argv[2]=="all":
    pass
else:
    raise ValueError(Fore.YELLOW + "Please, select the option regarding the completeness of the reference" + Style.RESET_ALL)

print("Done")
