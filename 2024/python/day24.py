from collections import defaultdict
import time
import unittest


def part1(path):
    res = 0
    gates = []
    deps = defaultdict(list)
    with open(path) as file:
        init, rest = file.read().split("\n\n")

    for line in rest.splitlines():
        a, op, b, _, out = line.split()
        gates.append([op, a, b, out])
        i = len(gates) - 1
        deps[a].append(i)
        deps[b].append(i)

    wires = defaultdict(bool)
    q = []
    for line in init.splitlines():
        line, val = line.split(": ")
        wires[line] = bool(int(val))
        q.append(line)
    while q:
        wire = q.pop(0)
        for i in deps[wire]:
            op, a, b, out = gates[i]
            res = False
            if op == "AND":
                wires[out] = wires[a] & wires[b]
            elif op == "OR":
                wires[out] = wires[a] | wires[b]
            else:
                wires[out] = wires[a] ^ wires[b]

            if out in deps:
                q.append(out)

    res = int(
        "".join(
            str(int(b))
            for _, b in sorted(
                ((k, v) for k, v in wires.items() if k[0] == "z"), reverse=True
            )
        ),
        2,
    )
    return res


def part2(path):
    with open(path) as file:
        _, rest = file.read().split("\n\n")

    gates = []
    deps = defaultdict(list)
    last_xor = 0
    for line in rest.splitlines():
        a, op, b, _, out = line.split()
        if out[0] == "z":
            last_xor = max(last_xor, int(out[1:]))
        gates.append([op, a, b, out])
        i = len(gates) - 1
        deps[a].append(i)
        deps[b].append(i)

    last_xor = f"z{last_xor}"

    problems = set()
    for op, a, b, out in gates:
        # an XOR gate to output cannot just be from x and y
        if op == "XOR":
            if a[0] not in "xyz" and b[0] not in "xyz" and out[0] not in "xyz":
                problems.add((a, b, op, out))
            # except for x00 and y00
            if a == "x00" and b == "y00" and out == "z00":
                continue
            elif (a[0] == "x" and b.startswith("y")) or (
                a[0] == "y" and b.startswith("x")
            ):
                if out[0] == "z":
                    problems.add((a, b, op, out))
                # all of these need to output to an XOR that outputs z
                if not any(
                    gates[i][0] != "XOR" or not gates[i][3][0] == "z" for i in deps[out]
                ):
                    problems.add((a, b, op, out))

            # otherwise it should be a z output
            elif not out[0] == "z":
                problems.add((a, b, op, out))

            # must go to an AND if not output
            if not out[0] == "z" and not any(gates[i][0] == "AND" for i in deps[out]):
                problems.add((a, b, op, out))

        # if it outputs to z, it must be an XOR, except for the last one (carry out)
        if out[0] == "z" and op != "XOR" and out != last_xor:
            problems.add((a, b, op, out))

        # an AND must go to an OR
        if op == "AND" and a != "x00":
            if not any(gates[i][0] == "OR" for i in deps[out]):
                problems.add((a, b, op, out))

    # debug print if not done
    if len(problems) != 8:
        print(f"Found {len(problems)} problems:")
        for a, b, op, out in problems:
            print(f"{a} {op} {b} -> {out}")
    return ",".join(sorted(gate[3] for gate in problems))


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day24ex1.txt"), 4)
        self.assertEqual(part1("../data/sample/day24ex2.txt"), 2024)


if __name__ == "__main__":
    start = time.time()
    print(f"part 1: {part1('../data/day24.txt')} ({time.time() - start:.4f}s)")

    start = time.time()
    print(f"part 2: \"{part2('../data/day24.txt')}\" ({time.time() - start:.4f}s)")

    unittest.main()
