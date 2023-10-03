#!/usr/bin/env python3
#
# This file is part of the sporetrap analysis scripts.
#
# Copyright (c) 2023 Jason Toney
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


# 3 images = 1 position in a trap, 4-5 positions per trap
def analyze_sporetraps(filename):
    """Total the counts for each position and write the results to an output file."""
    release = os.path.basename(os.path.dirname(filename))
    trap = os.path.basename(filename).split("_")[1]
    trap_results = csv_handler(filename)
    # make sure each trap has the correct number of images, 12 or 15 depending on release
    image_count = len(trap_results)
    if image_count % 3 != 0:
        sys.exit(f"ERROR: {release}: Trap {trap} contains {image_count} images.")
    # Output data and file headers
    sporetrap_data = []
    headers = [
        "Trap",
        "Position",
        "Microspheres",
        "Notes",
    ]
    # Use height instead of relative position
    positions = [0, 0.5, 1.0, 1.5, 3.0]
    # Combine counts for each position
    image, position = 1, 1
    # 4 position traps start at position 2
    if image_count == 12:
        position = 2
    counted = 0
    for result in trap_results:
        counted += result
        if image % 3 == 0:
            sporetrap_data.append([trap, positions[position - 1], counted])
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
        current_slice = 1
        for row in csv_reader:
            # calculate totals for each image
            if int(row["Slice"]) == current_slice:
                if not is_artifact(row):
                    counted += 1
            else:
                # hit the next slice, store the count
                image_data.append(counted)
                # don't assume what the "next" slice is, a slice could be missing/empty
                current_slice = int(row["Slice"])
                if is_artifact(row):
                    counted = 0
                else:
                    counted = 1
        # outside of the loop
        image_data.append(counted)
    return image_data


# Filter out bad ROIs | Start here: 1 pixel = 7.84 um^2
def is_artifact(row):
    """Returns whether or not the ROI should be counted."""
    return float(row["Area"]) <= 7.84 * 4 or (
        not 135 <= float(row["Y"]) <= 2125 and not 3575 <= float(row["Y"]) <= 5565
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
