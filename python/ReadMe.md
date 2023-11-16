# AoC Utilities
Some Python utilities to make Advent of Code development a bit easier.

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
* Functions `part1` and `part2` that are helpful to print the results for each part using colored (magenta) text. This helps it stand out from other debug text you might have.
* Simple timer functions that let you create a named timer that you can start and stop.
* A Grid class to help with grid based problems - (INCOMPLETE)

## Useful aliases
I've setup a few aliases to help with some common commands. In particular, is the alias that sets up a new day.
```
alias aoc='./${PWD##*/}.py'
alias aoc_lock="touch .aoc_lock"
alias aoc_unlock="rm -f .aoc_lock"
aoc_newday() {
    if [ -z $1 ]; then echo "Usage: ${FUNCNAME[0]} <day of month> [event year]"; return; fi
    yr=$(date +'%Y') # current year
    if [ ! -z $2 ]
    then
        yr="$2"
    fi
    if [ ! -f "/home/$USER/src/advent/$yr/day${1}/.aoc_lock" ]; then
       /home/$USER/src/advent/python/newday.py $1 $yr
       cd "/home/$USER/src/advent/$yr/day${1}"
    else
       echo "Day ${1}, Year $yr is LOCKED, aborting..."
    fi
}
```
The command `aoc` will run the current day's script, which then automatically looks for an input file called `input` - since it's the same for both Part 1 and Part 2. You can optionally pass in any other input file, such as `aoc test1` to run your script against `test1` input.

The commands `aoc_lock` and `aoc_unlock` will touch/delete a file in the current day's directory, preventing the files from being overwritted if you were to issue the `aoc_newday` command again, errantly.

The `aoc_newday` command is the most useful right after midnight. It takes the day of the month for a given puzzle and performs the operations listed above in the `newday.py` section. You can also use this for puzzle days from years past. Obviously, the `aoc_newday` alias would need to be modified for your directory structure, etc.