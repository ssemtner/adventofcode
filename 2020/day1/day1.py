def part1():
    with open("input.txt") as f:
        data = [int(i) for i in f.readlines()]
    
    for i, v in enumerate(data):
        for x in data[i:-1]:
            if v + x == 2020:
                print(v * x)


def part2():
    with open("input.txt") as f:
        data = [int(i) for i in f.readlines()]
        
    for i in data:
        for x in data:
            for z in data:
                if i + x + z == 2020:
                    print(i * x * z)

part1()
part2()
