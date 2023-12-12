# Solves a SAT instance on stdin and prints the result on stdout.

import fileinput

from pysat.solvers import Glucose4
from pysat.formula import CNF


def solve(input_string):
    f = CNF(from_string=input_string)

    g = Glucose4(f)
    g.solve()

    return g.get_model()
