#!/usr/bin/env python3

"""Count the number of de novo variants in a VCF"""
import sys

if len(sys.argv) < 3:
    print("Required Input:\n**Uncompressed VCF\n**Smaple Int (9-11, trio)")
    sys.exit()
else:
    file = sys.argv[1]
    sampleTab = int(sys.argv[2])
    with open(file, "r", encoding="UTF-8") as f:
        with open(file + ".dn.vcf", "w", encoding="UTF-8") as o:
            dnCount = 0
            inherited = 0
            missing = 0
            lowDq = 0
            total = 0
            unknown = 0

            # Read each line in the file
            for line in f:
                if line.startswith("#"):
                    continue

                # Total variants
                total += 1

                # Process VCF lines
                tabs = line.split("\t")
                filter_tab = tabs[6]
                format_tab = tabs[8].split(":")
                proband_calls = tabs[sampleTab].split(":")
                index = 0

                # PASS variants
                if filter_tab == "PASS":
                    # Find DN calls
                    if "DN" not in format_tab:
                        unknown += 1
                    else:
                        for index in range(len(format_tab)):
                            if format_tab[index] == "DN":
                                if len(format_tab) == len(proband_calls):
                                    if proband_calls[index] == "DeNovo":
                                        dnCount += 1
                                        o.write(line)
                                    elif proband_calls[index] == "Inherited":
                                        inherited += 1
                                    elif proband_calls[index] == "LowDQ":
                                        lowDq += 1
                                    elif proband_calls[index] == ".":
                                        missing += 1
                                    else:
                                        unknown += 1

    trioConcordance1 = 1 - (float(dnCount) / float(total))
    trioConcordance2 = 1 - float(dnCount) / float(inherited + lowDq + dnCount)
    print(total)
    print(dnCount)
    print(inherited)
    print(lowDq)
    print(missing)
    print(unknown)
    print("%.5f" % trioConcordance1)
    print("%.5f" % trioConcordance2)
