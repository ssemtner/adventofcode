with open('day9.txt') as file:
    data = [[int(i) for i in line.strip()] for line in file.readlines()]

DIRECTIONS = ((-1, 0), (0, -1), (1, 0), (0, 1))

low_points = []

for row in range(len(data)):
    for i in range(len(data[row])):
        low_point = True
        for d in DIRECTIONS:
            try:
                if data[row][i] >= data[row + d[0]][i + d[1]]:
                    low_point = False
            except IndexError:
                pass
        if low_point:
            print(row, i)
            low_points.append((row, i))

print(len(low_points))
