#!/usr/bin/env python3

"""Reads PHY data, filter for samples with > 75% non-N calls, and add pop data tags to sample name"""

import sys
import os
import argparse
import pathlib
import pandas as pd
import thousand_genomes_pop_info

SCRIPT_DIR = os.path.dirname(__file__)


def population_info(search, pop_dict, sample_dict, geno_dict):
    """Append sample with pop data"""

    new_name = search
    for sample_name in sample_dict.keys():
        if sample_name == search:
            try:
                new_name = (
                    f"{sample_name}_{pop_dict[sample_dict[sample_name]['subpop']]}"
                    f"_{sample_dict[sample_name]['subpop']}_{geno_dict[sample_name]}"
                )
            except KeyError:
                new_name = (
                    f"{sample_name}_{pop_dict[sample_dict[sample_name]['subpop']]}"
                    f"_{sample_dict[sample_name]['subpop']}"
                )
            else:
                pass

    return new_name


def read_sample_genotype():
    """Read sample data into a dictionary"""

    geno_dict = {}
    ped_file = f"{SCRIPT_DIR}/resources/cyp2a6_onekg_meta.csv"
    df = pd.read_csv(ped_file)
    for _, row in df.iterrows():
        geno_dict.update({row["sampname"]: row["genotype"]})
    return geno_dict


def get_args():
    """Get commandline inputs"""

    parser = argparse.ArgumentParser(
        description="Calculate non-N bases in a philip (.phy) file"
    )
    parser.add_argument(
        "-i",
        "--input_file",
        type=pathlib.Path,
        help="Provide a philip (.phy) file",
        required=True,
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    arguments = get_args()
    input_file = arguments.input_file
    out_dir = os.path.dirname(input_file)

    # get population info
    pop_data = thousand_genomes_pop_info.read_pop_map()
    sample_data = thousand_genomes_pop_info.read_sample_info()
    genotype_data = read_sample_genotype()

    # read phy file
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            header = file.readline()
            data = file.readlines()
    except FileNotFoundError:
        sys.exit()
    else:
        total = len(data)
        clean_data = []
        print("Samples filtered out:")

        # loop over phy file
        for sample in data:
            info = sample.split()
            seq_name = info[0]
            seq = info[1]
            INFORM_SITE = 0

            # loop over sequence
            for nt in seq:
                if nt != "N":
                    INFORM_SITE += 1
            faction_called = INFORM_SITE / len(seq)

            # rename sample
            name = population_info(
                search=seq_name,
                pop_dict=pop_data,
                sample_dict=sample_data,
                geno_dict=genotype_data,
            )

            # filter on fraction called ACTG
            if faction_called > 0.75:
                clean_data.append(f"{name} {seq}")
            else:
                total -= 1
                print(f"{name}\t{round(faction_called, 3)}")

        # write new phy to file
        with open(f"{out_dir}/clean_data.phy", "w", encoding="utf-8") as out:
            # phy header
            out.write(f"{total} {len(seq)}\n")

            # phy seqs
            for dat in clean_data:
                out.write(f"{dat}\n")

        print(f"Revised Phy Data:\t{os.path.abspath(out.name)}")
