bam_file=$2
contig_list=$1

# required args
if [ "$#" -ne 2 ]; then 
	echo "Missing a parameter..."
	echo "** ARG[1]: Genome file"
	echo "** ARG[2]: BAM file"
	exit 1
fi

# loop over input file and download
while IFS=$'\t' read -r contig length; do
	echo "samtools stats ${bam_file} ${contig}" | qsub -cwd -N ${contig}_stats
done < ${contig_list}

