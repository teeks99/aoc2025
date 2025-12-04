from textwrap import wrap
from itertools import groupby

class Solution(object):
    def __init__(self):
        self.bad_ids = []

    def check(self, input_str):
        ranges = input_str.split(",")
        for range in ranges:
            print(range)
            start, end = range.split("-")
            self.check_range(int(start), int(end))

    def check_range(self, start, end):
        for i in range(start, end+1):
            self.check_num(i)

    def check_num(self, input):
        test = str(input)

        length = len(test)
        for split_len in range(1,length+1):
            if length % split_len == 0:
                sections = wrap(test, int(length / split_len))
                if len(sections) == 1:
                    continue
                uncommon = set(sections)

                if len(uncommon) == 1:
                    print(test)
                    self.bad_ids.append(input)
                    break

        # if len(test) % 2 == 0:
        #     half = int(len(test) / 2)
        #     first = test[half:]
        #     second = test[:half]
        #     if first == second:
        #         print(test)
        #         self.bad_ids.append(input)

    def sum_ids(self):
        sum = 0
        for bad_id in self.bad_ids:
            sum += bad_id

        return sum


if __name__ == "__main__":
    test_input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

    s = Solution()
    #s.check(test_input)

    with open("input", "r") as f:
        s.check(f.read().strip())

    print(f"Sum = {s.sum_ids()}")