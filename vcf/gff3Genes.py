#!/usr/bin/env python3

"""Extract genes and mRNAs from a GFF3 file"""

import sys

if len(sys.argv) < 2:
    print("Required Input:\n**GFF3")
    sys.exit()
else:
    file = sys.argv[1]

    # Read each line in the file
    with open(file, "r", encoding="UTF-8") as f:
        for line in f:
            if line.startswith("#"):
                continue

            # Process lines
            tabs = line.split("\t")
            chrom = tabs[0]
            start = tabs[3]
            stop = tabs[4]
            annoType = tabs[2]
            if annoType == "gene":
                name = tabs[8].split(";")[1].split("Name=")[1]
            elif annoType == "mRNA":
                name = tabs[8].split(";")[2].split("Name=")[1]
                print("chr" + chrom + "\t" + start + "\t" + stop + "\t" + name)
