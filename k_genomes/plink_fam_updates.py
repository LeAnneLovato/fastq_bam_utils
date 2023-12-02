#!/usr/bin/env python3

"""Extract population data from 1kg: http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/"""

import os
import argparse
import pathlib
import pandas as pd
import thousand_genomes_pop_info


def get_args():
    """Get commandline inputs"""
    parser = argparse.ArgumentParser(
        description="1) Update PLINK .fam (sex, mom, dad) "
        "2) Get pop & subpop info for samples"
    )
    parser.add_argument(
        "-i",
        "--input_fam",
        type=pathlib.Path,
        help="Provide a plink fam file",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--sample_input",
        type=pathlib.Path,
        help="Provide a sample file if its NOT 1k genomes data",
        required=False,
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    flags = get_args()
    plink_fam_file = flags.input_fam
    samples = pd.read_csv(plink_fam_file, index_col=0, sep="\t", header=None)
    pop_data = thousand_genomes_pop_info.read_pop_map()

    # defaults tp 1kg ped files is none supplied
    if flags.sample_input:
        sample_data = thousand_genomes_pop_info.read_sample_info(flags.sample_input)
    else:
        sample_data = thousand_genomes_pop_info.read_sample_info()

    with open(
        f"./{os.path.basename(plink_fam_file)}.updated", "w", encoding="utf-8"
    ) as updated_fam:
        with open(f"./population_info.txt", "w", encoding="utf-8") as pop_info:
            for content in samples.iterrows():
                fields = content[0].split()

                try:
                    sample_data[fields[0]]
                except KeyError:
                    print(f"Sample, {fields[0]}, not found")
                    updated_fam.write(f"{fields[0]}\t{fields[0]}\t0\t0\t0\t-9\n")
                    pop_info.write(f"{fields[0]}\tNA\tNA\n")
                else:
                    # header: famID, samplID, matID, patID, sex, pheno, subpop...
                    updated_fam.write(
                        f"{fields[0]}\t{fields[0]}\t{sample_data[fields[0]]['dad']}\t"
                        f"{sample_data[fields[0]]['mom']}\t{sample_data[fields[0]]['sex']}\t{fields[5]}\n"
                    )
                    # header: samplID, subpop, pop
                    pop_info.write(
                        f"{fields[0]}\t{sample_data[fields[0]]['subpop']}\t"
                        f"{pop_data[sample_data[fields[0]]['subpop']]}\n"
                    )

    print(f"{updated_fam.name}")
    print(f"{pop_info.name}")
