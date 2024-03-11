#!/usr/bin/env python3
#
# This file is part of the sporetrap analysis scripts.
#
# Copyright (c) 2024 Jason Toney
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
    This script counts the number of microspheres captured by rods in a sporetrap.
    Input: CSV file containing list of ROIs generated by our analysis with ImageJ.
    Output: CSV file containing count of microspheres for each position in a trap.
"""

import csv
import os
import sys
from math import pi


# 30 images = 1 filter position in a trap, 4 filter positions per trap
def analyze_sporetraps(filename):
    """Total the counts for each position and write the results to an output file."""
    release = os.path.basename(os.path.dirname(filename))
    trap = os.path.splitext(os.path.basename(filename))[0].split("_")[1]
    trap_results = csv_handler(filename)
    # make sure each trap has the correct number of images, 120 for a full release
    image_count = len(trap_results)
    if image_count != 120:
        sys.exit(f"ERROR: {release}: Trap {trap} contains {image_count} images.")
    # Output data and file headers
    sporetrap_data = []
    headers = [
        "Trap",
        "Position",
        "Microspheres",
    ]
    # Combine counts for each position
    image, position = 1, 1
    counted = 0
    for result in trap_results:
        counted += result
        if image % 30 == 0:
            sporetrap_data.append([trap, position, counted])
            counted = 0
            position += 1
        image += 1
    # Write the results to the output file
    outfile = f"results/{release}.csv"
    write_headers = True
    if os.path.exists(outfile):
        write_headers = False
    with open(
        outfile,
        "a",
        newline="",
        encoding="utf-8",
    ) as csv_outfile:
        csv_writer = csv.writer(csv_outfile)
        if write_headers:
            csv_writer.writerow(headers)
        for row in sporetrap_data:
            csv_writer.writerow(row)


# handle csv datasets
def csv_handler(filename):
    """Count the microspheres and drop any bad ROIs."""
    with open(f"ImageJ/{filename}", "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        image_data = []
        counted = 0
        for row in csv_reader:
            # calculate totals for each image
            if int(row["Slice"]) == len(image_data) + 1:
                counted += not is_artifact(row)
            else:
                # hit the next slice, store the count
                image_data.append(counted)
                counted = not is_artifact(row)
        # outside of the loop
        image_data.append(counted)
    return image_data


# Filter out bad ROIs | Start here: 1 pixel = 8.067 µm^2, d = 4.017 µm
def is_artifact(row):
    """Returns true if the ROI should not be counted."""
    # Microsphere diameter thresholds (feret diameter measured by ImageJ)
    thresholds = [10, 50, 150, 400, 500]
    index = (int(row["Slice"]) - 1) // 30
    # ROI must have a minimum area and be within bounds of the targeted particle size
    return (
        float(row["Area"]) < pi * (thresholds[index] / 2) ** 2
        or not thresholds[index] <= float(row["Feret"]) <= thresholds[index + 1]
    )


def main(filename):
    """Execute main objective."""
    os.chdir(os.path.dirname(__file__))
    analyze_sporetraps(filename)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        sys.exit(f"Usage: python3 {__file__} [FILE]")
