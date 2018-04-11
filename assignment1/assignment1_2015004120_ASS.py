# check if the point is valid and not visited
def is_valid(point_y, point_x, row, col, maze, visited):
    if 0 <= point_y < row and 0 <= point_x < col:
        if maze[point_y][point_x] != '1' and visited[point_y][point_x] == '0':
            return True
    else:
        return False


def get_cost(point, path, start_point):
    count = 0
    while point != start_point:
        point = [p for p in path if p[0] == point][0][1]
        count += 1
    return count


def heuristic(point, goal_points):
    return min(map(lambda x: abs(x[0] - point[0]) + abs(x[1] - point[1]), goal_points))


def a_star_search(row, col, maze, start_point, goal_points):
    global cnt
    path, priority_queue, point = [], [], None
    visited = [['0' for _ in range(col)] for _ in range(row)]
    priority_queue.insert(0, (start_point, 0 + heuristic(start_point, goal_points), (-1, -1)))
    visited[start_point[0]][start_point[1]] = '1'
    while len(priority_queue) > 0:
        cnt += 1
        priority_queue = sorted(priority_queue, key=lambda x: x[1])
        point = priority_queue.pop(0)
        path.append((point[0], point[2]))
        point = point[0]
        if point in goal_points:
            break
        else:
            for p in map(lambda d: (point[0] + d[0], point[1] + d[1]), [(1, 0), (-1, 0), (0, 1), (0, -1)]):
                if is_valid(p[0], p[1], row, col, maze, visited):
                    visited[p[0]][p[1]] = '1'
                    priority_queue.insert(0, (p, get_cost(point, path, start_point) + heuristic(p, goal_points), point))
    while point != start_point:
        maze[point[0]][point[1]] = '5' if point not in goal_points else '4'
        point = [p for p in path if p[0] == point][0][1]
    return maze


# open input file and get information of maze
def get_maze():
    with open('input.txt', 'r') as f:
        row, col = list(map(int, f.readline().split()))
        maze = f.read().split()
        start_point = (maze.index('3') // col, maze.index('3') % col)
        goal_points = [(i // col, i % col) for i, x in enumerate(maze) if x == '4']
        maze = [maze[i:i + col] for i in range(0, len(maze), col)]
    return row, col, maze, start_point, goal_points


# open output file and write answer, length, time
def write_answer(answer, length, time):
    with open('output.txt', 'w') as f:
        f.write("\n".join([" ".join(line) for line in answer]))
        f.write("\n---\nlength={}\ntime={}\n".format(length, time))


cnt = 0
r, c, m, s, g = get_maze()
a = a_star_search(r, c, m, s, g)
write_answer(a, sum(l.count('5') for l in a), cnt)
