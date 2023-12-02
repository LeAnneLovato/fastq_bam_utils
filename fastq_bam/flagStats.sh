input=$1 
if [ -z ${input} ]; then
	echo "**Input BAM required"
else
	samtools flagstat ${input}
fi
