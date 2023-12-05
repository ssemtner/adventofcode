from typing import List
import unittest
from itertools import chain


class Range:
    def __init__(self, dest_start, source_start, length):
        self.source_start = source_start
        self.dest_start = dest_start
        self.length = length

    def __repr__(self):
        return f"Range({self.source_start}, {self.dest_start}, {self.length} ({self.source_start} - {self.source_start + self.length - 1}))"

    def __contains__(self, value):
        return self.source_start <= value < self.source_start + self.length

    def __getitem__(self, value):
        return self.dest_start - self.source_start + value

    # splits by point in source range
    # split_point is included in the first range and not in the second range
    # maintains same offset
    def split(self, split_point) -> ("Range", "Range"):
        if (
            split_point <= self.source_start
            or split_point >= self.source_start + self.length - 1
        ):
            raise ValueError("split_point must be in range")

        offset = self.dest_start - self.source_start
        # o = d - s
        # d = o + s

        return (
            Range(
                self.dest_start,
                self.source_start,
                split_point - self.source_start + 1,
            ),
            Range(
                self.dest_start - self.source_start + split_point + 1,  # dest
                self.dest_start
                - self.source_start
                + split_point
                + offset
                + 1,  # source
                self.length - (split_point - self.source_start) - 1,
            ),
        )


class Map:
    def __init__(self, ranges):
        self.ranges = ranges

    def __repr__(self):
        return f"Map[{self.ranges}]"

    def __getitem__(self, key):
        for range in self.ranges:
            if key in range:
                return range[key]
        return key

    def translate_range(self, range: Range) -> List[Range]:
        # print(" translate_range", range)

        # if range full contained, return [translated_range]
        # else if range partially contained, return [translate_range(contained), translate_range(not_contained)]
        # else if not contained, return [range]

        # end point, inclusive
        end = range.source_start + range.length - 1

        # first check range fully contained in r
        # print("    ranges", self.ranges)
        for r in self.ranges:
            if range.source_start in r and end in r:
                offset = r.dest_start - r.source_start
                # print("  fully contained in", r)
                translated = Range(
                    range.source_start + offset,
                    range.dest_start + offset,
                    range.length,
                )
                # print("   translated", [translated])
                return [translated]

        # then check partially contained
        for r in self.ranges:
            # ex: range [10-30] r [0-20]
            if range.source_start in r and end not in r:
                # print("  start contained", r)
                to_translate, remaining = range.split(
                    r.source_start + r.length - 1
                )  # [10-20], [21-30]
                translated = self.translate_range(to_translate)
                return translated + self.translate_range(remaining)

            # ex: range [0-10] r [5-20]
            elif end in r and range.source_start not in r:
                # print("  end contained", r)
                remaining, to_translate = range.split(
                    r.source_start - 1
                )  # [0-4], [5-10]
                translated = self.translate_range(to_translate)
                # print("       translated AA", translated)
                remaining_translated = self.translate_range(remaining)
                # print("    remaining_translated", remaining_translated)
                extended = translated + remaining_translated
                # print("    extended", extended)
                return extended

            # ex: range [0-10] r [2-4]
            elif r.source_start in range and r.source_start + r.length - 1 in range:
                # print("  r contained", r)
                remaining_1, step_2 = range.split(r.source_start - 1)  # [0-1], [2-10]
                to_translate, remaining_2 = step_2.split(
                    r.source_start + r.length - 1
                )  # [2-4], [5-10]
                translated = self.translate_range(to_translate)
                remaining_1_translated = self.translate_range(remaining_1)
                remaining_2_translated = self.translate_range(remaining_2)
                return translated + remaining_1_translated + remaining_2_translated

        # else it is not intersected
        # print("  not contained")
        return [range]


def parse_maps(sections):
    return [
        Map(
            [
                Range(*[int(x) for x in range.split(" ")])
                for range in section.split("\n")[1:]
                if range != ""
            ]
        )
        for section in sections[1:]
    ]


def trace_seed(seed, maps):
    val = seed
    for map in maps:
        val = map[val]
    return val


def part1(path):
    with open(path, "r") as file:
        sections = file.read().split("\n\n")
        seeds = [int(x) for x in sections[0].split(": ")[1].split(" ")]

        maps = parse_maps(sections)

        return min([trace_seed(seed, maps) for seed in seeds])


def trace_seed_range(seed_range: Range, maps: List[Map], i=0) -> List[Range]:
    # print("trace_seed_range", seed_range, i)
    if i >= len(maps):
        # print("returning", [seed_range])
        return [seed_range]

    ranges = maps[i].translate_range(seed_range)

    # print("    returned ranges:", ranges)

    return [trace_seed_range(r, maps, i + 1) for r in ranges]


def minimum_ranges_dest(*ranges: Range) -> int:
    print(ranges)
    return min([r.dest_start for r in ranges])


def part2(path):
    with open(path, "r") as file:
        sections = file.read().split("\n\n")
        seed_vals = [int(x) for x in sections[0].split(": ")[1].split(" ")]
        seed_ranges = []
        for i in range(0, len(seed_vals), 2):
            seed_ranges.append(Range(seed_vals[i], seed_vals[i], seed_vals[i + 1]))
        # print(seed_ranges)

        # print(seed_ranges[0].split(90))

        maps = parse_maps(sections)
        # print(maps[0].ranges[1])
        # print(maps[0].ranges[1].split(60))

        locations = [trace_seed_range(seed_range, maps) for seed_range in seed_ranges]

        def flattenList(nestedList):
            # check if list is empty
            if not (bool(nestedList)):
                return nestedList

            # to check instance of list is empty or not
            if isinstance(nestedList[0], list):
                # call function with sublist as argument
                return flattenList(*nestedList[:1]) + flattenList(nestedList[1:])

            # call function with sublist as argument
            return nestedList[:1] + flattenList(nestedList[1:])

        locations = flattenList(locations)

        # min_location =

        m = locations[0].dest_start
        for i in locations:
            if i.dest_start < m:
                m = i.dest_start

        return m

        # return minimum_ranges_dest(locations[0])
        # return min([trace_seed(seed, maps) for seed in real_seeds])


class TestDay1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day5.txt"), 35)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day5.txt"), 46)


if __name__ == "__main__":
    import time
    p1start = time.time()
    print("part 1:", part1("../data/day5.txt"))
    p1end = time.time()
    p2start = time.time()
    print("part 2:", part2("../data/day5.txt"))
    p2end = time.time()
    print("part 1 time:", p1end - p1start)
    print("part 2 time:", p2end - p2start)

    unittest.main()

