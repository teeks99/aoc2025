import copy

class Solution(object):
    def __init__(self):
        self.answer = 0
        self.ianswers = []
        self.problems = []

    def check(self, lines):
        self.combine(lines)
        self.do_math()

    def combine(self, lines):
        items = []

        index = 0
        math_rows = 4
        while index < len(lines[math_rows]):
            assert lines[4][index] in ["*", "+"]

            next_index = index
            while next_index + 1 < len(lines[4]) and not lines[4][next_index + 1] in ["*", "+"]:
                next_index += 1
            next_index += 1

            operator = lines[math_rows][index]

            p = []
            while index < next_index:
                n = ""
                for i in range(math_rows):
                    n += lines[i][index]
                if n.strip() == "":
                    pass
                else:
                    n = int(n)
                    p.append(n)
                index += 1
            p.append(operator)

            self.problems.append(p)

        # for line in lines:
        #     li = []
        #     for indiv in line.split():
        #         indiv = indiv.strip()
        #         if index < 4:
        #             indiv = int(indiv)
        #         li.append(indiv)
        #     items.append(li)
        #     index += 1

        # self.problems = []
        # for i in range(len(items[1])):
        #     p = []
        #     for j in range(len(items)):
        #         p.append(items[j][i])
            
        #     self.problems.append(p)

    def do_math(self):
        for p in self.problems:
            if p[-1] == "+":
                a = 0
                for i in p[:-1]:
                    if i:
                        a += i
                self.ianswers.append(a)
                self.answer += a
            elif p[-1] == "*":
                a = 1
                for i in p[:-1]:
                    if i:
                        a *= i
                self.ianswers.append(a)
                self.answer += a
            else:
                raise RuntimeError(f"{p}")


if __name__ == "__main__":
    input = [
        "123 328  51 64 ",
        " 45 64  387 23 ",
        "  6 98  215 314",
        "               ",
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

