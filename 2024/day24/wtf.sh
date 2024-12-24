#! /bin/bash

# z?? should be output of XOR except MSB
CANDIDATE_1=$(cat input.txt | grep '> z' | grep -v 'XOR' | grep -v 'z45$' | awk '{print $5}')

# all the XOR should have either x?? y?? for input, or z?? for output.
CANDIDATE_2=$(cat input.txt | grep ' XOR ' | grep -v '^x' | grep -v '^y' | grep -v '> z' | awk '{print $5}')

# input of OR should be always output of AND except for LSB
INPUT_OF_OR=$(cat input.txt | grep ' OR ' | awk '{ print $1; print $3 }' | sort -u)

OUTPUT_OF_AND=$(cat input.txt | grep -v 'x00 AND y00' | grep ' AND ' | awk '{ print $5 }' | sort -u)

CANDIDATE_3=$(comm -3 <(echo $INPUT_OF_OR | tr ' ' '\n') <(echo $OUTPUT_OF_AND | tr ' ' '\n'))

echo $CANDIDATE_1 $CANDIDATE_2 $CANDIDATE_3 | tr ' ' '\n' | sort -u | tr '\n' ',' | sed -e 's/,$//'
