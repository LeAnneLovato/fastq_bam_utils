bam_list=$1

# required args
if [ "$#" -ne 1 ]; then 
	echo "Missing a parameter..."
	echo "** ARG[1]: File list of BAMs"
	exit 1
fi

# loop over input file and download
while IFS=$'\t' read -r bam_file gvcf_file median_coverage; do
	sample=$(basename $bam_file | cut -d "." -f 1)
	echo "${sample}"
	samtools view ${bam_file} ${region}
done < ${bam_list}

