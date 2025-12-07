import copy

class Solution(object):
    def __init__(self):
        self.answer = 0
        self.layout = []

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

    def build_layout(self, lines):
        for line in lines:
            stage = []
            for c in line.strip():
                if c == "S":
                    c = "|"
                stage.append(c)
            self.layout.append(stage)

    def split_line(self, li):
        # propigate easy ones down
        for c in range(self.llen):
            if self.layout[li-1][c] == "|":
                if not self.layout[li][c] == "^":
                    self.layout[li][c] = "|"

        # add splits
        for c in range(self.llen):
            if self.layout[li][c] == "^" and self.layout[li-1][c] == "|":
                self.answer += 1
                if self.layout[li][c-1] == "." or self.layout[li][c+1] == ".":
                    #self.answer += 1
                    pass

                self.layout[li][c-1] = "|"
                self.layout[li][c+1] = "|"

    def beam_line(self, li):
        for c in range(self.llen):
            if self.layout[li-1][c] == "|":
                self.layout[li][c] = "|"

    def print_layout(self, to_line=None):
        if not to_line:
            to_line = len(self.layout)

        l = 0
        while l < to_line:
            print("".join(self.layout[l]))
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
