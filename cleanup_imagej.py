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

"""This script removes the files created by AnalyzeSporeTrap.ijm."""

import os
import shutil


def cleanup_imagej():
    """Clean up any results files that exist."""
    print("Cleaning up ImageJ files...")
    imagej_path = "ImageJ/sporetraps"
    removed = 0
    for folder in os.listdir(f"{imagej_path}/images"):
        current_folder = os.path.join(f"{imagej_path}/images", folder)
        if os.path.isdir(current_folder):
            print(f"Removing: {current_folder}.")
            shutil.rmtree(current_folder)
            removed += 1
    for folder in os.listdir(f"{imagej_path}/results"):
        current_folder = os.path.join(f"{imagej_path}/results", folder)
        if os.path.isdir(current_folder):
            print(f"Removing: {current_folder}.")
            shutil.rmtree(current_folder)
            removed += 1
    print(f"Cleanup complete. Deleted {removed} Release folders.")
    input("Press ENTER to exit.\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    cleanup_imagej()
