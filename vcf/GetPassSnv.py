#!/usr/bin/env python3

"""Extract PASS SNVs from a VCF"""

import sys

if len(sys.argv) < 4:
    print("Required Input:\n**Uncompressed VCF\n**VCF type\t**Smaple Int (9-11, trio)")
    sys.exit()
else:
    file = sys.argv[1]
    vcfType = sys.argv[2]
    sampleTab = sys.argv[3]

    # Read each line in the file
    with open(file, "r", encoding="UTF-8") as f:
        for line in f:
            if line.startswith("#"):
                continue

            # Process VCF lines
            tabs = line.split("\t")
            ref = int(len(tabs[3]))
            alt = tabs[4]
            filter_tab = tabs[6]
            proband_gt = tabs[int(sampleTab)].split(":")[0]

            # PASS Variants
            if filter_tab == "PASS":
                removeReturn = line.split("\n")
                print(removeReturn[0])

            # Small Variants
            if vcfType == "small":
                if int(len(alt)) == 1 and int(len(ref)) == 1 and filter_tab == "PASS":
                    if (
                        proband_gt == "0/1"
                        or proband_gt == "1/1"
                        or proband_gt == "0|1"
                        or proband_gt == "1|1"
                        or proband_gt == "1"
                    ):
                        print(
                            tabs[0] + ":" + tabs[1] + "-" + tabs[1] + "\t" + proband_gt
                        )

                # Multiple Alt alleles
                elif "," in alt and ref == 1 and filter_tab == "PASS":
                    alt_alleles = tabs[4].split[","]
                    if len(alt_alleles[0]) == 1 or len(alt_alleles[1] == 1):
                        if (
                            proband_gt == "0/1"
                            or proband_gt == "1/1"
                            or proband_gt == "0|1"
                            or proband_gt == "1|1"
                            or proband_gt == "1"
                        ):
                            print(
                                tabs[0]
                                + ":"
                                + tabs[1]
                                + "-"
                                + tabs[1]
                                + "\t"
                                + proband_gt
                            )

            # CNVs
            elif vcfType == "cnv":
                if filter_tab == "PASS":
                    coords = tabs[2].split(":")[3]
                    if (
                        proband_gt == "0/1"
                        or proband_gt == "1/1"
                        or proband_gt == "0|1"
                        or proband_gt == "1|1"
                        or proband_gt == "1"
                    ):
                        print(tabs[0] + ":" + coords + "\t" + proband_gt)
