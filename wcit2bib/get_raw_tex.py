print("Creating a TEX file from the word document")
import docx
import sys
import os

try:
    doc = docx.Document(sys.argv[1])
except:
    raise ValueError("Please, add word document")

os.chdir(sys.argv[2])
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
latex_template = """
\\documentclass{{report}}
\\usepackage[utf8]{{inputenc}}

\\usepackage[portuguese]{{babel}}
\\usepackage[autostyle,portuguese=brazilian]{{csquotes}}

\\usepackage[
backend=biber,
style=alphabetic,
sorting=ynt
]{{biblatex}}
\\addbibresource{{references.bib}}

\\begin{{document}}

\\input{{title_page}}

{}

\\printbibliography

\\end{{document}}


""".format(full_text)

f = open("main.tex", "w")
f.write(latex_template)
f.close()
print("Done")