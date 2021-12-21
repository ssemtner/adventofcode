with open('day2.txt') as file:
    steps = tuple([tuple(line.strip().split(' ')) for line in file.readlines()])

# ----------
# | Part 1 |
# ----------

depth = 0
horizontal = 0

for step in steps:
    amount = int(step[1])

    if step[0] == 'forward':
        horizontal += amount
    elif step[0] == 'down':
        depth += amount
    elif step[0] == 'up':
        depth -= amount

print('Part 1:')
print(f'Horizontal Position: {horizontal}')
print(f'Depth: {depth}')
print(f'Result: {horizontal * depth}\n')

# ----------
# | Part 2 |
# ----------

aim = 0
depth = 0
horizontal = 0

for step in steps:
    amount = int(step[1])

    if step[0] == 'forward':
        horizontal += amount
        depth += aim * amount
    elif step[0] == 'down':
        aim += amount
    elif step[0] == 'up':
        aim -= amount

print('Part 2:')
print(f'Aim: {aim}')
print(f'Horizontal Position: {horizontal}')
print(f'Depth: {depth}')
print(f'Result: {horizontal * depth}')
