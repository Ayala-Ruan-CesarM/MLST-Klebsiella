# MLST-Klebsiella
Code used for a MLST for Klebsiella proyect in colaboration with Paredes-Amaya Claudia (U.Valle, Colombia) and Sánchez-Reyes Ayixon (IBT.UNAM, Mexico)


Requiere:

Obtain current complet current path directory in linux OS with
``` 
pwd
``` 

for example /your/current/directory

Then, execute the script Preprocess_genomes.sh 
``` 
bash Preprocess_genomes.sh /your/current/directory
``` 
It will download all genomes used in the current MLST to the current directory 
Once this step is completed, you can run the Process_and_Align.sh script if all the sanger sequences used are also in current directory
The script also requires the current directory direction as input

``` 
bash Process_and_Align.sh /your/current/directory
``` 
Once MAFFT and TrimAl finished, it is highly encouraged to double check aligments in a software like Seaview
As the next steps are manually conducted.

In Seaview open each aligments and use the Seaview function concatenated by ranks as it will be order by rank

Save the result concateneted aligment which will be used for phylogenetic tree reconstruction with IQ-Tree2
It is also encourage to move the concatenated aligment to and individual folder in this case called "Tree"

``` 
iqtree2 -s Tree/Concatenate_All_sevenGenes.fasta -B 1000 -alrt 1000
```
Finally, speciation test (bPTP and ASAP) were conducted with windowns executables 

# Resitance gene search

First will need to downdload the genomes for K. variicola and quasipneumonaie found in Colombia (see methods article)

``` 
datasets download genome accession GCA_002119865.1 GCA_002851415.1 GCA_002851635.1 GCA_018208605.1 GCA_013169455.1 GCA_002854775.1 \
GCA_002855225.1 GCA_002853615.1 GCA_002853635.1 GCA_002853675.1 GCA_002853695.1 GCA_002853875.1 GCA_002851315.1 GCA_002851595.1 \
GCA_002855355.1 GCA_002855425.1 GCA_002855095.1 GCA_002853745.1 GCA_002851075.1 GCA_002851085.1 GCA_002851235.1 GCA_002851295.1 \
GCA_002854595.1 GCA_002854795.1 GCA_002854535.1 GCA_013169665.1 GCA_013169715.1 GCA_013169755.1 GCA_002119945.1 
```
Extract the genomes and send files to working directory
```
#unzip the file
unzip ncbi_dataset.zip
#copy genome files to current working folder 
find . -name *.fna -exec cp {} "$PATH" \;
``` 
Assuming all genomes files (type material and Colombian genomes) are on the same directory,
that [abricate](https://github.com/tseemann/abricate.git) and [ncbi datasest](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/command-line-tools/download-and-install/) are installed and executable and that "Remove_duplicates.py" is on the working dir then run:
```
bash Resistance.sh
```
That bash command will do: 
1) Predict resistance genes   all genomes
2) Execute the script Remove_duplicates.py
3) Create metadata tables from ncbi genome information

Once finised, covert the json files created "Metadata_typematerial.json" and "Metadata_Col.json" to tab separeted files
using the python script "convertjson.py" changing manually the input and output file names with the favorite text editor. 

As mentioned in the methods secction the output file from abricate "Klebsiella_all_dbs_clean_No_duplicates.tsv" went over manual revision before plotting
and data from "KP" isolations were added to the final data. 

# Plots generation 

You will need to have the "NEW_Anex_2.txt" table from article supplementary data then run:
```
python heatmap.py
```
Manually one could change rows or columns clustering changing one of the following options to True from the 
sns.clustermap plot funciton
```
col_cluster=False
row_cluster=False
```

# References 
1- Seemann T. Prokka: rapid prokaryotic genome annotation Bioinformatics 2014 Jul 15;30(14):2068-9. PMID:24642063

2- Seemann T, Abricate, Github https://github.com/tseemann/abricate

3- O’Leary NA, Cox E, Holmes JB, Anderson WR, Falk R, Hem V, Tsuchiya MTN, Schuler GD, Zhang X, Torcivia J, Ketter A, Breen L, Cothran J, Bajwa H, Tinne J, Meric PA, Hlavina W, Schneider VA. Exploring and retrieving sequence and metadata for species across the tree of life with NCBI Datasets. Sci Data. 2024 Jul 5;11(1):732. doi: 10.1038/s41597-024-03571-y. PMID: 38969627; PMCID: PMC11226681.
