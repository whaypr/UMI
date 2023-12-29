
class PDDL_Creator():

    def __init__(self):
        self.PDDL = ""

    def create_PDDL(self, input_stream):
        # LOAD AND PROCESS INPUT

        rows = [
            row.removesuffix("\n").split("|")[1:-1]
            for row in input_stream
            if not row.startswith("+")
        ]

        n_rows = len(rows)
        n_cols = len(rows[0])

        # keys: coordinates, values: names
        positions = {(r,c):f"position-{r}{c}" for r in range(1, n_rows+1) for c in range(1, n_cols+1)}

        # keys: names, values: coordinates
        monkeys = {}
        crates = {}
        bananas = {}

        for i, row in enumerate(rows, start=1):
            for j, item in enumerate(row, start=1):
                if item == 'M':
                    monkeys[f"monkey-{len(monkeys.keys())+1}"] = (i,j)
                if item == 'C':
                    crates[f"crate-{len(crates.keys())+1}"] = (i,j)
                if item == 'B':
                    bananas[f"bananas-{len(bananas.keys())+1}"] = (i,j)


        # CREATE PDDL

        self.__addLine("(define (problem sample-problem)", 0)
        self.__addLine("(:domain monkey-and-bananas)", 1)

        # setup objects
        self.__addLine("(:objects", 1)

        self.__addLine(self.__prepareObjects(monkeys.keys(), "monkey"))
        self.__addLine(self.__prepareObjects(crates.keys(), "crate"))
        self.__addLine(self.__prepareObjects(bananas.keys(), "bananas"))
        self.__addLine(self.__prepareObjects(positions.values(), "position"))

        self.__addLine(")", 1)

        # setup init state
        self.__addLine("(:init", 1)

        for name, coord in monkeys.items():
            self.__addLine(f"(not (up {name}))")
            self.__addLine(f"(at {name} {positions[coord]})")

        for name, coord in bananas.items():
            self.__addLine(f"(not (grabbed {name}))")
            self.__addLine(f"(at {name} {positions[coord]})")

        for name, coord in crates.items():
            self.__addLine(f"(movable {name})")
            self.__addLine(f"(at {name} {positions[coord]})")

        for coord, name in positions.items():
            if coord not in monkeys.values() and coord not in crates.values():
                self.__addLine(f"(empty {name})")

        for coord, name in positions.items():
            for other_coord in ((coord[0]-1, coord[1]), (coord[0], coord[1]-1), (coord[0], coord[1]+1), (coord[0]+1, coord[1])):
                if other_coord[0] <= 0 or other_coord[1] <= 0 or other_coord[0] > n_rows or other_coord[1] > n_cols:
                    continue 
                self.__addLine(f"(nextTo {name} {positions[other_coord]})")

        for coord, name in positions.items():
            x = coord[0]
            y = coord[1]

            if x + 2 <= n_rows:
                self.__addLine(f"(straightTriple {name} {positions[(x+1, y)]} {positions[(x+2, y)]})")
            if x >= 3:
                self.__addLine(f"(straightTriple {name} {positions[(x-1, y)]} {positions[(x-2, y)]})")
            if y + 2 <= n_cols:
                self.__addLine(f"(straightTriple {name} {positions[(x, y+1)]} {positions[(x, y+2)]})")
            if y >= 3:
                self.__addLine(f"(straightTriple {name} {positions[(x, y-1)]} {positions[(x, y-2)]})")

        self.__addLine(")", 1)

        # setup goals
        self.__addLine("(:goal (and", 1)

        for b in bananas:
            self.__addLine(f"(grabbed {b})")

        self.__addLine("))", 1)

        self.__addLine(")", 0)


        # RETURN PDDL

        return self.PDDL
    

    #                        HELPERS
    # -----------------------------------------------------------

    # helper method for adding lines to the output PDDL string
    def __addLine(self, text, n_indentations = 2):
        self.PDDL = self.PDDL + n_indentations*'\t' + text + "\n"

    # helper method for preparing objects
    def __prepareObjects(self, objectNames, typeName):
        line = ""
        for name in objectNames:
            line = line + f"{name} "
        line = line + f"- {typeName}"
        return line



#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

if __name__ == "__main__":
    import fileinput
    creator = PDDL_Creator()
    pddl = creator.create_PDDL(fileinput.input())
    print(pddl)
