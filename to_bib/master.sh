#!usr/bin/bash
path1=\2bib
path2=wcit2bib
path3=to_bib
RED='\033[0;31m'
NC='\033[0m' # No Color
echo "Checking if the automata sub-directories exists... "
if [ -d "$path1" ] && [ -d "$path2" ]
then
    echo "Ok"
elif ! [ -d "$path1" ]
then
    echo -e "${RED}ERROR: I cannot find $path1.${NC}"
    echo "Please, make sure you have 2bib, wcit2bib, and to_bib as sub-folders of the current directory"
    exit
elif ! [ -d "$path2" ]
then
    echo -e "${RED}ERROR: I cannot find $path2. ${NC}"
    echo "Please, make sure you have 2bib, wcit2bib, and to_bib as sub-folders of the current directory"
    exit
elif ! [ -d "$path3" ]
then
    echo -e "${RED}ERROR: I cannot find $path3.${NC}"
    echo "Please, make sure you have 2bib, wcit2bib, and to_bib as sub-folders of the current directory"
    exit
fi
ref_docx=$1
main_docx=$2
current_path=$(pwd)
#go to home dir
cd
#create output path
mkdir $3
#enter output path
cd $3
#get address
output_path=$(pwd)
#go to home dir
cd 
#back to working dir
cd $current_path
#enter
cd 2bib
#run 2bib
echo "Runing 2bib ..."
bash 2bib.sh $ref_docx $output_path
#back one dir
cd ..
#enter wcit
cd wcit2bib
echo "Running wcit2bib ..."
bash wcit2bib.sh $2 $output_path