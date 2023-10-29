# Trash-collecting robot problem
Given a maze with robot R and trashes T,
the goal for the robot is to collect all the trashes walking the shortest route possible.

## Usage
`./run.sh <input_path> <approach_number>`
        
Approaches:
1. greedily to the closest trash using BFS
2. optimally using A* with minimum spanning tree heuristic

Sample call:
`./run.sh test 2.txt 2`

## Approaches

### Greedy BFS - aprroach 1
A state space is just the input encoded as a graph.
A state in a state space is a position of the robot.

Using the BFS, the robot finds the nearest trash and goes for it.
This is repeated until all trashes are collected.

### Optimal BFS (A* with zero heuristic) - not implemented
A state in a state space is position of the robot AND a list of remaining trashes.

Using the BFS in this state space, the robot can find the optimal solution but many states are opened.

### Optimal A* with minimum spanning tree heuristic - approach 2
Same state space as in the optimal BFS variant.

The optimal solution is found as well but with much less states opened. 


## Performance

### Maze 1
| approach            | route length | states opened |
|---------------------|--------------|---------------|
| greedy BFS          | 128          | 1 825         |
| optimal BFS         | 128          | 43 153        |
| optimal A* with MST | 128          | 1 113         |

### Maze 2
| approach            | route length | states opened |
|---------------------|--------------|---------------|
| greedy BFS          | 79           | 378           |
| optimal BFS         | 62           | 2 757         |
| optimal A* with MST | 62           | 215           |

### Maze 3
| approach            | route length | states opened |
|---------------------|--------------|---------------|
| greedy BFS          | 184          | 3 056         |
| optimal BFS         | 163          | 603 446       |
| optimal A* with MST | 163          | 895           |

### Maze 4
| approach            | route length | states opened |
|---------------------|--------------|---------------|
| greedy BFS          | 16           | 32            |
| optimal BFS         | 11           | 70            |
| optimal A* with MST | 11           | 34            |