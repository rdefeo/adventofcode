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
    if [ ! -f "/home/rdefeo/src/advent/$yr/day${1}/.aoc_lock" ]; then
        /home/rdefeo/src/advent/python/newday.py $1 $yr
        cd "/home/rdefeo/src/advent/$yr/day${1}"
    else
        echo "Day ${1}, Year $yr is LOCKED, aborting..."
    fi
}