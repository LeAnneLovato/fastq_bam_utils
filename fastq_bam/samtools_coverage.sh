contig_list=$1
bam=$2

# required args
if [ "$#" -ne 2 ]; then 
	echo "Missing a parameter..."
	echo "** ARG[1]: Genome File"
	echo "** ARG[2]: BAM File"
	exit 1
fi

# loop over input file and download
while IFS=$'\t' read -r contig length; do
	echo "samtools coverage -r ${contig} ${bam}" | qsub -cwd -N ${contig}_cov
done < ${contig_list}

