from colorama import Fore, Style
#add path to import to_bib module
import sys
sys.path.append("../to_bib")
from to_bib import *
import sys
import os

os.chdir(sys.argv[1])

answer=input(Fore.YELLOW + "Do you want to add custom information in the title fields? (y/n) \n"+Style.RESET_ALL)
a=True
while a==True:
    try:
        if answer[0].lower()=="y":
            print(Fore.YELLOW + "Now we will create the title page. We are going to ask you to fill the information that should appear in cover page, if you want to let some information blank, just click enter to skip to the ne3xt field.")
            print("Please, fill the following information: ")
            institution=input("Institution's name: "+Style.RESET_ALL)
            college=input(Fore.YELLOW +"College: "+Style.RESET_ALL)
            department=input(Fore.YELLOW +"Department: "+Style.RESET_ALL)
            program=input(Fore.YELLOW +"Program: "+Style.RESET_ALL)
            author=input(Fore.YELLOW +"Author's name: "+Style.RESET_ALL)
            title=input(Fore.YELLOW +"Title: "+Style.RESET_ALL)
            city=input(Fore.YELLOW +"City: "+Style.RESET_ALL)
            year=input(Fore.YELLOW +"Year: "+Style.RESET_ALL)
            a=False
        elif answer[0].lower()=="n":
            print(Fore.YELLOW + "Ok. We are going to use the default information"+Style.RESET_ALL)
            institution="University of London"
            college="Faculty of Economics and Business"
            department="Department of Economics"
            program="Foreign Affairs Graduate School"
            author="Alexander Papadoulos"
            title="Soviet industrial production in stalinist era"
            city="London"
            year="2021"
            a=False
    except:
        print("Select a valid option, please.")
        answer=input(Fore.YELLOW + "Do you want to add custom information in the title fields? (y/n) \n"+Style.RESET_ALL)


meta=[institution,college,department,program,author,title,city,year]
meta=[k.upper() if (k!=author) & (k!=title) & (k!=city) else title_format(k) for k in meta]

title_page = """
\\begin{{titlepage}}
    \\begin{{center}}
        % \\vspace*{{1cm}}
        \\Large
        {{{0}}}
        \par
        {{{1}}}
        \par
        \\Large
        {{{2}}} \\\\
        {{{3}}}

       \\vspace{{3.5cm}}
       \\uppercase{{{4}}}    
       \\vspace{{2.5cm}}
            
       \\textbf{{{5}}}
            
       \\vfill
                   
        \\vspace{{1.8cm}}
            
            
        \\large
        {6}\\
        {7}
    \\end{{center}}
\\end{{titlepage}}
""".format(meta[0],meta[1],meta[2],meta[3],meta[4],meta[5],meta[6],meta[7])

f=open("docx/title_page.tex", "w")
f.write(title_page)
f.close()


