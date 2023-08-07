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

"""docstring goes here"""

import os
import subprocess
import sys
import time

import analyze_sporetraps


def batch_process(image_folder):
    """docstring goes here"""
    # Start the timer
    start_time = time.time()
    # Count how many albums are processed
    processed = 0
    # Iterate through the release folders
    for release_name in os.listdir(image_folder):
        if "Release" in release_name:
            os.chdir(f"{os.path.dirname(__file__)}/ImageJ")
            # Make release folders
            os.makedirs(f"sporetraps/images/{release_name}", exist_ok=True)
            os.makedirs(f"sporetraps/results/{release_name}", exist_ok=True)
            current_release = os.path.join(image_folder, release_name)
            # Iterate through the image folders
            for trap_name in os.listdir(current_release):
                current_trap = os.path.join(
                    current_release, f"{trap_name}/{trap_name}_N0000"
                )
                # Clean out unnecessary extraneous files
                for file in os.listdir(current_trap):
                    if not file.startswith("Tile0") and not file.endswith(".jpg"):
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
                for file in os.listdir("sporetraps/images"):
                    if file.startswith(trap_name) and file.endswith(".tif"):
                        os.rename(
                            f"sporetraps/images/{file}",
                            f"sporetraps/images/{release_name}/{file}",
                        )
                for file in os.listdir("sporetraps/results"):
                    if file.startswith(f"Results_{trap_name}") and file.endswith(
                        ".csv"
                    ):
                        os.rename(
                            f"sporetraps/results/{file}",
                            f"sporetraps/results/{release_name}/{file}",
                        )

            # Process the ImageJ results
            for file in sorted(
                os.listdir(f"sporetraps/results/{release_name}"),
                key=lambda x: int(x.split("_")[1][1:]),
            ):
                if file.endswith(".csv"):
                    analyze_sporetraps.main(f"sporetraps/results/{release_name}/{file}")

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
