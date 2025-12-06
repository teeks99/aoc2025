import copy

class Solution(object):
    def __init__(self):
        self.answer = 0

    def check(self, lines):
        self.ranges = []
        self.good_ranges = []
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

        self.dedup_ranges()
        self.total_ranges()

    def search(self):
        for ingredient in self.ingredients:
            if self.check_fresh(ingredient):
                self.answer += 1

    def check_fresh(self, ingredient):
        ingredient = int(ingredient)
        for arange in self.ranges:
            start, end = arange.split("-")
            start = int(start)
            end = int(end)

            if ingredient >= start and ingredient <= end:
                return True
        return False
    
    def dedup_ranges(self):
        self.numrs = {}
        for r in self.ranges:
            start, end = r.split("-")
            start = int(start)
            end = int(end)
            index = start
            
            if index in self.numrs and self.numrs[index][1] >= end:
                pass
            else:
                self.numrs[index] = [start, end]

        self.numrs = list(dict(sorted(self.numrs.items())).values())

        index = 0
        while index < len(self.numrs) - 1:
            overlap = True
            increment = 1
            while overlap:
                if index + increment >= len(self.numrs):
                    break

                ts = self.numrs[index][0]
                te = self.numrs[index][1]

                os = self.numrs[index + increment][0]
                oe = self.numrs[index + increment][1]

                assert os >= ts

                if oe <= te:
                    self.numrs.pop(index + increment)
                elif os <= te:
                    self.numrs[index][1] = oe
                    self.numrs.pop(index + increment)
                elif os > te:
                    overlap = False

            index += 1

        self.good_ranges = self.numrs

    def total_ranges(self):
        for arange in self.good_ranges:
            start, end = arange

            self.answer += (end + 1) - start


if __name__ == "__main__":
    input = [
        "3-5", #3
        "10-14", #5
        "16-20", #5
        "12-18", #1
        "22-23", #2
        "21-24", #2
        "32-33", #2
        "34-35", #2
        "31-36", #2
        "42-43", #2
        "45-46", #2
        "41-47", #3
        "50-50", #1
        "",  #total = 32
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
    #print(s.good_ranges)
    #for i in s.good_ranges:
    #    print(i)

