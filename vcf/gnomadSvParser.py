#!/usr/bin/env python3

"""Parse gnomad SVs"""

import sys

if len(sys.argv) < 2:
    print("Required Input:\n**gnomAD SV VCF")
    sys.exit()
else:
    with open("gnomad_sv.txt", "w", encoding="UTF-8") as gg:
        # Read each line in the file
        file = sys.argv[1]
        with open(file, "r", encoding="UTF-8") as f:
            for line in f:
                if line.startswith("#"):
                    continue

            # Process lines
            tabs = line.split("\t")
            chrom = tabs[0]
            start = tabs[1]
            ref = tabs[3]
            alt = tabs[4]
            # Filter for INS, DEL, DUP
            if alt == "<INS>" or alt == "<DEL>" or alt == "<DUP>":
                info = tabs[7]
                infoItems = info.split(";")
                for entry in infoItems:
                    if entry.startswith("END="):
                        end = entry.split("=")[1]
                    if entry.startswith("SVLEN"):
                        svlen = entry.split("=")[1]
                    if entry.startswith("AN"):
                        ac = entry.split("=")[1]
                    if entry.startswith("AC"):
                        an = entry.split("=")[1]
                    if entry.startswith("AF"):
                        af = entry.split("=")[1]
                gg.write(
                    f"{chrom}\t{start}\t{ref}\t{alt}\t{end}\tgnomadSV_2.1\t{svlen}\t{af}\t{an}\t{ac}\n"
                )
