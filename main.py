import heapq
import time
from collections import deque

goal = "012345678"


def is_solvable(state):
    inv = 0
    for i in range(8):
        for j in range(i + 1, 9):
            if state[j] != '0' and state[i] != '0' and state[i] > state[j]:
                inv = inv + 1
    return inv % 2 == 0


def get_path(parent):
    final_path = []
    curr = goal
    while parent[curr] != curr:
        final_path.append(curr)
        curr = parent[curr]
    final_path.append(curr)
    return final_path


def get_neighbor(state):
    res = []
    row = col = zero_pos = 0
    for i in range(9):
        if state[i] == '0':
            zero_pos = i
            row, col = i // 3, i % 3

    neighbours = [[row + 1, col], [row - 1, col], [row, col + 1], [row, col - 1]]
    for elem in neighbours:
        if 0 <= elem[0] <= 2 and 0 <= elem[1] <= 2:
            pos = elem[0] * 3 + elem[1]
            if zero_pos > pos:
                l, r = pos, zero_pos
            else:
                r, l = pos, zero_pos
            tmp = state[:l] + state[r] + state[l + 1:r] + state[l] + state[r + 1:]
            res.append(tmp)
    return res


def bfs(start):
    frontier = deque()
    explored = set()
    parent = dict()
    frontier.append(start)
    parent[start] = start
    while len(frontier) > 0:
        curr = frontier.popleft()
        explored.add(curr)
        if curr == goal:
            return parent
        for neighbour in get_neighbor(curr):
            if neighbour not in parent:
                frontier.append(neighbour)
                parent[neighbour] = curr


def dfs(start):
    frontier = deque()
    explored = set()
    parent = dict()
    frontier.append(start)
    parent[start] = start
    while len(frontier) > 0:
        curr = frontier.pop()
        explored.add(curr)
        if curr == goal:
            return parent
        for neighbour in get_neighbor(curr):
            if neighbour not in parent:
                frontier.append(neighbour)
                parent[neighbour] = curr


def Astar(start):
    pq = []  # frontier(priority queue)
    parent = dict()
    explored = set()
    heapq.heappush(pq, (start, 0))
    parent.update({start, (start, 0)})
    while not pq:
        cost, curr = heapq.heappop(pq)
        if curr in explored:
            continue
        explored.add(curr)
        if curr == goal:  # success
            return 1
        for neighbor, edge_cost in get_neighbor(curr):
            if neighbor not in parent:
                new_cost = cost + edge_cost
                parent[neighbor] = (curr, new_cost)
                heapq.heappush(pq, (neighbor, new_cost))
            if neighbor in pq:
                old_cost = pq
                modified_cost = cost + edge_cost
                if modified_cost < old_cost:
                    parent[neighbor] = (curr, modified_cost)
                    heapq.heappush(pq, (neighbor, modified_cost))
    return 0  # failed


def main():
    start = "125340678"
    if not is_solvable(start):
        print("Non Solvable")
        return
    start_time = time.time()
    ans = bfs(start)
    end_time = time.time()
    exec_time = end_time - start_time
    print("Finished in:", round(exec_time * 1e3, 4), "ms")
    trace = get_path(ans)
    print(trace[-1::-1])


if __name__ == "__main__":
    main()
