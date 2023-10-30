#! /bin/bash


# script usage info
help() { printf '%s\n' "
Usage:  run.sh <input_path> <approach_number>
        
Approaches:
        1: greedily to the closest trash using BFS
        2: optimally using A* - minimum spanning tree heuristic
        3: optimally using A* - furthest trash plus remaining trashes heuristic
        4: optimally using A* - nearest trash heuristic
        5: optimally using A* - remaining trashes heuristic
        6: optimally using A* - zero heuristic
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
        python3 optimal-AStar-MST/main.py "$INPUT" 2
    ;;
    3)
        python3 optimal-AStar-MST/main.py "$INPUT" 3
    ;;
    4)
        python3 optimal-AStar-MST/main.py "$INPUT" 4
    ;;
    5)
        python3 optimal-AStar-MST/main.py "$INPUT" 5
    ;;
    6)
        python3 optimal-AStar-MST/main.py "$INPUT" 6
    ;;
    \?)  echo 'Error: Invalid option' >&2 ; help >&2 ; exit 1 ;;
esac
