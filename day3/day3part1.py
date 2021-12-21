with open('day3.txt') as file:
    data = [[int(x) for x in i.strip()] for i in file.readlines()]

    gamma = ''

    for x in range(len(data[0])):
        r = round(sum([data[i][x] for i in range(len(data))]) / len(data))
        gamma += str(r)

    epsilon = ''.join(['1' if i == '0' else '0' for i in gamma])

    print(int(epsilon, 2) * int(gamma, 2))
