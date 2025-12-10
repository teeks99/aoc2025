import math

class Solution(object):
    def __init__(self):
        self.answer = 0
        #self.num_connections = 1000
        self.num_connections = 1000000000000000

        self.point_ids = {}
        self.distances = {}
        #self.distances = []
        #self.distances_points = []
        self.circuits = []

    def check(self, lines):
        self.id_points(lines)
        self.calc_distances()
        self.build_circuits()

        self.find_unconnected()

    def id_points(self, lines):
        index = 0
        for line in lines:
            x, y, z = line.split(",")
            x = int(x)
            y = int(y)
            z = int(z)

            self.point_ids[index] = (x, y, z)
            index += 1

    def calc_distances(self):
        allds = {}
        for i in range(len(self.point_ids)):
            if i % 10 == 0:
                #print(f"Distances from {i}")
                pass
            for j in range(i + 1, len(self.point_ids)):
                x = (self.point_ids[i][0] - self.point_ids[j][0]) ** 2
                y = (self.point_ids[i][1] - self.point_ids[j][1]) ** 2
                z = (self.point_ids[i][2] - self.point_ids[j][2]) ** 2

                d = math.sqrt(x + y + z)

                if d in allds:
                    raise RuntimeError(f"{d} already existed")

                allds[d] = (i,j)

        self.distances = dict(sorted(allds.items()))
        #print(len(self.distances))

    def build_circuits(self):
        conn = 0
        plenty_of_circuits = False
        for d, p in self.distances.items():

            already_in = False
            # ci = 0
            # while ci < len(self.circuits):
            #     if p[0] in self.circuits[ci] and p[1] in self.circuits[ci]:
            #         already_in = True
            #         break
            #     ci += 1

            ci = 0
            if not already_in:
                existing = None
                while ci < len(self.circuits):
                    if p[0] in self.circuits[ci] or p[1] in self.circuits[ci]:
                        if existing == None:
                            self.circuits[ci].add(p[0])
                            self.circuits[ci].add(p[1])
                            existing = ci
                        else:
                            #print(f"{p} - {self.circuits[existing]} - {self.circuits[ci]}")
                            self.circuits[existing] = self.circuits[existing].union(self.circuits[ci])
                            t = self.circuits[:existing] + self.circuits[existing+1:]
                            self.circuits = self.find_new_dups(self.circuits[existing], t)
                            break
                    ci += 1

                if existing == None:
                    c = {p[0], p[1]}
                    self.circuits.append(c)

            if not plenty_of_circuits:
                if len(self.circuits) > 4:
                    plenty_of_circuits = True

            if plenty_of_circuits and len(self.circuits) == 2:
                pass

            if plenty_of_circuits and len(self.circuits) == 1:
                all_in = True
                for i in self.point_ids.keys():
                    if not i in self.circuits[0]:
                        all_in = False
                        print(f"Point not in circuit {i}")
                if all_in:
                    print(f"All in one circuit with points {p[0]} and {p[1]}")
                    result = self.point_ids[p[0]][0] * self.point_ids[p[1]][0]
                    print(f"Multiplied Xs: {result}")
                    raise Exception("Done")

            #self.check_dups()

            if not already_in:
                conn += 1
            if conn >= self.num_connections:
                break

        long_circuits = []
        for c in self.circuits:
            #print(len(c))
            found = False
            for i in range(len(long_circuits)):
                if len(c) > len(long_circuits[i]):
                    long_circuits.insert(i, c)
                    found = True
                    break
            if not found:
                long_circuits.append(c)


        self.answer = 1
        for c in long_circuits[:3]:
            self.answer *= len(c)

    def find_new_dups(self, test, remainder):
        dup_here = False
        for c in test:
            i = 0
            while i < len(remainder):
                if c in remainder[i]:
                    #print(f"fnd - {test} - {remainder[i]}")
                    test = test.union(remainder[i])
                    t = remainder[:i] + remainder[i+1:]
                    return self.find_new_dups(test, t)
                i += 1

        remainder.append(test)
        return remainder

    def check_dups(self):
        i = 0
        while i < len(self.circuits):
            for c in self.circuits[i]:
                o = i + 1
                while o < len(self.circuits):
                    if c in self.circuits[o]:
                        print(f"Dup found {i} {o} - {c}")
                    o += 1
            i += 1

    def find_unconnected(self):
        pts = list(self.point_ids.keys())

        for c in self.circuits:
            for p in c:
                pts.remove(p)

        for p in pts:
            print(f"{p} - {self.point_ids[p]}")

if __name__ == "__main__":
    input = [
        "162,817,812",
        "57,618,57",
        "906,360,560",
        "592,479,940",
        "352,342,300",
        "466,668,158",
        "542,29,236",
        "431,825,988",
        "739,650,466",
        "52,470,668",
        "216,146,977",
        "819,987,18",
        "117,168,530",
        "805,96,715",
        "346,949,466",
        "970,615,88",
        "941,993,340",
        "862,61,35",
        "984,92,344",
        "425,690,689",
    ]

    test = True
    test = False

    s = Solution()
    if test:
        s.num_connections = 10
        s.check(input)
    else:
        with open("input", "r") as f:
            s.check(f.readlines())

    print(f"Answer = {s.answer}")
# 2880 too low
# 2112 must also be too low :-(
# 8100 too low
# 9021387100 with pts 532 and 759 too high