#########################
#This code create a database of references from a docx file

#author: Lucas Cavalcanti Rodrigues
#email: lucas.ecomg@gmail.com
#########################
print("I'm creating a reference csv file")
import docx
import sys
import re
import pandas as pd
import os
from tqdm import tqdm

try:
    doc = docx.Document(sys.argv[1])
except:
    raise ValueError("Please, add word document with a list of references")

#get paragraphs
all_paragraphs = doc.paragraphs
#remove empty paragraphs and get text of the no-empty
paragraphs = [k.text for k in all_paragraphs if k.text!='']

#here we assure that the list has only references starting with author's name
for index, paragraph in tqdm(enumerate(paragraphs)):
    if index>0:
        #if paragraph is not begining with author name
        if not re.match(r"^[A-Z-ÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]{2,}.+",paragraph):
            #then add it to the previous paragraph
            paragraphs[index-1] = paragraphs[index-1]+paragraphs[index]
            #and delete the current entry
            del paragraphs[index]

df = pd.DataFrame({"obra":paragraphs, "tipo":['']*len(paragraphs)})
os.chdir(sys.argv[2])
df.to_csv("references.csv", index = False)

print("Done")