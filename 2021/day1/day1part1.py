with open('day1.txt', 'r') as data:
    prev = 0
    count = -1
    for line in data.readlines():
        if int(line) > prev:
            count += 1
        prev = int(line)
    print(count)
