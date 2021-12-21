with open('day1.txt', 'r') as file:
    prev = 0
    count = -1
    # create rolling avg of every 3
    data = file.readlines()
    for i in range(len(data)):
        avg = sum([int(x) for x in data[i:i + 3]]) / 3
        # print(avg, data[i:i+3])
        if avg > prev:
            count += 1
        prev = avg
    print(count)
