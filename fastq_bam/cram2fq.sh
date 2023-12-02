input=$1
ref=$2

if [ "$#" -ne 2 ]; then
	echo "Missing a parameter..."
	echo "** ARG[1]: CRAM file"
	echo "** ARG[2]: Ref (.fa) file"
	exit 1
fi

sampleId=$(echo ${input} | cut -d "." -f 1)

echo "${sampleId}"

#Conversion
samtools view -T ${ref} -h -b -o ${sampleId}.convert.bam ${input}
samtools sort -n ${sampleId}.convert.bam -o ${sampleId}.sorted.bam

if [ ! -f "${sampleId}.sorted.bam" ]; then
	echo "${sampleId}.sorted.bam does not exist"
	exit 1;
fi

#Make fq files
bam bam2FastQ --in ${sampleId}.sorted.bam --refFile ${ref} --gzip --firstOut ${sampleId}_R1.fq.gz --secondOut ${sampleId}_R2.fq.gz --unpairedOut ${sampleId}_misc.fq.gz
	
#Clean up
rm ${sampleId}.convert.bam ${sampleId}.sorted.bam 

