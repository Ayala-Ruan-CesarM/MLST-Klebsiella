#!/bin/bash

#Gene resistance prediction on Klebsiella with abricate 
list=("argannot" "ecoh" "plasmidfinder" "ecoli_vf" "card" "resfinder" "ncbi" "megares" "vfdb" )
output_file="Klebsiella_all_"
input="*.fna"
for item in "${list[@]}" ; do 
    abricate --threads 20 --nopath --db $item $input > "${output_file}${item}".tsv
done

# Concatenate output and clean the file, no double headers
cat *.tsv > Klebsiella_all_dbs.tab
awk '/^#FILE/ && count++ > 0 {next} 1' Klebsiella_all_dbs.tab > Klebsiella_all_dbs_clean.tab

# Python script to remove duplicate gene annotations 

python Remove_duplicates_v2.py -i Klebsiella_all_dbs_clean.tab -o Klebsiella_all_dbs_clean_No_duplicates.tab

sed -i 's/(bla)//g' Klebsiella_all_dbs_clean_No_duplicates.tab

abricate --summary Klebsiella_all_dbs_clean_No_duplicates.tab > Klebsiella_all_dbs_clean_No_duplicates.tsv 


# Get metadata type material
datasets summary genome accession GCA_000163455 GCA_000215745 GCA_000281755 GCA_000613225 GCA_000614665 GCA_000742135 GCA_000751755 \
GCA_000788015 GCA_000826585 GCA_000828055 GCF_001590945 GCF_001598695 GCF_001598715 GCA_002269255 GCA_002925905 GCA_003261575 \
GCA_003417445 GCA_005860775 GCA_006364295 GCA_006711645 GCA_009173485 GCA_017638945 GCA_019048125 GCA_020099175 GCA_020115495 \
GCA_020115515 GCA_020115535 GCA_020115545 GCA_020525545 GCA_020525685 GCA_020525925 GCA_020526085 GCA_022869665 GCA_900200035 \
GCA_900452045 GCA_900452125 GCA_900461485 GCA_900635435 GCA_900636985 GCA_900978195 GCA_900978845 GCA_902158555 GCA_902158725 \
--as-json-lines > Metadata_typematerial.json

# Get metadata COL
datasets summary genome accession GCA_002119865.1 GCA_002851415.1 GCA_002851635.1 GCA_018208605.1 GCA_013169455.1 GCA_002854775.1 \
GCA_002855225.1 GCA_002853615.1 GCA_002853635.1 GCA_002853675.1 GCA_002853695.1 GCA_002853875.1 GCA_002851315.1 GCA_002851595.1 \
GCA_002855355.1 GCA_002855425.1 GCA_002855095.1 GCA_002853745.1 GCA_002851075.1 GCA_002851085.1 GCA_002851235.1 GCA_002851295.1 \
GCA_002854595.1 GCA_002854795.1 GCA_002854535.1 GCA_013169665.1 GCA_013169715.1 GCA_013169755.1 GCA_002119945.1 --as-json-lines > Metadata_Col.json

# Then used python script to convert json files tab files
