from collections import defaultdict

with open('day6.txt') as file:
    data = [int(i) for i in file.readline().strip().split(',')]

# Sample input
# data = [int(i) for i in '3,4,3,1,2'.split(',')]

state = defaultdict(int)
for fish in data:
    if fish not in state:
        state[fish] = 0
    state[fish] += 1

for day in range(1, 257):
    new_state = defaultdict(int)
    for key, count in state.items():
        if key == 0:
            new_state[6] += count
            new_state[8] += count
        else:
            new_state[key - 1] += count

    state = new_state

    if day == 80:
        print(f'Lanternfish after 80 days: {sum(state.values())}')

print(f'Lanternfish after 257 days: {sum(state.values())}')
