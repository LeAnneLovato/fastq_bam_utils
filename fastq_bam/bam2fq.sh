input=$1
ref=$2

if [ "$#" -ne 2 ]; then
	echo "Missing a parameter..."
	echo "** ARG[1]: BAM file"
	echo "** ARG[2]: Ref (.fa) file"
	exit 1
fi

sampleId=$(echo ${input} | cut -d "." -f 1)

echo "${sampleId}"

#Conversion
samtools sort -n ${input} -o ${sampleId}.sorted.bam

#Make fq files
bam bam2FastQ --in ${sampleId}.sorted.bam --refFile ${ref} --gzip --firstOut ${sampleId}_R1.fq.gz --secondOut ${sampleId}_R2.fq.gz --unpairedOut ${sampleId}_misc.fq.gz
	
#Clean up
rm ${sampleId}.sorted.bam

