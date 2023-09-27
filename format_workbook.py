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
    docstring
"""

import csv
import os
import sys
import openpyxl
from openpyxl.styles import Font


def add_colors(sheet, position_column_index):
    """docstring"""
    # Create a dictionary to map values to font colors
    value_color_mapping = {
        "1": "FF0000",  # Red
        "2": "00FF00",  # Green
        "3": "0000FF",  # Blue
        "4": "C0C0C0",  # Silver
        "5": "FFD700",  # Gold
    }

    # Iterate through rows starting from the second row
    for row in sheet.iter_rows(
        min_row=2, min_col=position_column_index, max_col=position_column_index
    ):
        for cell in row:
            cell_value = str(cell.value)  # Convert cell value to string
            if cell_value in value_color_mapping:
                # Change the font color based on the value
                font_color = value_color_mapping[cell_value]
                cell.font = Font(color=font_color)


def add_notations(notes_file, sheet, trap_column_index, position_column_index):
    """docstring"""
    # Load up the notations
    matching_values = []
    with open(notes_file, "r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            matching_values.append(row)

    # Iterate through rows
    for row in sheet.iter_rows(
        min_row=2, min_col=trap_column_index, max_col=position_column_index
    ):
        trap_value = row[0].value
        position_value = str(row[1].value)
        # Add notations if available
        for match_data in matching_values:
            if (
                match_data["Trap"] == trap_value
                and match_data["Position"] == position_value
            ):
                sheet.cell(row=row[0].row, column=4, value=match_data["Notes"])


def format_workbook(filename):
    """docstring"""
    # Load the Excel file
    workbook = openpyxl.load_workbook(filename)

    # Iterate through each sheet in the workbook
    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]

        # Find the column index of "Position"
        position_column_index, trap_column_index = None, None
        for col_index, cell in enumerate(sheet[1], start=1):
            if cell.value == "Trap":
                trap_column_index = col_index
            elif cell.value == "Position":
                position_column_index = col_index
            if trap_column_index and position_column_index:
                break

        # Add colors to the position column
        add_colors(sheet, position_column_index)

        # Add any relevant notations to the workbook
        notes_file = f"{os.path.dirname(__file__)}/notes/{sheet_name}.csv"
        if os.path.exists(notes_file):
            add_notations(notes_file, sheet, trap_column_index, position_column_index)

    # Save the modified workbook in-place
    workbook.save(filename)
    # Close the workbook
    workbook.close()

    print(f"Workbook: {os.path.basename(filename)} has been reformatted.")


def main(filename):
    """Execute main objective."""
    os.chdir(os.path.dirname(__file__))
    format_workbook(filename)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        sys.exit(f"Usage: python3 {__file__} [FILE]")
