# 2bib


`2bib` is a command line tool to create bibtex files from a word document. Here we explain briefly how it works.

To create a bibtex file from your list of references you will need a word file containing only references in abnt style entries. It's likely that `2bib` works even for other bibliography style but keep in mind that `2bib` was primarily thought for input references that use the abnt standard. 

Once you have create a the `references.docx` file, save it and then open the terminal and type:

```bash
bash 2bib path/references.docx DEST
```

Where `path` is the location of docx file and `DEST` is the destination folder where you want to save the bibtex file (which is always name `references.bib`).