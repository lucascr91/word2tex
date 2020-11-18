print("Replacing word style citations for TEX style citations in text body")
import pandas as pd 
from colorama import Fore, Style
import os
import sys
import re

try:
    new_path=sys.argv[1]
except:
    raise ValueError("Please, add the target path")

try:
    number_chapter=sys.argv[2]
except:
    raise ValueError("Please, add the chapter number")


os.chdir(new_path)

f=open("chapter{0}/chapter{0}.tex".format(number_chapter),"r")
tex = f.read()
f.close()

df=pd.read_csv("crossref.csv")

tex_dict={df["word_entry"][k]: df["best_match"][k] for k in range(len(df))}

for word, TEX in tex_dict.items():
    word_regex=r'{}'.format(word.translate(str.maketrans({"(":"\(", ")":"\)"," ":"\s?"})))
    TEX_regex=r'{}'.format(TEX.replace("\c","\\\c"))
    tex=re.sub(word_regex, TEX_regex,tex)

g = open("chapter{0}/chapter{0}.tex".format(number_chapter),"w")
g.write(tex)
g.close()

print("Done")