import fileinput
import itertools

import sys
sys.path.append('../utils')
import solve_SAT


# LOAD AND PREPROCESS INPUT

data = [set(x.strip("\n").split(" ")) for x in fileinput.input()]

max_subsets = int(data[0].pop())
universum = data[1]
total_subsets = len(data[2:])

# for item 'u' from the universum, this dict tells in which subsets it is 
u2s = {}
for i, subset in enumerate(data[2:], start=1):
    for item in subset:
        if item not in u2s.keys():
            u2s[item] = set()
        u2s[item].add(i)


# CREATE CNF

clauses = []

# for each item from the universum, define from which subsets it can be obtained
for subset_numbers in u2s.values():
    clause = " ".join(map(str, subset_numbers))
    clauses.append(clause)

# allow only 'max_subsets' subsets to be used
for comb in itertools.combinations(range(1, total_subsets + 1), max_subsets + 1):
    clause = "-" + " -".join(map(str, comb))
    clauses.append(clause)

cnf = f"p cnf {total_subsets} {len(clauses)}\n"
for c in clauses:
    cnf = cnf + c + " 0\n"
cnf = cnf.removesuffix("\n")

# SOLVE AND PRINT

print("CNF:", cnf, sep="\n")
print("--------------------")
print("SOLUTION:", solve_SAT.solve(cnf), sep="\n")
