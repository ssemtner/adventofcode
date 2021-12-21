def display_grid(grid_to_print):
    output = ''
    for row in list(zip(*grid_to_print)):
        for c in row:
            output += '.' if c == 0 else str(c)
        output += '\n'

    return output


def add_horizontal_or_vertical_line(line, direction):
    index = 0 if direction == 'h' else 1
    start, end = (min(line[0][index], line[1][index]), max(line[0][index], line[1][index]))

    for i in range(start, end + 1):
        if direction == 'h':
            grid[i][line[0][1]] += 1
        elif direction == 'v':
            grid[line[0][0]][i] += 1


def add_diagonal_line(line):
    # Put smallest x value first
    if line[0][0] > line[1][0]:
        right, left = line
    else:
        left, right = line

    y = left[1]
    change = 1 if left[1] < right[1] else -1
    for x in range(left[0], right[0] + 1):
        grid[x][y] += 1
        y += change


# Retrieve data
with open('day5.txt', 'r') as file:
    data = file.readlines()

lines = [tuple([tuple([int(i) for i in point.split(',')]) for point in line.strip().split('->')]) for line in data]

x_max, y_max = [max([max([i[x][d] for i in lines]) for x in range(2)]) for d in range(2)]

grid = [[0 for x in range(x_max + 1)] for y in range(y_max + 1)]

for line in lines:
    # Vertical (same x)
    if line[0][0] == line[1][0]:
        add_horizontal_or_vertical_line(line, 'v')

    # Horizontal (same y)
    elif line[0][1] == line[1][1]:
        add_horizontal_or_vertical_line(line, 'h')

    # Diagonal (45 degrees)
    else:
        add_diagonal_line(line)

print(display_grid(grid))

# Count intersections
print(sum([len(list(filter(lambda x: x > 1, row))) for row in grid]))
