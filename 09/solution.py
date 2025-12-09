import math

class Solution(object):
    def __init__(self):
        self.answer = 0
        self.red_coords = []
        self.map = []

        self.max_x = 0
        self.max_y = 0

        self.max_size = 0
        self.coords_max = []

    def check(self, lines):
        self.make_cords(lines)
        #self.make_map()
        #self.print_map(self.map)
        self.find_rectangles()
        self.answer = self.max_size

    def make_cords(self, lines):
        for line in lines:
            x, y = line.split(",")
            x = int(x)
            y = int(y)

            if x > self.max_x:
                self.max_x = x

            if y > self.max_y:
                self.max_y = y

            self.red_coords.append((x,y))

    def make_map(self):
        for i in range(self.max_y + 1):
            line = []
            for j in range(self.max_x + 1):
                line.append(None)
            self.map.append(line)

        for coord_id in range(len(self.red_coords)):
            x, y = self.red_coords[coord_id]
            if self.map[y][x]:
                raise RuntimeError(f"Matching coordinate found at {x},{y} - index {coord_id}")
            self.map[y][x] = coord_id

    def print_map(self, pmap):
        ms = []
        for row in pmap:
            line = ""
            for column in row:
                if isinstance(column, int):
                    line += "#"
                elif isinstance(column, str):
                    line += column
                else:
                    line += "."
            ms.append(line)

        for row in ms:
            print(row)

    def find_rectangles(self):
        for i in range(len(self.red_coords)):
            if i % 20 == 0:
                print(i)
            j = i + 1
            while j < len(self.red_coords):
                if i == j:
                    continue

                x1, y1 = self.red_coords[i]
                x2, y2 = self.red_coords[j]

                w = 0
                if x1 > x2:
                    w = x1 - x2 + 1
                else:
                    w = x2 - x1 + 1

                h = 0
                if y1 > y2:
                    h = y1 - y2 + 1
                else:
                    h = y2 - y1 + 1

                s = h * w
                if s == self.max_size:
                    self.coords_max.append((i,j))
                elif s > self.max_size:
                    self.max_size = s
                    self.coords_max = [(i,j)]

                j += 1




if __name__ == "__main__":
    input = [
        "7,1",
        "11,1",
        "11,7",
        "9,7",
        "9,5",
        "2,5",
        "2,3",
        "7,3",
    ]

    test = True
    test = False

    s = Solution()
    if test:
        s.num_connections = 10
        s.check(input)
    else:
        with open("input", "r") as f:
            s.check(f.readlines())

    print(f"Answer = {s.answer}")