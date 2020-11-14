#########################
#This code create a class of objects named Reference. Instances of this class are bibliographic references. The main class' method is self.bib which generates
# a bibtex entry for the instantiated reference.

#author: Lucas Cavalcanti Rodrigues
#email: lucas.ecomg@gmail.com
#########################


import warnings
from colorama import Fore, Style


def n_char(record:str, char="", digit=False):
    """
    This function get the number of characters of certain kind from a string
    """
    if digit or char!="":
        if digit:
            n = len([k for k in record if k.isdigit()])
        else:
            n = len([k for k in record if k==char])
    else:
        raise ValueError("Please select a character")
    return n


def title_format(name):
    """"
    This customized title function transform names in title format while keeping prepositions like "de" and "das" in lowercase
    """
    person_names = [k.title() if len(k)>3 else k for k in name.split(' ')]
    return ' '.join(person_names)

class Reference:
    def __init__(self, kind, authors: list, title, year, address = "", publisher = "", 
    journal = "", number="",pages="",month="", volume = "",series="",edition="",isbn="", subtitle="",howpublished = "",
    school = "", organization = "", chapter = "", booktitle = ""):
        self.authors = authors
        self.title = title
        self.address = address
        self.publisher = publisher
        self.year = year
        self.kind = kind
        self.journal = journal
        self.number = number
        self.pages = pages
        self.month = month
        self.volume = volume
        self.serie = series
        self.edition = edition
        self.isbn = isbn
        self.subtitle = subtitle
        self.howpublished = howpublished
        self.school = school
        self.organization = organization
        self.chapter = chapter
        self.booktitle = booktitle

    def author_tag(self, n=0):
        """
        Get authors tag based on index (0 is first author, 1 is the second author and so on)
        """
        names = self.authors[n].split(' ')
        #if the second name starts with something like "de" or "das"
        if len(names[0])<=3:
            names[0] = names[0] + names[1]
        else:
            pass

        return names[0].lower()
    
    def filled(self):
        """
        Get a list of the arguments that were filled
        """
        return [k for k in self.__dict__.keys() if len(self.__dict__[k])!=0]


    def bib(self):
        """
        Create a bibtex entry
        """
        #create list of strings with elements like "title = The Black Swan", except for "kind" and "authors"
        list_bib = ["{0} = {{{1}}}, \n".format(k,self.__dict__[k]) for k in self.filled() if (k!="kind") & (k!="authors")]
        #create authors element (of course, there is a clever way to do this, but I'm tired now)
        if len(self.authors)==1:
            str_authors = "{{{}}}, \n".format(self.authors[0])
            str_authors = "author = " + str_authors
        elif len(self.authors)==2:
            str_authors = "{{{}}} and {{{}}}, \n".format([name for name in self.authors])
            str_authors = "author = " + str_authors
        elif len(self.authors)==3:
            str_authors = "{{{}}} and {{{}}}  and {{{}}}, \n".format([name for name in self.authors])
            str_authors = "author = " + str_authors
        elif len(self.authors)==4:
            str_authors = "{{{}}} and {{{}}}  and {{{}}} and {{{}}}, \n".format([name for name in self.authors])
            str_authors = "author = " + str_authors
        elif len(self.authors)==5:
            str_authors = "{{{}}} and {{{}}}  and {{{}}} and {{{}}} and {{{}}}, \n".format([name for name in self.authors])
            str_authors = "author = " + str_authors
        else:
            warnings.warn(Fore.YELLOW + "There are more than 5 authors here. Please entry \"{}\" manually".format(self.title) + Style.RESET_ALL, WARNING)
            str_authors = "author = a lot, \n"
        #create tag (tag are elements like @book{taleb2007black,})
        tag_title = self.title.split(' ')[0].lower()
        if len(self.authors)==1:
            tag = "@{0}{{{1}{2}{3},\n".format(self.kind, self.author_tag(0),self.year,tag_title)
        elif len(self.authors)==2:
            tag = "@{0}{{{1}{2}{3}{4},\n".format(self.kind, self.author_tag(0), self.author_tag(1),self.year,tag_title)
        else:
            tag = "@{0}{{{1}atal{2}{3},\n".format(self.kind, self.author_tag(0),self.year,tag_title)
        #add tag to list
        tag = tag.replace(",","").replace("\n","")+",\n"
        list_bib.insert(0,tag)
        list_bib.insert(1,str_authors)
        list_bib[-1] = list_bib[-1].replace(", \n","\n} \n\n")

        return "".join(list_bib)

    def __repr__(self):
        return self.title
    
    def __str__(self):
        return self.title

class WARNING(UserWarning):
    pass