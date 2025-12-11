import math
import re

class Machine(object):
    def __init__(self, line):
        self.max_sequences = 5000

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
            self.joltage = tuple(int(x) for x in joltage_str.split(','))

    def find_presses(self):
        pattern = [0]*len(self.desired_pattern)
        found_patterns = []

        self.presses = 1
        found = False
        sequences = []
        for b in range(len(self.buttons)):
            sequences.append(ButtonSequence(self.joltage, self.buttons, pattern, [], b))

        while len(sequences) > 0:
            for s in sequences:
                if s.check():
                    return self.presses

            s2 = []
            for s in sequences:
                if s.current_pattern in found_patterns:
                    pass
                elif s.any_above():
                    pass
                else:
                    found_patterns.append(s.current_pattern)
                    s2.append(s)

            s3 = []
            for s in s2:
                s3 += s.next_level()

            sequences = sorted(s3, key=lambda s: s.sum, reverse=True)
            if len(sequences) > self.max_sequences:
                sequences = sequences[:self.max_sequences]

            self.presses += 1
        raise RuntimeError(f"Failed to find sequence with max: {self.max_sequences}")

class ButtonSequence(object):
    def __init__(self, desired_pattern, buttons, current_pattern, presses, new_button):
        self.desired_pattern = desired_pattern
        self.buttons = buttons
        self.current_pattern = current_pattern
        self.presses = presses[:]
        self.presses.append(new_button)
        self.sum = 0

    def check(self):
        cp = list(self.current_pattern)
        for w in self.buttons[self.presses[-1]]:
            cp[w] += 1

        self.current_pattern = tuple(cp)
        self.create_sum()
        return self.pattern_matches(self.current_pattern)
    
    def any_above(self):
        for i in range(len(self.desired_pattern)):
            if self.current_pattern[i] > self.desired_pattern[i]:
                return True
        return False
    
    def create_sum(self):
        self.sum = 0
        for j in self.current_pattern:
            self.sum += j

    def pattern_matches(self, pattern):
        for i in range(len(self.desired_pattern)):
            if pattern[i] != self.desired_pattern[i]:
                return False
        return True

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