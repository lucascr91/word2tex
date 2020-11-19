#!usr/bin/bash
RED='\033[0;31m'
NC='\033[0m' # No Color
current_path=$(pwd)
cd
cd $2
output_path=$(pwd)
cd $current_path
cp human_classified.csv $output_path
#create a csv file from references docx
python references2csv.py $1 $output_path &&
#create features dataset from list of references
python create_features.py $output_path &&
#classify references using k-neighborhoods algorithm
python basic_model.py $output_path &&
#create a bibtex file
python get_bib.py $output_path basic
retVal=$?

if [[ $retVal -eq 0 ]]
then
    echo "Removing redundant files from target directory."
    cd $output_path
    rm *csv
    echo "Done"
    echo "This step is finish. We just create a bibtex file. Now you should run wcit2bib to transform the word body text citations in TEX citations."
else
    echo -e "${RED}Some error occurred. Bibtex file not created. Please, check warning and error messages above.${NC}"
    cd
    rm -r $output_path
    exit 1
fi
