with open('day4.txt', 'r') as file:
    data = file.readlines()

called = [int(i) for i in data[0].strip().split(',')]

# parse boards
boards = []
current = []
for i in data[2::]:
    if i == '\n':
        boards.append(current)
        current = []
    else:
        current.append([int(x) for x in filter(lambda e: e != '', i.strip().split(' '))])

boards.append(current)  # last board because file doesn't end with \n

# print(called, '\n', boards)
# pprint(boards)

winners = []

for number in called:
    for board in range(len(boards)):
        for row in range(len(boards[board])):
            for i, item in enumerate(boards[board][row]):
                if item == number:
                    boards[board][row][i] = True

    # check for bingo
    for b, board in enumerate(boards):
        # create list of columns
        columns = list(zip(*board))

        if any([all([i == True for i in row]) for row in board]) or any(
                [all([i == True for i in col]) for col in columns]):
            if b not in winners:
                score = sum([sum([0 if i == True else i for i in row]) for row in board]) * number

                if len(winners) == 0:
                    print(f'First winning board is #{b + 1} with a score of score of {score}')
                else:
                    print(f'Board {b + 1} won. Score: {score}')
                winners.append(b)
