import heapq
import math
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

def get_path_A(parent):
    final_path = []
    curr = goal
    while parent[curr][0] != curr:
        final_path.append(curr)
        curr = parent[curr][0]
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
    level = dict()
    frontier.append(start)
    parent[start] = start
    search_depth = level[start] = 0
    while len(frontier) > 0:
        curr = frontier.popleft()
        search_depth = max(search_depth, level[curr])
        explored.add(curr)
        if curr == goal:
            return (parent, len(explored), search_depth)
        for neighbour in get_neighbor(curr):
            if neighbour not in parent:
                frontier.append(neighbour)
                parent[neighbour] = curr
                level[neighbour] = level[curr] + 1


def dfs(start):
    frontier = deque()
    explored = set()
    parent = dict()
    level = dict()
    frontier.append(start)
    parent[start] = start
    search_depth = level[start] = 0

    while len(frontier) > 0:
        curr = frontier.pop()
        search_depth = max(search_depth, level[curr])
        explored.add(curr)
        if curr == goal:
            return (parent, len(explored), search_depth)
        for neighbour in get_neighbor(curr):
            if neighbour not in parent:
                frontier.append(neighbour)
                parent[neighbour] = curr
                level[neighbour] = level[curr] + 1


def Astar(initial_state, is_manhattan):
    pq = []  # frontier(priority queue)
    parent = dict()
    level = dict()

    explored = set()
    heapq.heappush(pq, (heuristic_manhattan(initial_state) if is_manhattan else heuristic_euclidean(initial_state), initial_state))
    parent[initial_state] = (initial_state, 0)
    search_depth = level[initial_state] = 0

    while len(pq) > 0:
        cost, curr = heapq.heappop(pq)
        if curr in explored:
            continue

        search_depth = max(search_depth, level[curr])
        explored.add(curr)
        if curr == goal:  # success
            return (parent, len(explored), search_depth)
        for neighbor in get_neighbor(curr):
            new_cost = cost + 1
            total_cost = new_cost + (heuristic_manhattan(neighbor) if is_manhattan else heuristic_euclidean(neighbor))
            if neighbor not in parent:
                parent[neighbor] = (curr, new_cost)
                level[neighbor] = level[curr] + 1
                heapq.heappush(pq, (total_cost, neighbor))
            elif neighbor in pq and new_cost < parent[neighbor][1]:
                parent[neighbor] = (curr, new_cost)
                level[neighbor] = max(level[curr] + 1, level[neighbor])
                heapq.heappush(pq, (total_cost, neighbor))

    # failed


def heuristic_manhattan(state):
    sum = 0
    for i in range(len(state)):
        x_ind = (i // 3)
        y_ind = (i % 3)
        if state[i] == ' ':
            sum = sum + abs(0 - x_ind) + abs(0 - y_ind)
        else:
            sum = sum + abs(int(state[i])//3 - x_ind) + abs(int(state[i]) % 3 - y_ind)
    return sum


def heuristic_euclidean(state):
    sum = 0
    for i in range(len(state)):
        x_ind = (i // 3)
        y_ind = (i % 3)
        if state[i] == ' ':
            sum = sum + math.sqrt(((0 - x_ind) ** 2 + (0 - y_ind) ** 2))
        else:
            sum = sum + math.sqrt(((int(state[i])//3 - x_ind) ** 2 + (int(state[i]) % 3 - y_ind) ** 2))
    return sum


def main():
    start = "120534678"
    if not is_solvable(start):
        print("Non Solvable")
        return
    start_time = time.time()
    ans = Astar(start, False)
    end_time = time.time()
    exec_time = end_time - start_time
    print("Finished in:", round(exec_time * 1e3, 4), "ms")
    trace = get_path(ans)
    print(trace[-1::-1])


if __name__ == "__main__":
    main()