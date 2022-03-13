from decimal import Decimal, ROUND_HALF_UP


def main_loop(flip, input_data):
    i = 0
    while len(input_data) > 1 and i < len(input_data[0]):
        # find most common in current bit position
        common_bit = Decimal(sum([input_data[x][i] for x in range(len(input_data))]) / len(input_data)).quantize(0,
                                                                                                                 ROUND_HALF_UP)

        if flip:
            common_bit = 1 if common_bit == 0 else 0

        # filter the numbers
        input_data = [x for x in input_data if x[i] == common_bit]

        i += 1

    return int(''.join([str(x) for x in input_data[0]]), 2)


with open('day3.txt') as file:
    data = [[int(x) for x in line.strip()] for line in file.readlines()]

oxy = main_loop(False, data)
co2 = main_loop(True, data)
print(oxy * co2)
