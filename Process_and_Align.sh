#!/bin/bash
# This scripts requires: 1) that all .seq and .abi files are in the current directory
#                        2) Introduce the $PATH of the current as argument as it creates sub folders
#                        
PATH=$1

#Folders variables
parent_dir="$PATH"
working_dir=Results_dir
reseqdir=$parent_dir/Reseq
gapAfolder=gapA
infBfolder=infB
mdhfolder=mdh
pgifolder=pgi
phoEfolder=phoE
tonBfolder=tonB
rpoBfolder=rpoB
folder_seqOir=Originales

#Create folders
mkdir -p $folder_seqOir
mkdir -p $Working_dir
cd $parent_dir

# make copy of sequences to work on
cp *.seq $working_dir/
#Move original information to a safe folder
mv *.seq $folder_seqOir/
mv *.ab1 $folder_seqOir/
cd $working_dir
rm *EC*

# Remove bad cuality and reseq secuences
list=(DA_131_KP211-rpoB_rpoB-F_E06.seq DA_123_KP126-rpoB_rpoB-F_E05.seq DA_099_KP126-phoE_phoE-F_E02.seq DA_099_KP126-phoE_phoE-F_E02.seq DA_090_KP79-phoE_phoE-F_D01.seq CA_047_KP65-mdh_mdh-F_C07.seq CA_048_KP79-mdh_mdh-F_D07.seq CA_050_KP92-mdh_mdh-F_F07.seq CA_054_KP116-mdh_mdh-F_B08.seq CA_055_KP121-mdh_mdh-F_C08.seq CA_056_KP122-mdh_mdh-F_D08.seq CA_065_KP211-mdh_mdh-F_E09.seq CA_078_KP126-pgi_pgi-F_E11.seq)
for file in "${list[@]}"; do
    rm -f "$file"
done

# Here iniciates ciclyes to process every gene sequence
for file in *gapA_gapA*; do
    base_name=$(echo "$file" | cut -c 8-17 | tr '-' '_')
    seqkit subseq -r 40:610 -o "${base_name}.fasta" "$file"
done
rm -f *.fai
mkdir -p $gapAfolder
mv *.fasta $gapAfolder/

for file in *infB_infB*; do
    base_name=$(echo "$file" | cut -c 8-17 | tr '-' '_')
    seqkit subseq -r 40:450 -o "${base_name}.fasta" "$file"
done
rm -f *.fai
mkdir -p $infBfolder
mv *.fasta $infBfolder/

for file in *-pgi_pgi*; do
    base_name=$(echo "$file" | cut -c 8-17 | tr '-' '_')
    seqkit subseq -r 20:650 -o "${base_name}.fasta" "$file"
done
seqkit subseq -r 20:650 -o KP111_pgi.fasta CA_074_KP111-pgiA_pgi-F_A11.ab1
rm -f *.fai
mkdir -p $pgifolder
mv *.fasta $pgifolder

for file in *-phoE_phoE*; do
    base_name=$(echo "$file" | cut -c 8-17 | tr '-' '_')
    seqkit subseq -r 30:570 -o "${base_name}.fasta" "$file"
done
seqkit subseq -r 30:570 -o KP79_phoE.fasta BC_009_KP79-phoE_PhoE-F_A07.seq
seqkit subseq -r 30:570 -o KP126_phoE.fasta BC_010_KP126-phoE_PhoE-F_B07.seq
rm -f *.fai
mkdir -p $phoEfolder
mv *.fasta $phoEfolder

for file in *-rpoB_rpoB*; do
    base_name=$(echo "$file" | cut -c 8-17 | tr '-' '_')
    seqkit subseq -r 70:780 -o "${base_name}.fasta" "$file"
done
seqkit subseq -r 70:780 -o KP211_rpoB.fasta BC_012_KP211-rpoB_rpoB_D07.seq
rm -f *.fai
mkdir -p $rpoBfolder
mv *.fasta $rpoBfolder

for file in *-tonB_tonBB*; do
    base_name=$(echo "$file" | cut -c 8-17 | tr '-' '_')
    seqkit subseq -r 20:520 -o "${base_name}.fasta" "$file"
done
seqkit subseq -r 70:520 -o KP126_tnoB.fasta BC_013_KP126-tonB_tonB_E07.seq
rm -f *.fai
mkdir -p $tonBfolder
mv *.fasta $tonBfolder

####################################################################################
######### The following code requires that the annotation with native prokka was met
#####################################################################################
cd $parent_dir

# Cycle on the Klebsiella and Enterobacter genomes
# requires that they be located in parent_dir
for file in *.fna ; do
    base_name=$(echo "$file" | cut -c 1-15)
    dir=$base_name/
    cd "$parent_dir/$dir"
    # Este ciclo extrae las secuencias de los genes en formato fasta 
    for gene in ${genes[@]}; do
        gff=$base_name.gff
        ffn=$base_name.ffn
        seq_out="${base_name}_${gene}.fasta"
        echo "Extrayendo el gen $gene del genoma $base_name "
        # Con el siguiente comando puedo obtener los IDS para extraer las secuencias de los genes
        seqid_file="$gene"_ID.txt
        grep "$gene" "$gff" | awk '{print $9}' | grep "locus_tag" | awk -F'=' '{print $NF}' > $seqid_file
        #sleep 2
        seqkit grep -f $seqid_file $ffn > $seq_out
        #pattern="$(cat $seqid_file)"
        while IFS= read -r pattern; do
            sed -i "s/$pattern/${base_name}_${gene}_${pattern}/" $seq_out
        done < "$seqid_file"
    done
    folder_clean=genes_mlst
    mkdir -p $folder_clean
    mv *ID* $folder_clean
    mv *.fasta "$folder_clean"
done

# Here all the generated genes are taken and put in the folders
# in which the genes resulting from bleeding are found individually
cd $parent_dir
find . -name *rpoB.fasta* -exec cp {} $working_dir/rpoB/ \;

find . -name *infB.fasta* -exec cp {} $working_dir/infB/ \;

find . -name *mdh.fasta* -exec cp {} $working_dir/mdh/ \;

find . -name *gapA.fasta* -exec cp {} $working_dir/gapA/ \;

find . -name *pgi.fasta* -exec cp {} $working_dir/pgi/ \;

find . -name *phoE.fasta* -exec cp {} $working_dir/phoE/ \;

find . -name *tonB.fasta* -exec cp {} $working_dir/tonB/ \;

cd $working_dir
aligmentfolder=aligments
mkdir -p $aligmentfolder
#All genes are concatenated. File order is maintained automatically
cat rpoB/*.fasta > $aligmentfolder/all_rpoB.fasta
cat infB/*.fasta > $aligmentfolder/all_infB.fasta
cat mdh/*.fasta > $aligmentfolder/all_mdh.fasta
cat gapA/*.fasta > $aligmentfolder/all_gapA.fasta
cat pgi/*.fasta > $aligmentfolder/all_pgi.fasta
cat phoE/*.fasta > $aligmentfolder/all_phoE.fasta
cat tonB/*.fasta > $aligmentfolder/all_tonB.fasta

# Execute mafft
for file in *.fasta; do
    basename=$(echo "$file" | sed 's/.fasta$//')
    mafft "$file" > $basename.mafft
done

#Execute trimal
#It requieres manual inspection to double check optimal trimm
for file in *.mafft; do 
    basename=$(echo "$file" | sed 's/.mafft$//')
    trimal -in $file -out trim_$basename.fasta -gappyout
done




