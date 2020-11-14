print("Identifying word style citation in text body")
import re
import pickle as pkl
import numpy as np
import os
import sys
from colorama import Fore, Style

os.chdir(sys.argv[1])

f = open("main.tex" ,"r")
tex = f.read()
f.close()

citations = re.findall(r"([A-Z]+,)\s*([0-9]{4})", tex)
#get unique
citations = np.unique([k[0].strip()+k[1].strip() for k in citations])

if len(citations)>0:
    pass
else:
    raise ValueError(Fore.RED + "I cannot find any citations. Please, check the document and/or the regex" + Style.RESET_ALL)

#save citations as a list
pkl.dump(citations, open('citations.pkl', 'wb'))

print("Done")
