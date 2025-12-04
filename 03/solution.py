from textwrap import wrap
from itertools import groupby

digits_to_collect = 12

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
            self.check_bank(bank.strip(), digits_to_collect)

    def check_bank(self, bank, digits):
        combined = ""
        last_max_loc = 0
        for i in range(digits):
            max = 0
            current_max_loc = 0

            trim_end = -1 * (digits - (i + 1))
            if trim_end  == 0:
                trim_end = None
            
            check_part = bank[last_max_loc:trim_end]
            for j in range(len(check_part)):
                if int(check_part[j]) > max:
                    max = int(check_part[j])
                    current_max_loc = j

            last_max_loc += current_max_loc + 1
            combined += str(max)

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
    # 987654321111 + 811111111119 + 434234234278 + 888911112111 = 3121910778619