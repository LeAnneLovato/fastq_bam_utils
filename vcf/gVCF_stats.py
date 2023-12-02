#!/usr/bin/env python3

"""gVCF stats for callability, allele depth, total depth, GT quality"""

import sys
import os
import argparse
import pathlib
import gzip
import numpy as np

SCRIPT_DIR = os.path.dirname(__file__)


def get_args():
    """Get commandline inputs"""
    parser = argparse.ArgumentParser(
        description="gVCF stats for callability, allele depth, total depth, GT quality"
    )
    parser.add_argument(
        "-g",
        "--gvcf",
        type=pathlib.Path,
        help="Provide a bgzip compressed gVCF file",
        required=True,
    )
    parser.add_argument(
        "-w",
        "--window_size",
        type=int,
        help="Provide a bgzip compressed gVCF file",
        required=True,
    )
    args = parser.parse_args()
    return args


def callability(vcf_lines):
    """Callability is calculated as PASS sites where all samples have a GQ > 25 divided by all sites in the window"""
    callability_tally = 0  # track all callable sites

    # loop over window
    for entry in vcf_lines:
        format_info = entry["format"].split(":")
        gq_index = format_info.index("GQ")

        # include pass sites
        if entry["filter"] == "PASS":
            callable_count = 0  # track samples with GQ > 25

            # loop over samples
            for sample in entry["samples"]:
                fields = sample.split(":")
                if fields[gq_index] != "." and int(fields[gq_index]) > 25:
                    callable_count += 1

            # count as callable if all samples meet GQ cutoff
            if callable_count == len(entry["samples"]):
                callability_tally += 1

    # callable sites / all sites in window
    callability_metric = round(callability_tally / len(vcf_lines), 4)
    return f"{callability_tally}\t{callability_metric}"


def depth(vcf_lines):
    """Depth is calculated for all sites with information"""
    depth_values = []  # store depth for each sample across sites

    # loop over window
    for entry in vcf_lines:
        format_info = entry["format"].split(":")
        dp_index = format_info.index("DP")

        # loop over samples
        for sample in entry["samples"]:
            fields = sample.split(":")

            # code missing info as nan
            if fields[dp_index] == ".":
                depth_values.append(float("nan"))
            else:
                depth_values.append(float(fields[dp_index]))

    # remove nan values for depth summary
    dp_mean = round(np.nanmean(depth_values), 4)
    dp_sd = round(np.nanstd(depth_values), 4)
    dp_median = round(np.nanmedian(depth_values), 4)
    dp_min = round(np.nanmin(depth_values), 4)
    dp_max = round(np.nanmax(depth_values), 4)
    return f"{dp_min}\t{dp_max}\t{dp_median}\t{dp_mean}\t{dp_sd}"


if __name__ == "__main__":
    arguments = get_args()

    # gvcf is compressed
    if arguments.gvcf.name.endswith(".gz"):
        # initialize
        BASE_COUNT = 0  # track uniq bases in a window
        WINDOW_SIZE = arguments.window_size
        window_content = []
        chrom = None
        pos = None

        # read gvcf line by line
        with gzip.open(arguments.gvcf, "rb") as stream:
            # create output file
            with open("gvcf_metrics.txt", "w", encoding="utf-8") as outfile:
                print("Calculating gVCF Metrics")
                print(f"Output file: {os.path.abspath(outfile.name)}")

                outfile.write(
                    "#chrom\twindow_start\twindow_end\tuniq_sites\ttotal_sites\t"
                    "min_dp\tmax_dp\tmedian_dp\tmean_dp\tsd_dp\t"
                    "callable_sites\tcallability\n"
                )

                # loop over gVCF
                for line in stream:
                    # ignore header lines
                    if line.decode().startswith("#"):
                        continue

                    # create a list of dict. from the vcf lines
                    content = line.decode().strip().split()

                    # increment window bases when unique
                    if pos and content[1] != pos:
                        BASE_COUNT += 1

                    # base count >= 1500bp || chrom change
                    if BASE_COUNT == WINDOW_SIZE or chrom and content[0] != chrom:
                        # calculate metrics & reset window
                        # print(len(window_content))
                        # sys.exit()
                        depth_summary = depth(window_content)
                        callability_summary = callability(window_content)
                        outfile.write(
                            f"{window_content[0]['chr']}\t{window_content[0]['pos']}\t"
                            f"{window_content[BASE_COUNT - 1]['pos']}\t{BASE_COUNT}\t{len(window_content)}\t"
                            f"{depth_summary}\t{callability_summary}\n"
                        )
                        BASE_COUNT = 0
                        RAW_BASE_COUNT = 0
                        window_content = []

                    chrom = content[0]
                    pos = content[1]
                    window_content.append(
                        {
                            "chr": content.pop(0),
                            "pos": content.pop(0),
                            "id": content.pop(0),
                            "ref": content.pop(0),
                            "alt": content.pop(0),
                            "qual": content.pop(0),
                            "filter": content.pop(0),
                            "info": content.pop(0),
                            "format": content.pop(0),
                            "samples": content,
                        }
                    )

                # finish last window
                depth_summary = depth(window_content)
                callability_summary = callability(window_content)
                outfile.write(
                    f"{window_content[0]['chr']}\t{window_content[0]['pos']}\t"
                    f"{window_content[BASE_COUNT - 1]['pos']}\t{BASE_COUNT}\t{len(window_content)}\t"
                    f"{depth_summary}\t{callability_summary}\n"
                )

    # gvcf is uncompressed
    else:
        print("ERROR: The gVCF must be compressed")
        sys.exit()
