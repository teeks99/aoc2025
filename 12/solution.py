import copy

class Solution(object):
    def __init__(self):
        self.answer = 0

        self.spaces = []
        self.combos = []
        self.minimal_combos = []

        self.max_width = 0
        self.max_height = 0

    def check(self, lines, presents):

        self.load_input(lines)
        self.load_presents(presents)

        self.simple_check_areas()


    def load_input(self, lines):
        for line in lines:
            size, quantities = line.split(":")
            width, height = size.split("x")
            quantities = quantities.split()

            width = int(width)
            height = int(height)
            quantities = list(map(int, quantities))

            if width > self.max_width:
                self.max_width = width
            if height > self.max_height:
                self.max_height = height

            self.spaces.append(Space(width, height, quantities))

    def load_presents(self, lines):
        index = 0
        line = 0
        while line < len(lines):
            if not lines[line].strip() == f"{index}:":
                raise RuntimeError("Line is off")
            quantities = [0] * 6
            quantities[index] = 1

            line += 1
            p = Present(lines[line:line+3])
            self.combos.append(Combination(p.grid, quantities))
            #for r in p.rotations:
            #    self.combos.append(Combination(r, quantities))
            line += 4
            index += 1

        self.minimal_combos = self.combos[:]

    def join(self, one, two, max_height, max_width):
        combos = []

    def simple_check_areas(self):
        self.answer = 0
        for space in self.spaces:
            space_needed = 0
            total_num = 0
            for q in range(len(space.quantities)):
                space_needed += space.quantities[q] * self.minimal_combos[q].occupied
                total_num += space.quantities[q]

            area = space.width * space.height
            slots3x3 = (1 + space.width // 3) * (1 + space.height // 3)

            if space_needed < area and total_num < slots3x3:
                self.answer += 1



class Combination(object):
    def __init__(self, grid, quantities):
        self.grid = grid
        self.rotations = None
        self.width = len(grid[0])
        self.height = len(grid)
        self.quantities = quantities
        self.density = 0

        self.occupied = 0
        for r in self.grid:
            for s in r:
                if s:
                    self.occupied += 1
        self.density = self.occupied / (self.width * self.height)

    def create_rotations(self):
        r = []
        r.append(self.grid)
        for rot in range(3):
            g2 = [[False] * 3] * 3
            g2[0][0] = r[-1][2][0]
            g2[0][1] = r[-1][1][0]
            g2[0][2] = r[-1][0][0]

            g2[1][0] = r[-1][2][1]
            g2[1][1] = r[-1][1][1]
            g2[1][2] = r[-1][0][1]
                    
            g2[2][0] = r[-1][2][2]
            g2[2][1] = r[-1][1][2]
            g2[2][2] = r[-1][0][2]

            g3 = []
            for row in g2:
                g3.append(tuple(row))
            r.append(tuple(g3))

        self.rotations = tuple(r)

class Space(object):
    def __init__(self, width, height, quantities):
        self.width = width
        self.height = height
        self.quantities = quantities

    def fill(self, presents):
        pass


class Present(object):
    def __init__(self, rows):
        self.rows = rows
        self.grid = ()

        self.rotations = ()

        self.create_grid()
        self.create_rotations()

    def create_grid(self):
        g = []
        for row in self.rows:
            r = []
            for c in row.strip():
                if c == "#":
                    r.append(True)
                elif c == ".":
                    r.append(False)
                else:
                    raise RuntimeError("Grid Creation")
            g.append(tuple(r))
        self.grid = tuple(g)

    def create_rotations(self):
        r = []
        r.append(self.grid)
        for rot in range(3):
            g2 = [[False] * 3] * 3
            g2[0][0] = r[-1][2][0]
            g2[0][1] = r[-1][1][0]
            g2[0][2] = r[-1][0][0]

            g2[1][0] = r[-1][2][1]
            g2[1][1] = r[-1][1][1]
            g2[1][2] = r[-1][0][1]
                    
            g2[2][0] = r[-1][2][2]
            g2[2][1] = r[-1][1][2]
            g2[2][2] = r[-1][0][2]

            g3 = []
            for row in g2:
                g3.append(tuple(row))
            r.append(tuple(g3))

        self.rotations = tuple(r)


if __name__ == "__main__":
    test = True
    test = False

    s = Solution()
    if test:
        input = []
        presents = []
        with open("tinput", "r") as f:
            input = f.readlines()
        with open("tinput-presents", "r") as f:
            presents = f.readlines()
        s.check(input, presents)
    else:
        input = []
        presents = []
        with open("input", "r") as f:
            input = f.readlines()
        with open("input-presents", "r") as f:
            presents = f.readlines()
        s.check(input, presents)

    print(f"Answer = {s.answer}")

# 267 - Too low