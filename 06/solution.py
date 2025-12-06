import copy

class Solution(object):
    def __init__(self):
        self.answer = 0
        self.ianswers = []

    def check(self, lines):
        self.combine(lines)
        self.do_math()

    def combine(self, lines):
        items = []

        index = 0
        for line in lines:
            li = []
            for indiv in line.split():
                indiv = indiv.strip()
                if index < 4:
                    indiv = int(indiv)
                li.append(indiv)
            items.append(li)
            index += 1

        self.problems = []
        for i in range(len(items[1])):
            p = []
            for j in range(len(items)):
                p.append(items[j][i])
            
            self.problems.append(p)

    def do_math(self):
        for p in self.problems:
            if p[4] == "+":
                a = p[0] + p[1] + p[2] + p[3]
                self.ianswers.append(a)
                self.answer += a
            elif p[4] == "*":
                a = p[0] * p[1] * p[2] * p[3]
                self.ianswers.append(a)
                self.answer += a
            else:
                raise RuntimeError(f"{p}")


if __name__ == "__main__":
    input = [
        "123 328  51 64 ",
        "45 64  387 23 ",
        "6 98  215 314",
        "1 0 1 0"
        "*   +   *   +  ",
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
    print(s.ianswers)

