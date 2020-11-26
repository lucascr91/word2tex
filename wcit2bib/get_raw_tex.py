print("Creating a TEX file from the word document")
import docx
import sys
import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from docx.enum.text import WD_ALIGN_PARAGRAPH


try:
    doc = docx.Document(sys.argv[1])
except:
    raise ValueError("Please, add word document")

try:
    new_path=sys.argv[2]
except:
    raise ValueError("Please, add the target path")


def to_bold(text):
    return '\\textbf{{{}}} '.format(text)

def to_italic(text):
    return '\\textit{{{}}} '.format(text)

def to_underline(text):
    return '\\underline{{{}}} '.format(text)

def run_df(para):
    """
    Create a dataframe where each row is a run and the columns are boolean values informing if the run is bold, underline, italic etc.
    """
    df= pd.DataFrame({"run":[k.text for k in para.runs],"bold":[k.bold for k in para.runs],"italic":[k.italic for k in para.runs], "underline":[k.underline for k in para.runs]})
    df.replace({None:False}, inplace=True)
    df['latex']=[to_bold(df['run'][k]) if (df['bold'][k]==True) & (df['italic'][k]==False) & (df['underline'][k]==False) else df['run'][k] for k in df.index]
    df['latex']=[to_italic(df['run'][k]) if (df['bold'][k]==False) & (df['italic'][k]==True) & (df['underline'][k]==False) else df['latex'][k] for k in df.index]
    df['latex']=[to_underline(df['run'][k]) if (df['bold'][k]==False) & (df['italic'][k]==False) & (df['underline'][k]==True) else df['latex'][k] for k in df.index]
    df['latex']=[to_italic(to_bold(df['run'][k])) if (df['bold'][k]==True) & (df['italic'][k]==True) & (df['underline'][k]==False) else df['latex'][k] for k in df.index]
    df['latex']=[to_underline(to_bold(df['run'][k])) if (df['bold'][k]==True) & (df['italic'][k]==False) & (df['underline'][k]==True) else df['latex'][k] for k in df.index]
    df['latex']=[to_underline(to_italic(df['run'][k])) if (df['bold'][k]==False) & (df['italic'][k]==True) & (df['underline'][k]==True) else df['latex'][k] for k in df.index]
    df['latex']=[to_bold(to_underline(to_italic(df['run'][k]))) if (df['bold'][k]==True) & (df['italic'][k]==True) & (df['underline'][k]==True) else df['latex'][k] for k in df.index]
    return df

os.chdir(new_path)
#get paragraphs
all_paragraphs = doc.paragraphs
#remove empty paragraphs
paragraphs = [k for k in all_paragraphs if k.text!='']

alignment_values=[paragraph.paragraph_format.alignment for paragraph in paragraphs]

print("These are the paragraphs alignments")
for value in alignment_values:
    print(value)

# print("Center is regard as block citation")

#join paragraphs and add \par keyword
full_text = ''
for paragraph in tqdm(paragraphs):
    #is center align?
    if paragraph.paragraph_format.alignment==WD_ALIGN_PARAGRAPH.CENTER:
        df=run_df(paragraph)
        full_text = full_text + "\n" + "\\begin{{center}}\n{}\n\\end{{center}}".format(''.join(df['latex'].to_list()))+"\n"
    # elif is_block[paragraph]:
    #     full_text = full_text + "\n" + "\\begin{{citacao}}\n{}\n\\end{{citacao}}".format(paragraph.text)+"\n"
    else:
        df=run_df(paragraph)
        full_text = full_text + "\n" + "\par " + ''.join(df['latex'].to_list()) + "\n"
        
#create escapes for latex
full_text = full_text.replace("%","\%").replace("_","\_")
#add text to template
basic_template = "{}".format(full_text)

todoc_template = """
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

os.system("mkdir text")

f = open("text/text.tex", "w")
f.write(basic_template)
f.close()

f = open("docx/main.tex", "w")
f.write(todoc_template)
f.close()
print("Done")