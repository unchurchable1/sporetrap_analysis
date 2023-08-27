# sporetrap analysis
This project is composed of Python scripts and ImageJ macros for use with\
images taken for the fluorescent microsphere particle release experiment.

## License
This project is licensed under the GNU General Public License v3.0.
For more details, please see the LICENSE file.

## Installation
1) Install Python 3.9 or 3.10.
2) Install the additional required dependencies:\
    Windows: Run setup/InstallDependencies.bat\
    Linux: Untested/Unsupported\
    Mac: Untested/Unsupported

## Usage
1) Place image albums into the "ECHO Images" directory.\
    Folders should retain the /Release #/Trap #/ structure, e.g.:\
    ECHO Images/Release 1/T1/T1_N0000/ ...
2) Run batch_process.py to process the image albums.\
    Results will be compiled into an Excel spreadsheet in this directory.

## TODO
- better filtering of artifacts
