import math
import re

class Machine(object):
    def __init__(self, line):
        self.line = line

        self.desired_pattern = ()
        self.buttons = ()
        self.joltage = []

        self.presses = 0

        self.parse(line)

    def parse(self, line):
        # 1. Define a pattern to separate the three main sections
        #    Group 1: [.##.] -> captures .##.
        #    Group 2: The middle section with parentheses
        #    Group 3: {3,5,4,7} -> captures 3,5,4,7
        pattern = r"\[([.#]+)\]\s+(.*?)\s+\{([\d,]+)\}"
        match = re.search(pattern, line)

        if match:
            lights_str, bwire_raw, joltage_str = match.groups()

            # --- Parse Lights ---
            # Map '.' to False and '#' to True
            self.desired_pattern = tuple(char == '#' for char in lights_str)

            # --- Parse Bwire ---
            # Find all items inside parentheses: (3) or (1,3)
            # Convert them into a list of tuples
            bwire_matches = re.findall(r"\(([\d,]+)\)", bwire_raw)
            self.buttons = [tuple(map(int, item.split(','))) for item in bwire_matches]

            # --- Parse Joltage ---
            # Split by comma and convert to integers
            self.joltage = [int(x) for x in joltage_str.split(',')]

    def find_presses(self):
        pattern = [False]*len(self.desired_pattern)

        self.presses = 1
        found = False
        sequences = []
        for b in range(len(self.buttons)):
            sequences.append(ButtonSequence(self.desired_pattern, self.buttons, pattern, [], b))

        while not found:
            for s in sequences:
                if s.check():
                    return self.presses
            current_patterns = []

            s2 = []
            for s in sequences:
                if s.int_pattern in current_patterns:
                    pass
                else:
                    current_patterns.append(s.int_pattern)
                    s2.append(s)

            s3 = []
            for s in s2:
                s3 += s.next_level()

            sequences = s3

            self.presses += 1

class ButtonSequence(object):
    def __init__(self, desired_pattern, buttons, current_pattern, presses, new_button):
        self.desired_pattern = desired_pattern
        self.buttons = buttons
        self.current_pattern = current_pattern[:]
        self.int_pattern = 0
        self.presses = presses[:]
        self.presses.append(new_button)

    def check(self):
        for w in self.buttons[self.presses[-1]]:
            self.current_pattern[w] = not self.current_pattern[w]

        self.set_int_pattern()
        return self.pattern_matches(self.current_pattern)

    def pattern_matches(self, pattern):
        for i in range(len(self.desired_pattern)):
            if pattern[i] != self.desired_pattern[i]:
                return False
        return True
    
    def set_int_pattern(self):
        self.int_pattern = 0
        for bit in self.current_pattern:
            self.int_pattern = (self.int_pattern << 1) | bit
    
    def next_level(self):
        next = []
        for b in range(len(self.buttons)):
            next.append(ButtonSequence(self.desired_pattern, self.buttons, self.current_pattern, self.presses, b))
        return next


class Solution(object):
    def __init__(self):
        self.answer = 0
        self.presses = []

        self.machines = []

    def check(self, lines):
        self.load_input(lines)
        i = 0
        for m in self.machines:
            p = m.find_presses()
            print(f"Needed {p} presses for machine {i}")
            self.answer += p
            i += 1

    def load_input(self, lines):
        for line in lines:
            self.machines.append(Machine(line))

if __name__ == "__main__":
    test = True
    test = False

    s = Solution()
    if test:
        s.num_connections = 10
        with open("tinput", "r") as f:
            s.check(f.readlines())
    else:
        with open("input", "r") as f:
            s.check(f.readlines())

    print(f"Answer = {s.answer}")