import copy

class Solution(object):
    def __init__(self):
        self.free_rolls = 0
        self.max_neighbors = 4

        self.height = 0
        self.width = 0

    def check(self, grid):
        self.grid = grid
        self.debug_grid = copy.deepcopy(grid)
        self.height = len(grid)
        self.width = len(grid[0].strip())

        for row in range(self.height):
            for column in range(self.width):
                if self.grid[row][column] == "@":
                    neighbors = self.check_neighbors(row, column)

                    if neighbors < self.max_neighbors:
                        self.free_rolls += 1
                        str_row = self.debug_grid[row]
                        self.debug_grid[row] = str_row[:column] + "x" + str_row[column+1:]

    def check_neighbors(self, row, column):
        checks = [ 
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        neighbors = 0
        for check in checks:
            if self.get_status(row + check[0], column + check[1]):
                neighbors += 1
        return neighbors

    def get_status(self, row, column):
        if row < 0:
            return False
        elif row >= self.height:
            return False
        elif column < 0:
            return False
        elif column >= self.width:
            return False
        else:
            if self.grid[row][column] == ".":
                return False
        return True


if __name__ == "__main__":
    grid = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@.",
    ]

    test = True
    test = False

    s = Solution()
    if test:
        s.check(grid)
    else:
        with open("input", "r") as f:
            s.check(f.readlines())

    print(f"Free Rolls = {s.free_rolls}")
    for row in s.debug_grid:
        print(row)
