# ndpis_to_afi

A Python utility to convert `.ndpis` file lists (from Hamamatsu NanoZoomer) into `.afi` (Leica / XML Image List) files.

## Overview

This script recursively scans a specified directory for `.ndpis` files. For each file found, it parses the content to identify associated `.ndpi` images and their channel suffixes, then generates a corresponding `.afi` XML file in the same location.

## Usage

Run the script from the command line, providing the path to the root directory you want to scan:

```bash
python ndpis2afi.py /path/to/data_folder
```
