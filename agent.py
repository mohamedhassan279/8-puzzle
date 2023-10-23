import heapq
import math
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
    while parent[curr][0] != curr:
        final_path.append(curr)
        curr = parent[curr][0]
    final_path.append(curr)
    return final_path


def get_neighbor(state):
    res = []
    zero_pos = 0
    for i in range(9):
        if state[i] == '0':
            zero_pos = i
            break
    row, col = zero_pos // 3, zero_pos % 3
    neighbours = [[row + 1, col], [row - 1, col], [row, col + 1], [row, col - 1]]
    for elem in neighbours:
        if 0 <= elem[0] <= 2 and 0 <= elem[1] <= 2:
            pos = elem[0] * 3 + elem[1]
            if zero_pos > pos:
                left, right = pos, zero_pos
            else:
                right, left = pos, zero_pos
            tmp = state[:left] + state[right] + state[left + 1:right] + state[left] + state[right + 1:]
            res.append(tmp)
    return res


def bfs(start):
    frontier = deque()
    explored = set()
    parent = dict()
    frontier.append(start)
    parent[start] = (start, 0)
    search_depth = 0
    while len(frontier) > 0:
        curr = frontier.popleft()
        curr_level = parent[curr][1]
        search_depth = max(search_depth, curr_level)
        explored.add(curr)
        if curr == goal:
            return parent, len(explored), search_depth
        for neighbour in get_neighbor(curr):
            if neighbour not in parent:
                frontier.append(neighbour)
                parent[neighbour] = (curr, curr_level + 1)


def dfs(start):
    frontier = deque()
    explored = set()
    parent = dict()
    frontier.append(start)
    parent[start] = (start, 0)
    search_depth = 0
    while len(frontier) > 0:
        curr = frontier.pop()
        curr_level = parent[curr][1]
        search_depth = max(search_depth, curr_level)
        explored.add(curr)
        if curr == goal:
            return parent, len(explored), search_depth
        for neighbour in get_neighbor(curr):
            if neighbour not in parent:
                frontier.append(neighbour)
                parent[neighbour] = (curr, curr_level + 1)


def a_star(start, heuristic):
    frontier = []
    explored = set()
    parent = dict()
    heapq.heappush(frontier, (heuristic(start), start))
    parent[start] = (start, 0, 0)
    search_depth = 0
    while len(frontier) > 0:
        cost, curr = heapq.heappop(frontier)
        actual_cost = cost - heuristic(curr)
        if curr in explored:
            continue
        curr_level = parent[curr][2]
        search_depth = max(search_depth, curr_level)
        explored.add(curr)
        if curr == goal:
            return parent, len(explored), search_depth
        for neighbor in get_neighbor(curr):
            new_cost = actual_cost + 1
            total_cost = new_cost + heuristic(neighbor)
            if neighbor not in parent:
                heapq.heappush(frontier, (total_cost, neighbor))
                parent[neighbor] = (curr, new_cost, curr_level + 1)
            elif neighbor not in explored and new_cost < parent[neighbor][1]:
                parent[neighbor] = (curr, new_cost, max(curr_level + 1, parent[neighbor][2]))
                heapq.heappush(frontier, (total_cost, neighbor))


def heuristic_manhattan(state):
    total = 0
    for i in range(len(state)):
        x_ind = (i // 3)
        y_ind = (i % 3)
        if state[i] != '0':
            total += abs(int(state[i]) // 3 - x_ind) + abs(int(state[i]) % 3 - y_ind)
    return total


def heuristic_euclidean(state):
    total = 0
    for i in range(len(state)):
        x_ind = (i // 3)
        y_ind = (i % 3)
        if state[i] != '0':
            total += math.sqrt((int(state[i]) // 3 - x_ind) ** 2 + (int(state[i]) % 3 - y_ind) ** 2)
    return total
