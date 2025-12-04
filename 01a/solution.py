
min = 0
max = 99

class Solution(object):
    def __init__(self):
        self.position = 50
        self.total_zeros = 0
        self.click_zeros = 0

    def left(self, distance):
        for i in range(distance):
            if self.position == min:
                self.position = max
            else:
                self.position -= 1

            if self.position == min:
                self.click_zeros += 1

        print(f" to {self.position}")
        
        if self.position == min:
            self.total_zeros += 1

    def right(self, distance):
        for i in range(distance):
            if self.position == max:
                self.position = min
            else:
                self.position += 1

            if self.position == min:
                self.click_zeros += 1

        print(f" to {self.position}")

        if self.position == min:
            self.total_zeros += 1

    def make_turn(self, code):
        print(code.strip(), end='')
        direction = code[0]
        distance = int(code[1:].strip())

        if direction == "L":
            self.left(distance)
        else:
            self.right(distance)

    def sequence(self, turns):
        for turn in turns:
            self.make_turn(turn)

if __name__ == "__main__":
    test = [
        "L68",
        "L30",
        "R48",
        "L5",
        "R60",
        "L55",
        "L1",
        "L99",
        "R14",
        "L82",
        "R67",
        "R1",
    ]

    s = Solution()
    #s.sequence(test)

    with open("input", "r") as f:
        s.sequence(f.readlines())

    print(f"Number of zeros {s.total_zeros}")
    print(f"Number of click zeros {s.click_zeros}")
    