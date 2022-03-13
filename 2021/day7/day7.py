# Brute force because I'm dumb
def calculate(input_data, calculate_fuel_usage):
    results = [sum([calculate_fuel_usage(abs(position - goal)) for position in input_data]) for goal in
               range(min(input_data), max(input_data) + 1)]
    least_fuel = int(min(results))
    index = results.index(least_fuel)
    return f'{index} uses the least fuel at {least_fuel} units'


with open('day7.txt', 'r') as file:
    data = [int(i) for i in file.readline().strip().split(',')]

# Sample input
# data = [int(i) for i in '16,1,2,0,4,2,7,1,2,14'.split(',')]

# Part 1
print('Part 1')
print(calculate(data, lambda distance: distance))

# Part 2
print('\nPart2')
print(calculate(data, lambda distance: (distance ** 2) / 2 + distance / 2))
