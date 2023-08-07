#!/usr/bin/python3
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

    its almost 3am and
    Your looking at a nice pretty and informative dcostring rn

"""

import csv
import os
import sys
from tabulate import tabulate


# 3 images = 1 position in a trap, 5 positions per trap
def analyze_sporetraps(filename):
    """docstring goes here"""
    trap_results = csv_handler(filename)

    release = os.path.basename(os.path.dirname(filename))
    trap = os.path.basename(filename).split("_")[1]

    # Output data and file headers
    sporetrap_data = []
    headers = [
        "Trap",
        "Position",
        "Microspheres",
    ]
    image, position = 1, 1
    counted = 0
    for result in trap_results:
        counted += result
        if image % 3 == 0:
            sporetrap_data.append([trap, position, counted])
            counted = 0
            position += 1
        image += 1

    # Write the results to the output file
    outfile = f"../results/FinalResults_{release}.csv"
    write_headers = True
    if os.path.exists(outfile):
        write_headers = False
    with open(
        f"../results/FinalResults_{release}.csv",
        "a",
        newline="",
    ) as csv_outfile:
        csv_writer = csv.writer(csv_outfile)
        if write_headers:
            csv_writer.writerow(headers)
        for row in sporetrap_data:
            csv_writer.writerow(row)

    # Print a table of the results for the user
    print(tabulate(sporetrap_data, headers=headers))


# handle csv datasets
def csv_handler(filename):
    """docstring goes here"""
    with open(filename, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        image_data = []
        counted = 0
        current_slice = 1
        for row in csv_reader:
            # Filter out bad ROIs | Start here: 1 pixel = 7.84 um^2
            # if float(row["Area"]) < 7.84 * 4:
            #     continue
            # calculate totals for each image
            if int(row["Slice"]) == current_slice:
                counted += 1
            else:
                # hit the next slice, store the count
                image_data.append(counted)
                current_slice += 1
                counted = 1
        # outside of the loop
        image_data.append(counted)

        return image_data


def main(filename):
    """docstring goes here"""
    os.chdir(os.path.dirname(sys.argv[0]))
    analyze_sporetraps(filename)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        sys.exit(f"Usage: {sys.argv[0]} [FILE]")
