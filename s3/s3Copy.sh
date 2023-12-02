dir=$1
path=$2
profile=$3

# required args
if [ "$#" -ne 3 ]; then
        echo "Missing a parameter..."
        echo "** ARG[1]: target directory for download"
        echo "** ARG[2]: s3 path"
        echo "** ARG[3]: AWS profile"
	exit 1
fi

# determine endpoint from profile
if [ "${profile}" == "USSD" ]; then
	endpoint="https://endpont1.com"
elif [ "${profile}" == "USFC" ]; then
	endpoint="https://endpont2.com"
else
	echo "Unable to determine the endpoint from the profile provided, ${profile}"
	exit 1
fi

echo "Source Dir: ${path}"
echo "Target Dir: ${dir}"
echo "Profile: ${profile}"
echo "Endpoint: ${endpoint}"

aws s3 --profile ${profile} --endpoint ${endpoint} cp ${path} ${dir} 
aws s3 --profile ${profile} --endpoint ${endpoint} cp ${path}.crai ${dir}
