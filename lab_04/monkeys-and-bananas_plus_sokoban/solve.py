import fileinput
import tempfile
import subprocess

from transform_to_pddl import PDDL_Creator


pddl_creator = PDDL_Creator()
pddl = pddl_creator.create_PDDL(fileinput.input())

script = f"echo -n '{pddl}' | ./scorpion.sh inputs/monkey-and-bananas.pddl /dev/stdin"
subprocess.run(script, shell=True, capture_output=False)
