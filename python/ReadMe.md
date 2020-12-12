# AoC Utilities
Some utilities to make Advent of Code development a bit easier.

## newday.<span>py
Performs a series of steps to prepare for a new day of AoC. It will:
* Create a new directory for the given `day` argument
   * This directory will be created in the `current year` folder, if `year` is not specified
* Copies `template.py` to the newly created directory
* Downloads the `input` file for the given day
   * This requires a file called `.cookie` that contains your AoC cookie

You can run the script over and over and it will *always* copy `tempalte.py` into `dayN.py`, where N is the day. To prevent this from happening, simply create a empty file called `.aoc_lock` in the `dayN` directory.

## template.<span>py
A boilerplate script that includes some common `import` statements and automatically reads/parses the `input` file. Also provides for optional arguments, which lets you pass in test input filenames

## aoc_utils.<span>py
A (poor) attempt to provide some useful functions for AoC puzzles. Highlights include:
* Functions `part` and `part2` that are helpful to print the results for each part using colored (magenta) text. This helps it stand out from other debug text you might have.
* Simple timer functions that let you create a named timer that you can start and stop.
* A Grid class to help with grid based problems - (INCOMPLETE)