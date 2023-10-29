#! /bin/bash


# script usage info
help() { printf '%s\n' "
Usage:  run.sh <input_path> <approach_number>
        
Approaches:
        1: greedily to the closest trash using BFS
        2: optimally using A* with minimum spanning tree heuristic
"; }


# check the correct number of arguments
[[ $# != 2 ]] && { help >&2; exit 1; }


INPUT="$1"
ALGO="$2"

# run
case "$ALGO" in
    1)
        [ -f greedy-BFS/exec ] || ( cd greedy-BFS; make; )
        ./greedy-BFS/exec "$INPUT"
    ;;
    2)
        python3 optimal-AStar-MST/main.py "$INPUT"
    ;;
    \?)  echo 'Error: Invalid option' >&2 ; help >&2 ; exit 1 ;;
esac
