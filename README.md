# MLST-Klebsiella
Code used for a MLST for Klebsiella proyect in colaboration with Paredes-Amaya Claudia (U.Valle, Colombia) and Sánchez-Reyes Ayixon (IBT.UNAM, Mexico)


Requiere:

Obtain current complet current path directory in linux OS with

>pwd

for example /your/current/directory

Then, execute the script Preprocess_genomes.sh 

> Preprocess_genomes.sh /your/current/directory

It will download all genomes used in the current MLST to the current directory 
Once this step is completed, you can run the Process_and_Align.sh script if all the sanger sequences used are also in current directory
The script also requires the current directory direction as input

> Process_and_Align.sh /your/current/directory

