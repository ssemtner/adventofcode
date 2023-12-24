# This is a direct translation of https://github.com/thienudomsrirungruang/advent_of_code_2023/blob/master/day21/gold.cpp
# I have no clue how to solve part 2 so I am just going to make this functional in ocaml
# but first I wanted to make sure it worked in python

# (it only works on the real input)
# I did find an alternate test input that does work

from collections import deque

STEPS = 26501365
N = 131

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

lines = []
with open("../data/day21.txt") as file:
    lines = [line.strip() for line in file.readlines()]


import time

start_time = time.time()

n = len(lines)
m = len(lines[0].strip())

assert n == N
assert m == N

g = [[None for _ in range(3 * N)] for _ in range(3 * N)]
for i in range(N):
    for j in range(N):
        for a in range(3):
            for b in range(3):
                g[i + a * N][j + b * N] = (
                    "." if (lines[i][j] == "S" and (a != 1 or b != 1)) else lines[i][j]
                )

start = None
for i in range(3 * N):
    for j in range(3 * N):
        if g[i][j] == "S":
            start = (i, j)
            break
    if start is not None:
        break

print(start)

assert start is not None

dist = [[0 for _ in range(3 * N)] for _ in range(3 * N)]
vis = [[False for _ in range(3 * N)] for _ in range(3 * N)]

queue = deque()

queue.append(start)
vis[start[0]][start[1]] = True


def inside(point):
    return 0 <= point[0] < 3 * N and 0 <= point[1] < 3 * N


while len(queue) > 0:
    u = queue.popleft()
    for j in range(4):
        d = DIRS[j]
        v = (u[0] + d[0], u[1] + d[1])
        if inside(v) and g[v[0]][v[1]] != "#" and not vis[v[0]][v[1]]:
            vis[v[0]][v[1]] = True
            dist[v[0]][v[1]] = dist[u[0]][u[1]] + 1
            queue.append(v)

v = 0
for i in vis:
    for j in i:
        if j:
            v += 1
print(v)

dp = [0 for _ in range(STEPS + 1000)]
for i in range(STEPS, -1, -1):
    dp[i] = (i % 2 == STEPS % 2) + 2 * dp[i + N] - dp[i + 2 * N]

print(len(dp))

ans = 0
for i in range(3 * N):
    for j in range(3 * N):
        if not vis[i][j]:
            continue
        dx = i - start[0]
        dy = j - start[1]
        if -N <= dx < N and -N <= dy < N:
            ans += dp[dist[i][j]]

print(ans)
print("time:", time.time() - start_time)
