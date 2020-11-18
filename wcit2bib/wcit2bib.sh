#!usr/bin/bash
RED='\033[0;31m'
NC='\033[0m' # No Color
word_document=$1
current_path=$(pwd)
number_chapter=$3

cd
#goes to selected directory
cd $2
#get selected directory path
output_path=$(pwd)
echo "Checking if references.bib is in $output_path ..."
if [[ -f references.bib ]]
then
    echo "Ok"
else
    echo "I can't find the bibtex file in $output_path. Please, make sure you have ran 2bib before with $output_path as the target directory."
    exit
fi

cd $current_path
#create tex version from word doc
python get_raw_tex.py $word_document $output_path $number_chapter&&

#get word citations
python get_citations.py $output_path $number_chapter&&

#replace word citation for tex citations
python replace_wcitations.py $output_path $number_chapter
retVal=$?

echo "Removing redundant files"
cd $output_path
rm *csv

if [[ $retVal -eq 0 ]]
then
    echo "This step is finish. We just create a TEX file and replace the word citations for TEX citations. Now you should compile the TEX files using standard TEX distributions (to get the PDF document) or pandoc (to get a Word document)."
else
    echo -e "${RED}Some error occurred. TEX file not created and/or citations not replaced. Please, check warning and error messages above.${NC}"
fi


