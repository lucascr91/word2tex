
print("Creating bibtex file")
import pandas as pd 
import os
from tqdm import tqdm
import sys
#add path to import to_bib module
sys.path.append("../to_bib")
from to_bib import *

os.chdir(sys.argv[1])

df = pd.read_csv("references.csv")

references = df.obra.to_list()
lista_bib=[Reference(**get_dict(reference)).bib() for reference in tqdm(references)]

f = open("references.bib", "w")
f.write("".join(lista_bib))
f.close()

print("Done")
