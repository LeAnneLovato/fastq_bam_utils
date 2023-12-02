if [ "$#" -ne 1 ]; then
    echo "Input[1]: VCF"
    exit
fi

input=$1
name=$(basename ${input} | cut -d "." -f 1)

plink --vcf ${input} --make-bed --out ${name} --allow-extra-chr
