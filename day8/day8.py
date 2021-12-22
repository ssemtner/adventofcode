with open('day8.txt') as file:
    data = [[[sorted(list(i)) for i in x.split()] for x in line.strip().split('|')] for line in file.readlines()]

outputs = []
for line in data:
    for output in line[1]:
        outputs.append(output)

# Count all that are 1, 4, 7, or 8
unique = (2, 4, 3, 7)
count = 0
for i in outputs:
    if len(i) in unique:
        count += 1

print(f'Part 1: {count}\n')


def filter_by_segments(dataset, quantity):
    return list(filter(lambda x: len(x) == quantity, dataset))


def find_different_segments(dataset, start, removed):
    return list(filter(lambda x: x not in dataset[removed], dataset[start]))


def solve_positions(patterns):
    # top, top-right, bottom-right, bottom, bottom-left, top-left, middle
    positions = ['' for i in range(7)]
    numbers = [[] for i in range(10)]

    # Find the unique numbers
    for key, value in {1: 2, 4: 4, 7: 3, 8: 7}.items():
        numbers[key] = filter_by_segments(patterns, value)[0]

    positions[0] = find_different_segments(numbers, 7, 1)[0]

    # Find 5 segment digits (2, 3, 5)
    five_segments = filter_by_segments(patterns, 5)

    # Lock in 3
    for number in five_segments:
        if all([i in number for i in numbers[7]]):
            numbers[3] = number

    # Find 6 segment numbers (0, 6, 9)
    six_segments = filter_by_segments(patterns, 6)

    # Lock in 6
    for number in six_segments:
        if any([i not in number for i in numbers[7]]):
            numbers[6] = number

    # Middle segment is the only one in 3 and not 0
    # positions[6] = find_different_segments(numbers, 3, 0)[0]

    # Top left segment is only one in 4 and not 3
    positions[5] = find_different_segments(numbers, 4, 3)[0]

    # Top right segment is the one from 1 that is in 6
    positions[1] = find_different_segments(numbers, 1, 6)[0]

    # Bottom right is the other one
    positions[2] = list(filter(lambda x: x != positions[1], numbers[1]))[0]

    # Bottom left is in 8 and not 3 and not the same as top left
    positions[4] = list(filter(lambda x: x != positions[5], find_different_segments(numbers, 8, 3)))[0]

    # Bottom is in 3 and not 4 and not one of the existing positions
    positions[3] = list(filter(lambda x: x not in positions, find_different_segments(numbers, 3, 4)))[0]

    # Middle is in 8 and not positions
    positions[6] = list(filter(lambda x: x not in positions, numbers[8]))[0]

    return positions


def solve_outputs(problem_data):
    solved_positions = solve_positions(problem_data[0])

    number_positions = {key: sorted([solved_positions[x] for x in value]) for key, value in
                        NUMBER_POSITIONS_TEMPLATE.items()}

    result = ''

    for digit in problem_data[1]:
        for key, value in number_positions.items():
            if value == digit:
                result += str(key)

    return int(result)


NUMBER_POSITIONS_TEMPLATE = {
    0: (0, 1, 2, 3, 4, 5),
    1: (1, 2),
    2: (0, 1, 3, 4, 6),
    3: (0, 1, 2, 3, 6),
    4: (1, 2, 5, 6),
    5: (0, 2, 3, 5, 6),
    6: (0, 2, 3, 4, 5, 6),
    7: (0, 1, 2),
    8: (0, 1, 2, 3, 4, 5, 6),
    9: (0, 1, 2, 3, 5, 6)
}

print(sum([solve_outputs(line) for line in data]))
