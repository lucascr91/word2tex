print("Replacing word style citations for TEX style citations in text body")
import pandas as pd 
from colorama import Fore, Style
import os
import sys

os.chdir(sys.argv[1])
f = open("main.tex" ,"r")
tex = f.read()
f.close()

df=pd.read_csv("crossref.csv")

tex_dict={df["word_citation"][k]: df["best_match"][k] for k in range(len(df))}

for word, TEX in tex_dict.items():
    tex=tex.replace(word, TEX)

g = open("main.tex" ,"w")
g.write(tex)
g.close()

print("Done")
