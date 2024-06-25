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
