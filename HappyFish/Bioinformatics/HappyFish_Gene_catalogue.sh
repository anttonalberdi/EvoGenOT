###-----------------------------------------------------------------###
###						HappyFish Metagenomic Pipeline				###
###-----------------------------------------------------------------###

# Credits: Jacob Agerbo Rasmussen
# Contact: Genomicsisawesome@gmail.com
# Version: 0.0.1

#-----------------------------------------------------------------#
#						Samples and sample list					  #
#-----------------------------------------------------------------#

find *.fq.gz > list
sed 's/.fq.gz//g' list > list2
uniq list2 > sample_list
rm -f list*
sample_list=$(cat sample_list)
echo ${sample_list[@]}

#-----------------------------------------------------------------#
#							Initial QC							  #
#-----------------------------------------------------------------#
module load java/1.8.0  fastqc/0.11.8
mkdir FastQC_initial
cd FastQC_initial


#!/bin/sh
###Note: No commands may be executed until after the #PBS lines
### Account information
#PBS -W group_list=ku-cbd -A ku-cbd
### Job name (comment out the next line to get the name of the script used as the job name)
#PBS -N jacras_SG01_trim
### Only send mail when job is aborted or terminates abnormally
#PBS -m n
### Number of nodes
#PBS -l nodes=1:ppn=21
### Memory
#PBS -l mem=120gb
### Requesting time - format is <days>:<hours>:<minutes>:<seconds> (here, 12 hours)
#PBS -l walltime=7:00:00:00

# Go to the directory from where the job was submitted (initial directory is $HOME)
echo Working directory is $PBS_O_WORKDIR
cd $PBS_O_WORKDIR

### Here follows the user commands:
# Define number of processors
NPROCS=`wc -l < $PBS_NODEFILE`
echo This job has allocated $NPROCS nodes

