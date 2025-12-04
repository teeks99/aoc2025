from textwrap import wrap
from itertools import groupby

class Solution(object):
    def __init__(self):
        self.bankmax = []

    def total_jolts(self):
        sum = 0
        for bank in self.bankmax:
            sum += int(bank)
        return sum

    def check(self, banks):
        for bank in banks:
            self.check_bank(bank.strip())

    def check_bank(self, bank):
        first_max = 0
        first_max_loc = 0

        start = bank[:-1]

        for i in range(len(start)):
            if int(start[i]) > first_max:
                first_max = int(start[i])
                first_max_loc = i

        remaining = bank[first_max_loc+1:]
        second_max = 0

        for c in remaining:
            if int(c) > second_max:
                second_max = int(c)

        combined = f"{first_max}{second_max}"
        print(f"{bank} - {combined}")
        self.bankmax.append(combined)

if __name__ == "__main__":
    banks = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111",
    ]

    s = Solution()
    #s.check(banks)

    with open("input", "r") as f:
        s.check(f.readlines())

    print(f"Sum = {s.total_jolts()}")