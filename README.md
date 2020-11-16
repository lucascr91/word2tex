# word2tex

This is a software whose main goal is to automatically convert monographies, dissertations and thesis from docx to LaTex. Currently, the software is based on two command line tools. The code for each of this tools can be found in folders **2bib** and **wcit2bib** in this repository. The first tool create a `bibtex` file from a list of references in a docx document. The second tool, named **wcit2bib**, export word style in text body citations to the same kind of entry in Latex. Both tools can work independently and more details on their working can be found in the respective folders.

It's easy to see that the two tools deal only with the problem of reference conversion. In the near future we will also add tools to make automatic the conversion of floats, like figures and tables. However, it's important to note that the current software version already supports the general formatting of document that includes cover, summary, page numbering, margins, and so on.

Although the each tool works separately, we create a bash file named `master.sh` whose function is run all tools in the right sequence and thus simplifying the user's work.

To run the whole software just type in command line:

```bash
bash master.sh references.docx main.docx DEST
```

Where `DEST`