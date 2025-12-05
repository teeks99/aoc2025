import copy

class Solution(object):
    def __init__(self):
        self.answer = 0

    def check(self, lines):
        self.ranges = []
        self.ingredients = []

        found_blank = False
        for line in lines:
            line = line.strip()
            if not line:
                found_blank = True
            elif not found_blank:
                self.ranges.append(line)
            else:
                self.ingredients.append(line)

        #print(self.ranges)
        #print(self.ingredients)

        self.search()

    def search(self):
        for ingredient in self.ingredients:
            if self.check_fresh(ingredient):
                self.answer += 1

    def check_fresh(self, ingredient):
        ingredient = int(ingredient)
        for range in self.ranges:
            start, end = range.split("-")
            start = int(start)
            end = int(end)

            if ingredient >= start and ingredient <= end:
                return True
        return False

if __name__ == "__main__":
    input = [
        "3-5",
        "10-14",
        "16-20",
        "12-18",
        "",
        "1",
        "5",
        "8",
        "11",
        "17",
        "32",
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

