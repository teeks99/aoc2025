

class Solution(object):
    def __init__(self):
        self.answer = 0

        self.links = {}

    def check(self, lines):
        self.load_input(lines)
        self.find_paths()

    def load_input(self, lines):
        for line in lines:
            node, connections = line.split(":")
            self.links[node] = tuple(connections.split())

    def find_paths(self):
        active_paths = {"you":1}
        while(len(active_paths)):
            node, count = active_paths.popitem()
            for conn in self.links[node]:
                if conn == "out":
                    self.answer += count
                else:
                    if conn in active_paths:
                        active_paths[conn] += count
                    else:
                        active_paths[conn] = count


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