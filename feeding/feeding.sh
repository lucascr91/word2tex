cd ..
cd 2bib
output_path=$(pwd)
cd ..
cd feeding

python3 feeding.py $output_path

cd ..
cp 2bib/human_classified.csv to_bib/
cp 2bib/human_classified.csv wcit2bib/
cp 2bib/human_classified.csv feeding/