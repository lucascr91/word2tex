#!usr/bin/bash
RED='\033[0;31m'
NC='\033[0m' # No Color
word_document=$1
current_path=$(pwd)

cd
#goes to selected directory
cd $2
#get selected directory path
output_path=$(pwd)
echo "Checking if references.bib is in $output_path ..."
if [[ -f references.bib ]]
then
    cp references.bib docx/
    echo "Ok"
else
    echo "I can't find the bibtex file in $output_path. Please, make sure you have ran 2bib before with $output_path as the target directory."
    exit
fi

cd $current_path
#create tex version from word doc
python get_raw_tex.py $word_document $output_path &&

#get word citations
python get_citations.py $output_path &&

#replace word citation for tex citations
python replace_wcitations.py $output_path &&

#add title_page for word document
python title_page.py $output_path

retVal=$?

if [[ $retVal -eq 0 ]]
then
    cd $output_path
    echo "Creating docx file"
    cd docx
    bash tex2word.sh
    cd ..
    echo "Removing redundant files"
    rm *csv
    echo "This step is finish. We just create a TEX file, replace the word citations for TEX citations and create a word document. Now you should compile the TEX files using standard TEX distributions (to get the PDF document)."

else
    echo -e "${RED}Some error occurred. TEX file not created and/or citations not replaced. Please, check warning and error messages above.${NC}"
    cd 
    rm -r $2
    exit 1
fi


