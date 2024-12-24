import time
import unittest


def part1(path):
    with open(path) as file:
        grid, instructions = file.read().split("\n\n")
        grid = grid.split("\n")
        n, m = len(grid), len(grid[0])
        walls = [[False for _ in range(m)] for _ in range(n)]
        boxes = [[False for _ in range(m)] for _ in range(n)]
        robot = (0, 0)
        for i, line in enumerate(grid):
            for j, c in enumerate(line):
                if c == "O":
                    boxes[i][j] = True
                elif c == "@":
                    robot = (i, j)
                elif c == "#":
                    walls[i][j] = True

    for c in instructions.replace("\n", ""):
        assert c in "<>^v"
        dx, dy = (
            (0, -1)
            if c == "<"
            else (0, 1)
            if c == ">"
            else (-1, 0)
            if c == "^"
            else (1, 0)
        )

        x, y = robot
        xx, yy = x + dx, y + dy

        # check for wall
        if walls[xx][yy]:
            continue
        # if nothing in front, just move
        elif not boxes[xx][yy]:
            robot = (xx, yy)
        else:
            # find end box pos
            bx, by = xx, yy
            while bx in range(1, n - 1) and by in range(1, m - 1) and boxes[bx][by]:
                bx, by = bx + dx, by + dy

            # if box is not wall, move all
            if not walls[bx][by]:
                boxes[bx][by] = True
                boxes[xx][yy] = False
                robot = (xx, yy)

    res = 0
    for i in range(n):
        for j in range(m):
            if boxes[i][j]:
                res += i * 100 + j

    return res


# I could adapt my part2 solution to also do part1, but I didn't


def part2(path):
    with open(path) as file:
        grid, instructions = file.read().split("\n\n")
        grid = grid.split("\n")
        n, m = len(grid), len(grid[0])
        walls = set()
        boxes = set()
        robot = (0, 0)
        for i, line in enumerate(grid):
            for j, c in enumerate(line):
                if c == "O":
                    boxes.add((i, j * 2))
                elif c == "@":
                    robot = (i, j * 2)
                elif c == "#":
                    walls.add((i, j * 2))
                    walls.add((i, j * 2 + 1))

    def show():
        box = False
        for i in range(n):
            for j in range(m * 2):
                if box:
                    print("]", end="")
                    box = False
                elif (i, j) in boxes:
                    print("[", end="")
                    box = True
                elif (i, j) == robot:
                    print("@", end="")
                elif (i, j) in walls:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    # print()
    # show()

    for c in instructions.replace("\n", ""):
        assert c in "<>^v"
        dx, dy = (
            (0, -1)
            if c == "<"
            else (0, 1)
            if c == ">"
            else (-1, 0)
            if c == "^"
            else (1, 0)
        )

        x, y = robot
        xx, yy = x + dx, y + dy

        # check for wall
        if (xx, yy) in walls:
            continue
        # if nothing in front, just move
        elif (xx, yy) not in boxes and (xx, yy - 1) not in boxes:
            robot = (xx, yy)
        else:
            # collect boxes to move
            to_move = set()
            q = [(x, y)]
            seen = set()
            while q:
                qx, qy = q.pop()
                if (qx, qy) in seen:
                    continue
                seen.add((qx, qy))
                qxx, qyy = qx + dx, qy + dy
                if (qxx, qyy) in boxes:
                    to_move.add((qxx, qyy))
                    q.append((qxx, qyy))
                    q.append((qxx, qyy + 1))
                if (qxx, qyy - 1) in boxes:
                    to_move.add((qxx, qyy - 1))
                    q.append((qxx, qyy - 1))
                    q.append((qxx, qyy))

                if (qxx, qyy) in walls or (qxx, qyy) in walls:
                    break

            else:  # (did not break)
                new_boxes = set()
                for x, y in boxes:
                    if (x, y) in to_move:
                        new_boxes.add((x + dx, y + dy))
                    else:
                        new_boxes.add((x, y))
                boxes = new_boxes
                robot = (xx, yy)

    res = 0
    for i in range(n):
        for j in range(m * 2):
            if (i, j) in boxes:
                res += i * 100 + j

    return res


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day15.txt"), 10092)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day15.txt"), 9021)


if __name__ == "__main__":
    start = time.time()
    print(f"part 1: {part1('../data/day15.txt')} ({time.time() - start:.4f}s)")

    start = time.time()
    print(f"part 2: {part2('../data/day15.txt')} ({time.time() - start:.4f}s)")

    unittest.main()
