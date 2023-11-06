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
    This script executes the ImageJ macro and python scripts in a batch process.
    Input: all images found within the local "ECHO Images" folder.
    Output: CSV file containing the total counts of microspheres in the images.
"""

import glob
import os
import subprocess
import sys
import time

import analyze_sporetraps
import compile_workbook
import format_workbook


def batch_process(image_folder):
    """Analyze all the images found in "ECHO Images" subdirectories."""
    # Start the timer
    start_time = time.time()
    # Count how many albums are processed
    processed = 0
    # Clean out any stale results files
    _ = [
        os.remove(file)
        for file in glob.glob(os.path.join(f"{os.path.dirname(__file__)}/results", "*"))
    ]
    # Also nuke old workbooks
    workbook_file = f"{os.path.dirname(__file__)}/Particle Release Counts.xlsx"
    if os.path.exists(workbook_file):
        os.remove(workbook_file)
    # Iterate through the release folders
    for release_name in os.listdir(image_folder):
        if "Release" in release_name:
            os.chdir(f"{os.path.dirname(__file__)}/ImageJ")
            # Make release folders
            os.makedirs(f"sporetraps/images/{release_name}", exist_ok=True)
            os.makedirs(f"sporetraps/results/{release_name}", exist_ok=True)
            current_release = os.path.join(image_folder, release_name)
            # Iterate through the image folders
            for trap_name in sorted(
                os.listdir(current_release),
                key=lambda x: int(x[1:]),
            ):
                current_trap = os.path.join(
                    current_release, f"{trap_name}/{trap_name}_N0000"
                )
                # Clean out unnecessary extraneous files
                for file in os.listdir(current_trap):
                    if not (file.startswith("Tile0") and file.endswith(".tif")):
                        os.remove(f"{current_trap}/{file}")
                # Check if the album has already been processed
                if os.path.exists(
                    f"sporetraps/images/{release_name}/{trap_name}_N0000.tif"
                ):
                    if os.path.exists(
                        f"sporetraps/results/{release_name}/Results_{trap_name}_N0000.csv"
                    ):
                        print(f"Skipping folder: {current_trap}, already processed.")
                        continue
                print(f"Processing folder: {current_trap}")
                processed += 1

                # Execute the ImageJ macro for the current folder
                command = [
                    "./ImageJ.exe",
                    "-macro",
                    "sporetraps/AnalyzeSporeTrap.ijm",
                    current_trap,
                ]

                try:
                    subprocess.run(command, capture_output=True, text=True, check=True)
                except subprocess.CalledProcessError as exception:
                    print(f"Error executing the macro: {exception}")

                # Relocate output files into their respective release folders
                if os.path.exists(f"sporetraps/images/{trap_name}_N0000.tif"):
                    os.rename(
                        f"sporetraps/images/{trap_name}_N0000.tif",
                        f"sporetraps/images/{release_name}/{trap_name}_N0000.tif",
                    )
                if os.path.exists(f"sporetraps/results/Results_{trap_name}_N0000.csv"):
                    os.rename(
                        f"sporetraps/results/Results_{trap_name}_N0000.csv",
                        f"sporetraps/results/{release_name}/Results_{trap_name}_N0000.csv",
                    )

            # Process the ImageJ results
            for file in sorted(
                os.listdir(f"sporetraps/results/{release_name}"),
                key=lambda x: int(x.split("_")[1][1:]),
            ):
                if file.endswith(".csv"):
                    analyze_sporetraps.main(f"sporetraps/results/{release_name}/{file}")

    # Compile the results into a workbook
    compile_workbook.main()

    # Reformat the workbook
    format_workbook.main(workbook_file)

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    # Print elapsed time in H:M:S format
    print(f"\nElapsed time: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}")
    print(f"Albums processed: {processed}")
    input("Batch processing complete. Press ENTER.\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        IMAGE_FOLDER = sys.argv[1]
    else:
        IMAGE_FOLDER = f"{os.path.dirname(__file__)}/ECHO Images"
    batch_process(IMAGE_FOLDER)
