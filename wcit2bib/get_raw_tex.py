print("Creating a TEX file from the word document")
import docx
import sys
import os

try:
    doc = docx.Document(sys.argv[1])
except:
    raise ValueError("Please, add word document")

try:
    new_path=sys.argv[2]
except:
    raise ValueError("Please, add the target path")

try:
    number_chapter=sys.argv[3]
except:
    raise ValueError("Please, add the chapter number")

os.chdir(new_path)
#get paragraphs
all_paragraphs = doc.paragraphs
#remove empty paragraphs
paragraphs = [k for k in all_paragraphs if k.text!='']

#join paragraphs and add \par keyword
full_text = ''
for paragraph in paragraphs:
    if len(paragraph.text)>30:
        full_text = full_text + "\n" + "\par " + paragraph.text.strip() + "\n"
    else:
        name_section = "{"+paragraph.text.strip()+"}"
        full_text = full_text + "\n" + "\section{}".format(name_section) + "\n"

#create escapes for latex
full_text = full_text.replace("%","\%").replace("_","\_")
#add text to template
latex_template = "{}".format(full_text)

os.system("mkdir chapter{}".format(number_chapter))

f = open("chapter{0}/chapter{0}.tex".format(number_chapter), "w")
f.write(latex_template)
f.close()
print("Done")