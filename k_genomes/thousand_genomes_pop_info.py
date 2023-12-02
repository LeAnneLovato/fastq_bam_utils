#!/usr/bin/env python3

"""Extract population data from 1kg: http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/"""

import os
import argparse
import pathlib
import pandas as pd
import re

SCRIPT_DIR = os.path.dirname(__file__)


def read_pop_map():
    """Read pop data into a dictionary"""

    pop_file = f"{SCRIPT_DIR}/../resources/igsr_populations.tsv"
    df = pd.read_csv(pop_file, index_col=0, sep="\t")
    pop_dict = {}
    pop = ""
    for index, row in df.iterrows():
        # replace descriptions with abbreviations
        if re.search("European", row["Superpopulation name"]):
            pop = "EUR"
        if re.search("East Asian", row["Superpopulation name"]):
            pop = "EAS"
        if re.search("South Asian", row["Superpopulation name"]):
            pop = "SAS"
        if re.search("African", row["Superpopulation name"]):
            pop = "AFR"
        if re.search("American", row["Superpopulation name"]):
            pop = "AMR"
        pop_dict.update({index: pop})
    return pop_dict


def read_sample_info(ped_file=None):
    """Read sample data into a dictionary"""
    sample_dict = {}
    if ped_file is None:
        ped_file = (
            f"{SCRIPT_DIR}/resources/integrated_call_samples_v3.20200731.ALL.ped.txt"
        )
    df = pd.read_csv(ped_file, index_col=0, sep="\t")
    for index, row in df.iterrows():
        sample_dict.update(
            {
                row["Individual ID"]: {
                    "sex": row["Gender"],
                    "subpop": row["Population"],
                    "mom": row["Maternal ID"],
                    "dad": row["Paternal ID"],
                }
            }
        )
    return sample_dict


def get_args():
    """Get commandline inputs"""
    parser = argparse.ArgumentParser(
        description="Get 1k genome sample info: sex, subpop, superpop, mom, dad"
    )
    parser.add_argument(
        "-i",
        "--input_file",
        type=pathlib.Path,
        help="Provide list of sample IDs",
        required=True,
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    arguments = get_args()
    sample_list = pd.read_csv(arguments.input_file, index_col=0, header=None)
    pop_db = read_pop_map()
    sample_db = read_sample_info()
    for index, row in sample_list.iterrows():
        try:
            sample_info = sample_db[index]
        except KeyError:
            print(f"{index}, ERROR: sample ID not found")
        else:
            super_pop = pop_db[sample_info["subpop"]]
            print(f"{index},{sample_info['sex']},{sample_info['subpop']},{super_pop}")