# Load all required modules for the job
module load java/1.8.0  fastqc/0.11.8
fastqc -o . ../*.fq.gz

unzip '*fastqc.zip'
head -n10 *_fastqc/fastqc_data.txt > 1-raw_read_count.txt


#-----------------------------------------------------------------#
#				Pre-processing, without collapse				  #
#-----------------------------------------------------------------#
### Trim adapters
mkdir 1-trimmed
cd 1-trimmed

#!/bin/sh
###Note: No commands may be executed until after the #PBS lines
### Account information
#PBS -W group_list=ku-cbd -A ku-cbd
### Job name (comment out the next line to get the name of the script used as the job name)
#PBS -N jacras_SG01_trim
### Only send mail when job is aborted or terminates abnormally
#PBS -m n
#PBS -j oe
#PBS -k oe
### Number of nodes
#PBS -l nodes=1:ppn=21
### Memory
#PBS -l mem=20gb
### Requesting time - format is <days>:<hours>:<minutes>:<seconds> (here, 12 hours)
#PBS -l walltime=7:00:00:00

# Go to the directory from where the job was submitted (initial directory is $HOME)
echo Working directory is $PBS_O_WORKDIR
cd $PBS_O_WORKDIR

### Here follows the user commands:
# Define number of processors
NPROCS=`wc -l < $PBS_NODEFILE`
echo This job has allocated $NPROCS nodes

# Load all required modules for the job
module load adapterremoval/2.2.4
FASTA_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/0-data'
WORK_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/0-data/1-trimmed'

cd $FASTA_DIR/
find *.fq.gz > temp
sed 's/_read_[1-2].fq.gz//g' temp > temp2
uniq temp2 > sample_list.txt
rm -f temp*
sample_list=$(cat sample_list.txt)
cd $WORK_DIR

for a in $sample_list
do
AdapterRemoval --file1 ../"$a"_read_1.fq.gz --file2 ../"$a"_read_2.fq.gz --basename "$a" --output1 "$a"_filtered_1.fq.gz --output2 "$a"_filtered_2.fq.gz --adapter1 AAGTCGGAGGCCAAGCGGTCTTAGGAAGACAA --adapter2 GAACGACATGGCTACGATCCGACTT --qualitybase 30 --minlength 50 --threads 20 --gzip
done


#-----------------------------------------------------------------#
#				Pre-processing, without collapse				  #
#-----------------------------------------------------------------#
### Trim adapters with cutadapt

#!/bin/sh
###Note: No commands may be executed until after the #PBS lines
### Account information
#PBS -W group_list=ku-cbd -A ku-cbd
### Job name (comment out the next line to get the name of the script used as the job name)
#PBS -N jacras_SG01_trim
### Only send mail when job is aborted or terminates abnormally
#PBS -m n
#PBS -j oe
#PBS -k oe
### Number of nodes
#PBS -l nodes=1:ppn=21
### Memory
#PBS -l mem=20gb
### Requesting time - format is <days>:<hours>:<minutes>:<seconds> (here, 12 hours)
#PBS -l walltime=7:00:00:00

# Go to the directory from where the job was submitted (initial directory is $HOME)
echo Working directory is $PBS_O_WORKDIR
cd $PBS_O_WORKDIR

### Here follows the user commands:
# Define number of processors
NPROCS=`wc -l < $PBS_NODEFILE`
echo This job has allocated $NPROCS nodes

# Load all required modules for the job
module load anaconda3/4.4.0 pigz/2.3.4
FASTA_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/0-data'
WORK_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/0-data/1-trimmed'

cd $FASTA_DIR/
find *.fq.gz > temp
sed 's/.fq.gz//g' temp > temp2
uniq temp2 > sample_list.txt
rm -f temp*
sample_list=$(cat sample_list.txt)
cd $WORK_DIR

for a in $sample_list
do
	/services/tools/anaconda3-2.2.0/bin/cutadapt --quality-base=33 --cores=0 -q 30 -m 50 -b AAGTCGGAGGCCAAGCGGTCTTAGGAAGACAA -b GAACGACATGGCTACGATCCGACTT -o $WORK_DIR/"$a"_filtered.fq.gz  $FASTA_DIR/"$a".fq.gz  > $WORK_DIR/"$a".fq.gz.cutadapt.log
done


#-----------------------------------------------------------------#
#				Post Trimming QC of merged reads				  #
#-----------------------------------------------------------------#
module load java/1.8.0  fastqc/0.11.8
mkdir FastQC_Post_Trim
cd FastQC_Post_Trim

#!/bin/sh
###Note: No commands may be executed until after the #PBS lines
### Account information
#PBS -W group_list=ku-cbd -A ku-cbd
### Job name (comment out the next line to get the name of the script used as the job name)
#PBS -N jacras_FastQC_51_filtered
### Only send mail when job is aborted or terminates abnormally
#PBS -m n
### Number of nodes
#PBS -l nodes=1:ppn=21
### Memory
#PBS -l mem=60gb
### Requesting time - format is <days>:<hours>:<minutes>:<seconds> (here, 12 hours)
#PBS -l walltime=1:00:00:00

# Go to the directory from where the job was submitted (initial directory is $HOME)
echo Working directory is $PBS_O_WORKDIR
cd $PBS_O_WORKDIR

### Here follows the user commands:
# Define number of processors
NPROCS=`wc -l < $PBS_NODEFILE`
echo This job has allocated $NPROCS nodes

# Load all required modules for the job
module load java/1.8.0  fastqc/0.11.8
fastqc ../1-trimmed/37_filtered_* -t 20

unzip '*fastqc.zip'
head -n10 *_fastqc/fastqc_data.txt > 2-Trimmed_read_count.txt

#-----------------------------------------------------------------#
#				Filtering of Host DNA, using Bowtie				  #
#-----------------------------------------------------------------#

# Filtering Host DNA, using Omyk_1.0 reference genome:		https://www.ncbi.nlm.nih.gov/assembly/GCF_002163495.1/

mkdir 1-Host_Removal
cd 1-Host_removal

# 1) Build Bowtie Host_DB
module load bowtie2/2.3.4.1
bowtie2-build ./refs/GCA_002163495.1_Omyk_1.0_genomic.fna.gz host_DB

# 2) bowtie2 mapping against host sequence database, keep both mapped and unmapped reads (paired-end reads)

#!/bin/sh
###Note: No commands may be executed until after the #PBS lines
### Account information
#PBS -W group_list=ku-cbd -A ku-cbd
### Job name (comment out the next line to get the name of the script used as the job name)
#PBS -N jacras_37_Host_filtering
### Only send mail when job is aborted or terminates abnormally
#PBS -m n
### Number of nodes
#PBS -l nodes=1:ppn=21
### Memory
#PBS -l mem=2000gb
### Requesting time - format is <days>:<hours>:<minutes>:<seconds> (here, 12 hours)
#PBS -l walltime=7:00:00:00

# Go to the directory from where the job was submitted (initial directory is $HOME)
echo Working directory is $PBS_O_WORKDIR
cd $PBS_O_WORKDIR

### Here follows the user commands:
# Define number of processors
NPROCS=`wc -l < $PBS_NODEFILE`
echo This job has allocated $NPROCS nodes

# Load all required modules for the job
module load bowtie2/2.3.4.1
declare -a sample_list=("")
for sample in "${sample_list[@]}"
do
bowtie2 -x host_DB -1 /home/projects/ku-cbd/people/jacras/1-HappyFish/0-data/1-trimmed/${sample}_filtered_1.fq.gz -2 /home/projects/ku-cbd/people/jacras/1-HappyFish/0-data/1-trimmed/${sample}_filtered_2.fq.gz -p 20 -S /1-Output/${sample}_mapped_and_unmapped.sam
done

# 3) convert file .sam to .bam
module load samtools/1.9 bedtools/2.28.0

samtools view -bS ${sample}_mapped_and_unmapped.sam > ${sample}_mapped_and_unmapped.bam

# 4) SAMtools SAM-flag filter: get unmapped pairs (both ends unmapped)
samtools view -b -f 12 -F 256 ${sample}_mapped_and_unmapped.bam > ${sample}_bothEndsUnmapped.bam

# 5) sort bam file by read name (-n) to have paired reads next to each other as required by bedtools
samtools sort -n ${sample}_bothEndsUnmapped.bam > ${sample}_bothEndsUnmapped_sorted.bam

bedtools bamtofastq -i ${sample}_bothEndsUnmapped_sorted.bam -fq ${sample}_host_removed_r1.fastq -fq2 ${sample}_host_removed_r2.fastq


#-----------------------------------------------------------------#
#						Assembly, using Spades					  #
#-----------------------------------------------------------------#
mkdir 1-Assembly
cd 1-Assembly
mkdir 1-MetaSpades
cd 1-MetaSpades

#!/bin/sh
###Note: No commands may be executed until after the #PBS lines
### Account information
#PBS -W group_list=ku-cbd -A ku-cbd
### Job name (comment out the next line to get the name of the script used as the job name)
#PBS -N jacras_Assembly
### Only send mail when job is aborted or terminates abnormally
#PBS -m n
### Number of nodes
#PBS -l nodes=1:ppn=21
### Memory
#PBS -l mem=120gb
### Requesting time - format is <days>:<hours>:<minutes>:<seconds> (here, 12 hours)
#PBS -l walltime=7:00:00:00

# Go to the directory from where the job was submitted (initial directory is $HOME)
echo Working directory is $PBS_O_WORKDIR
cd $PBS_O_WORKDIR

### Here follows the user commands:
# Define number of processors
NPROCS=`wc -l < $PBS_NODEFILE`
echo This job has allocated $NPROCS nodes

# Load all required modules for the job
module load SPAdes/3.13.0 anaconda3/4.4.0

for sample in "${sample_list[@]}"
do
spades.py --meta --1 ../../0-data/1-Host_Removal/${sample}_host_removed_r1.fastq --2 ../../0-data/1-Host_Removal/${sample}_host_removed_r2.fastq -o ../2-Assembly/${sample}/1-Spades_output
done

#-----------------------------------------------------------------#
#						Assembly, using MegaHit					  #
#-----------------------------------------------------------------#

mkdir 2-MegaHit
cd 2-MegaHit

#!/bin/sh
###Note: No commands may be executed until after the #PBS lines
### Account information
#PBS -W group_list=ku-cbd -A ku-cbd
### Job name (comment out the next line to get the name of the script used as the job name)
#PBS -N jacras_Assembly
### Only send mail when job is aborted or terminates abnormally
#PBS -m n
### Number of nodes
#PBS -l nodes=1:ppn=21
### Memory
#PBS -l mem=120gb
### Requesting time - format is <days>:<hours>:<minutes>:<seconds> (here, 12 hours)
#PBS -l walltime=7:00:00:00

# Go to the directory from where the job was submitted (initial directory is $HOME)
echo Working directory is $PBS_O_WORKDIR
cd $PBS_O_WORKDIR

### Here follows the user commands:
# Define number of processors
NPROCS=`wc -l < $PBS_NODEFILE`
echo This job has allocated $NPROCS nodes

# Load all required modules for the job
module load megahit/1.1.1

for sample in "${sample_list[@]}"
do
megahit -1 ../../0-data/1-Host_Removal/${sample}_host_removed_r1.fastq -2 ../../0-data/1-Host_Removal/${sample}_host_removed_r1.fastq -t 24 -o ${sample} --out-prefix ${sample}
done



#-------------------------------------------------------------------#
#					Co-Assembly, using MegaHit						#
#-------------------------------------------------------------------#

### check before running job
FASTA_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/0-data/2-Host_Removal/1-Output'
ASSEM_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/2-MegaHit/test'
FASTA=$(ls $FASTA_DIR/*.fastq.gz | python -c 'import sys; print ",".join([x.strip() for x in sys.stdin.readlines()])')


#!/bin/sh
###Note: No commands may be executed until after the #PBS lines
### Account information
#PBS -W group_list=ku-cbd -A ku-cbd
### Job name (comment out the next line to get the name of the script used as the job name)
#PBS -N jacras_Assembly
### Only send mail when job is aborted or terminates abnormally
#PBS -m n
### Number of nodes
#PBS -l nodes=1:ppn=25
### Memory
#PBS -l mem=100gb
### Requesting time - format is <days>:<hours>:<minutes>:<seconds> (here, 12 hours)
#PBS -l walltime=7:00:00:00
module load megahit/1.1.1 anaconda2/4.4.0
FASTA_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/0-data/2-Host_Removal/1-Output'
ASSEM_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/2-MegaHit/test'
FASTA=$(ls $FASTA_DIR/*.fastq.gz | python -c 'import sys; print ",".join([x.strip() for x in sys.stdin.readlines()])')
megahit -r $FASTA --min-contig-len 1000 -t 24 --presets meta-sensitive -o $ASSEM_DIR

#!/bin/sh
###Note: No commands may be executed until after the #PBS lines
### Account information
#PBS -W group_list=ku-cbd -A ku-cbd
### Job name (comment out the next line to get the name of the script used as the job name)
#PBS -N jacras_Assembly_test
### Only send mail when job is aborted or terminates abnormally
#PBS -m n
### Number of nodes
#PBS -l nodes=1:ppn=25
#PBS -j oe
#PBS -k oe
### Memory
#PBS -l mem=100gb
### Requesting time - format is <days>:<hours>:<minutes>:<seconds> (here, 12 hours)
#PBS -l walltime=2:00:00:00
module load megahit/1.1.1 anaconda2/4.4.0
ASSEM_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/2-MegaHit/test_pe12'
FASTA_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/0-data/2-Host_Removal/1-Output'
WORK_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/2-MegaHit/'

cd $FASTA_DIR/
find *.fastq.gz > temp
sed 's/_r[1-2].fastq.gz//g' temp > temp2
uniq temp2 > sample_list.txt
rm -f temp*
sample_list=$(cat sample_list.txt)
cd $WORK_DIR
for a in $sample_list
do
megahit -1 $FASTA_DIR/"$a"_r1.fastq.gz -2 $FASTA_DIR/"$a"_r2.fastq.gz --min-contig-len 1000 -t 24 --presets meta-sensitive -o $ASSEM_DIR
done

#-------------------------------------------------------------------#
#							Co-Assembly QC						#
#-------------------------------------------------------------------#

perl ../contig-stats.pl < ../test/final.contigs.fa

module load anaconda2/4.4.0 quast/5.0.2
quast.py -o Quast_out final.contigs.fa

#-------------------------------------------------------------------#
#						Mapping of Co-Assembly						#
#-------------------------------------------------------------------#

module load bwa/0.7.15
bwa index final.contigs.fa

################################ REMAP ##############################
#!/bin/sh
###Note: No commands may be executed until after the #PBS lines
### Account information
#PBS -W group_list=ku-cbd -A ku-cbd
### Job name (comment out the next line to get the name of the script used as the job name)
#PBS -N jacras_SG01_v2
### Only send mail when job is aborted or terminates abnormally
#PBS -m n
### Number of nodes
#PBS -l nodes=1:ppn=21
### Memory
#PBS -l mem=20gb
### Requesting time - format is <days>:<hours>:<minutes>:<seconds> (here, 12 hours)
#PBS -l walltime=1:00:00:00

# Go to the directory from where the job was submitted (initial directory is $HOME)
echo Working directory is $PBS_O_WORKDIR
cd $PBS_O_WORKDIR

### Here follows the user commands:
# Define number of processors
NPROCS=`wc -l < $PBS_NODEFILE`
echo This job has allocated $NPROCS nodes

# Load all required modules for the job
module load bwa/0.7.15
ASSEM_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/2-MegaHit/test_pe12_gz'
FASTA_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/0-data/2-Host_Removal/1-Output'
WORK_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/2-MegaHit/test_pe12_gz/remap'

cd $FASTA_DIR/
find *.fastq > temp
sed 's/_r[1-2].fastq//g' temp > temp2
uniq temp2 > sample_list.txt
rm -f temp*
sample_list=$(cat sample_list.txt)
cd $WORK_DIR
for a in $sample_list
do
        bwa mem -t 20  $ASSEM_DIR/final.contigs.fa $FASTA_DIR/"$a"_r1.fastq $FASTA_DIR/"$a"_r2.fastq > $WORK_DIR/"$a"_aln_pe.sam
done

#### Convert sam to bam ####

WORK_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/2-MegaHit/test_pe12_gz/remap'
for a in $sample_list
do
samtools view -bS $WORK_DIR/"$a"_aln_pe.sam > $WORK_DIR/"$a"_aln_pe.bam
done

#### Sort out allignment by supplementary allignment and vendor quality check (flag 2560)
#!/bin/sh
###Note: No commands may be executed until after the #PBS lines
### Account information
#PBS -W group_list=ku-cbd -A ku-cbd
### Job name (comment out the next line to get the name of the script used as the job name)
#PBS -N jacras_assembly_remap_sorting
### Only send mail when job is aborted or terminates abnormally
#PBS -m n
#PBS -j oe
#PBS -k oe
### Number of nodes
#PBS -l nodes=1:ppn=21
### Memory
#PBS -l mem=60gb
### Requesting time - format is <days>:<hours>:<minutes>:<seconds> (here, 12 hours)
#PBS -l walltime=2:00:00:00

# Go to the directory from where the job was submitted (initial directory is $HOME)
echo Working directory is $PBS_O_WORKDIR
cd $PBS_O_WORKDIR

### Here follows the user commands:
# Define number of processors
NPROCS=`wc -l < $PBS_NODEFILE`
echo This job has allocated $NPROCS nodes

# Load all required modules for the job
module load bwa/0.7.15 samtools/1.9
ASSEM_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/2-MegaHit/test_pe12_gz'
FASTA_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/0-data/2-Host_Removal/1-Output'
WORK_DIR='/home/projects/ku-cbd/people/jacras/1-HappyFish/2-MegaHit/test_pe12_gz/remap'

cd $FASTA_DIR/
find *.fastq > temp
sed 's/_r[1-2].fastq//g' temp > temp2
uniq temp2 > sample_list.txt
rm -f temp*
sample_list=$(cat sample_list.txt)
cd $WORK_DIR
for a in $sample_list
do
samtools view -F 2560 -b -h -q 20 -@ 12 -> $WORK_DIR/"$a"_aln_pe.bam > $WORK_DIR/"$a"_aln_sort.bam
done
################################ REMAP ##############################

#-----------------------------------------------------------------#
#	Gene prediction of MegaHit assemblies, using prodigal		  #
#-----------------------------------------------------------------#

### Gene prediction, using prodigal/2.6.3

#!/bin/sh
###Note: No commands may be executed until after the #PBS lines
### Account information
#PBS -W group_list=ku-cbd -A ku-cbd
### Job name (comment out the next line to get the name of the script used as the job name)
#PBS -N jacras_SG01_v2
### Only send mail when job is aborted or terminates abnormally
#PBS -m n
### Number of nodes
#PBS -l nodes=1:ppn=21
### Memory
#PBS -l mem=20gb
### Requesting time - format is <days>:<hours>:<minutes>:<seconds> (here, 12 hours)
#PBS -l walltime=1:00:00:00

# Go to the directory from where the job was submitted (initial directory is $HOME)
echo Working directory is $PBS_O_WORKDIR
cd $PBS_O_WORKDIR

### Here follows the user commands:
# Define number of processors
NPROCS=`wc -l < $PBS_NODEFILE`
echo This job has allocated $NPROCS nodes

# Load all required modules for the job
module load prodigal/2.6.3
prodigal -p meta -a prodigal/final.contigs.genes.faa -d prodigal/final.contigs.genes.fna -f gff -o prodigal/final.contigs.genes.gff -i final.contigs.fa
