import copy

class Solution(object):
    def __init__(self):
        self.answer = 0

        self.links = {}

        self.fast_links = {}
        self.int_lookup = {}
        self.str_lookup = {}

        self.cache_level = 200
        self.cache = {}

    def check(self, lines):

        self.load_input(lines)

        svr_id = self.str_lookup["svr"]
        dac_id = self.str_lookup["dac"]
        fft_id = self.str_lookup["fft"]
        out_id = self.str_lookup["out"]

        self.cache_drop = [svr_id, dac_id, fft_id, out_id]
        self.cache_stop_short = []
        self.load_stop_shorts()

        self.heat_cache()
        print(f"Cached items: {len(self.cache)}")

        to_dac = self.find_paths5(svr_id, dac_id, [fft_id, out_id])
        print(f"Paths to dac: {to_dac}")
        to_fft = self.find_paths5(svr_id, fft_id, [dac_id, out_id])
        print(f"Paths to fft: {to_fft}")
        dac_to_fft = self.find_paths5(dac_id, fft_id, [out_id])
        print(f"Paths dac to fft: {dac_to_fft}")
        fft_to_dac = self.find_paths5(fft_id, dac_id, [out_id])
        print(f"Paths fft to dac: {dac_to_fft}")
        fft_to_out = self.find_paths5(fft_id, out_id, [])
        print(f"Paths fft to out {fft_to_out}")
        dac_to_out = self.find_paths5(dac_id, out_id, [])
        print(f"Paths dac to out {dac_to_out}")


        # to_dac = self.find_paths4("svr", "dac", ["fft", "out"])
        # print(f"Paths to dac: {to_dac}")
        # to_fft = self.find_paths4("svr", "fft", ["dac", "out"])
        # print(f"Paths to fft: {to_fft}")
        # dac_to_fft = self.find_paths4("dac", "fft", ["out"])
        # print(f"Paths dac to fft: {dac_to_fft}")
        # fft_to_dac = self.find_paths4("fft", "dac", ["out"])
        # print(f"Paths fft to dac: {dac_to_fft}")
        # fft_to_out = self.find_paths4("fft", "out", [])
        # print(f"Paths fft to out {fft_to_out}")
        # dac_to_out = self.find_paths4("dac", "out", [])
        # print(f"Paths dac to out {dac_to_out}")

        self.answer = to_fft * fft_to_dac * dac_to_out
        self.answer += to_dac * dac_to_fft * fft_to_out

        # self.answer = to_fft * to_dac * to_out

        #self.find_paths()

    def load_input(self, lines):
        index = 0
        for line in lines:
            node, connections = line.split(":")
            self.int_lookup[index] = node
            self.str_lookup[node] = index
            self.links[node] = tuple(connections.split())
            index += 1

        self.int_lookup[index] = "out"
        self.str_lookup["out"] = index

        for node, connections in self.links.items():
            cs = []
            for conn in connections:
                cs.append(self.str_lookup[conn])
            self.fast_links[self.str_lookup[node]] = cs

    def load_stop_shorts(self):
        for node, check_set in self.fast_links.items():
            for drop in self.cache_drop:
                if drop in check_set:
                    self.cache_stop_short.append(node)

    def heat_cache(self):
        for node, check_set in self.fast_links.items():
            if node in self.cache_drop:
                continue

            active_paths = {}

            drop = False
            for c in check_set:
                if c in self.cache_drop:
                    drop = True
                    break
                elif c in self.cache_stop_short:
                    active_paths[c] = 1

            check_set = [x for x in check_set if not x in self.cache_stop_short]

            if drop:
                continue

            iter = 0
            while iter < self.cache_level:
                for c in check_set:
                    if c in self.cache_drop:
                        raise RuntimeError("Got to a drop")
                        drop = True
                        break
                    elif c in self.cache_stop_short:
                        raise RuntimeError("Got to a stop short")
                        pass
                    elif c == node:
                        raise RuntimeError("Loop Detected")
                    elif c in active_paths:
                        active_paths[c] += 1
                    else:
                        active_paths[c] = 1

                check_set = []
                for path in active_paths.keys():
                    if path in self.cache_stop_short:
                        continue
                    check_set += self.fast_links[path]

                for c in check_set:
                    if c in self.cache_stop_short:
                        if c in active_paths:
                            active_paths[c] += 1
                        else:
                            active_paths[c] = 1
                check_set = [x for x in check_set if not x in self.cache_stop_short]

                if drop:
                    break
                iter += 1

            if drop:
                continue
            self.cache[node] = active_paths


    def find_paths5(self, start, end, drop=[]):
        active_paths = {start:1}
        total = 0
        while(len(active_paths)):
            node, count = active_paths.popitem()
            for conn in self.fast_links[node]:
                if conn in drop:
                    pass
                elif conn == end:
                    total += count
                elif conn in self.cache:
                    for path, count in self.cache[conn].items():
                        if path in active_paths:
                            active_paths[path] += count
                        else:
                            active_paths[path] = count
                else:
                    if conn in active_paths:
                        active_paths[conn] += count
                    else:
                        active_paths[conn] = count
        return total

    def find_paths4(self, start, end, drop=[]):
        active_paths = {start:1}
        total = 0
        while(len(active_paths)):
            node, count = active_paths.popitem()
            for conn in self.links[node]:
                if conn in drop:
                    pass
                elif conn == end:
                    total += count
                else:
                    if conn in active_paths:
                        active_paths[conn] += count
                    else:
                        active_paths[conn] = count
        return total

    def find_paths3(self, start, end):
        active_paths = [start]
        total = 0
        while(len(active_paths)):
            node = active_paths.pop()
            for conn in self.links[node]:
                if conn == end:
                    total += 1
                elif conn == "out":
                    pass
                else:
                    active_paths.append(conn)

    def find_paths2(self, start, end):
        active_paths = {start:[[start]]}
        total = 0
        while(len(active_paths)):
            node, paths = active_paths.popitem()
            for conn in self.links[node]:
                if conn == end:
                    #print(len(paths))
                    total += len(paths)
                    #for path in paths:
                    #    print(path)
                elif conn == "out":
                    pass
                else:
                    loop = False
                    p2 = []
                    for path in paths:
                        if conn in path:
                            loop = True
                            break
                        p3 = path[:]
                        p3.append(conn)
                        p2.append(p3)
                    if not loop:
                        if conn in active_paths:
                            active_paths[conn] += p2
                        else:
                            active_paths[conn] = p2
        return total

    def find_paths_old(self):
        # 0 - through neither
        # 1 - through dac
        # 2 - through fft
        # 3 - through both
        active_paths = {"svr":[0, 0, 0, 0]}
        while(len(active_paths)):
            node, counts = active_paths.popitem()
            for conn in self.links[node]:
                if conn == "out":
                    if counts[2]:
                        self.answer += counts[2]
                else:
                    new_counts = [0, 0, 0, 0]
                    if conn == "dac":
                        new_counts[1] = counts[0]
                        new_counts[3] = counts[2]
                    elif conn == "fft":
                        new_counts[2] = counts[0]
                        new_counts[3] = counts[1]
                    else:
                        pass

                    if conn in active_paths:
                        active_paths[conn] += count
                    else:
                        active_paths[conn] = info


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

# 312 - too low
# 30000000 - too low