import copy

class Solution(object):
    def __init__(self):
        self.answer = 0
        self.layout = []

        self.ends = 0
        self.max_end = 0

    def check(self, lines):
        self.build_layout(lines)

        self.llen = len(lines[1].strip())


        li = 1
        while li < len(lines):
            self.beam_line(li)
            li += 1
            if li < len(lines):
                self.split_line(li)
                li += 1
            #print(f"After line {li}:")
            #self.print_layout()

        self.sum_end()

        # li = 0
        # for i in range(self.llen):
        #     if self.layout[0][i] == "|":
        #         self.answer = self.num_paths(li + 2, i)
        #         break

    def num_paths(self, li, sc):
        if li >= len(self.layout):
            self.ends += 1
            if sc > self.max_end:
                self.max_end = sc
            if self.ends % 100 == 0:
                print(self.max_end)
            return 1
        
        if self.layout[li][sc] == ".":
            return self.num_paths(li + 2, sc)
        elif self.layout[li][sc] == "^":
            paths = 0
            paths += self.num_paths(li + 2, sc - 1)
            paths += self.num_paths(li + 2, sc + 1)
            return paths

    def build_layout(self, lines):
        for line in lines:
            stage = []
            for c in line.strip():
                if c == "S":
                    c = 1
                stage.append(c)
            self.layout.append(stage)

    def split_line(self, li):
        # propigate easy ones down
        for c in range(self.llen):
            if isinstance(self.layout[li-1][c], int):
                if not self.layout[li][c] == "^":
                    self.layout[li][c] = self.layout[li-1][c]

        # add splits
        for c in range(self.llen):
            if self.layout[li][c] == "^" and isinstance(self.layout[li-1][c], int):
                if self.layout[li][c-1] == ".":
                    self.layout[li][c-1] = self.layout[li-1][c]
                else:
                    self.layout[li][c-1] += self.layout[li-1][c]
                if self.layout[li][c+1] == ".":
                    self.layout[li][c+1] = self.layout[li-1][c]
                else:
                    self.layout[li][c+1] += self.layout[li-1][c]

    def beam_line(self, li):
        for c in range(self.llen):
            if isinstance(self.layout[li-1][c], int):
                self.layout[li][c] = self.layout[li-1][c]

    def sum_end(self):
        self.answer = 0
        for n in self.layout[-1]:
            if isinstance(n, int):
                self.answer += n

    def print_layout(self, to_line=None):
        if not to_line:
            to_line = len(self.layout)

        l = 0
        while l < to_line:
            s = ""
            for i in self.layout[l]:
                s += str(i)
            print(s)
            l += 1


if __name__ == "__main__":
    input = [
        ".......S.......",
        "...............",
        ".......^.......",
        "...............",
        "......^.^......",
        "...............",
        ".....^.^.^.....",
        "...............",
        "....^.^...^....",
        "...............",
        "...^.^...^.^...",
        "...............",
        "..^...^.....^..",
        "...............",
        ".^.^.^.^.^...^.",
        "...............",
    ]

    test = True
    test = False

    s = Solution()
    if test:
        s.check(input)
    else:
        with open("input", "r") as f:
            s.check(f.readlines())

    print(f"Answer = {s.answer}")
    #s.print_layout()
