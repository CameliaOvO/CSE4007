# check if the point is valid and not visited
def is_valid(point_y, point_x, row, col, maze, visited):
    if 0 <= point_y < row and 0 <= point_x < col:
        if maze[point_y][point_x] != '1' and visited[point_y][point_x] == '0':
            return True
    else:
        return False


def iterative_deepening_search(row, col, maze, start_point, goal_points):
    depth, answer_stack = 0, []
    while depth < row * col:
        visited = [['0' for _ in range(col)] for _ in range(row)]
        found = depth_limited_search(row, col, maze, start_point, goal_points, depth, visited, answer_stack)
        if found is not None:
            for p in answer_stack:
                maze[p[0]][p[1]] = '5' if p not in goal_points else '4'
            return maze
        depth += 1


def depth_limited_search(row, col, maze, point, goal_points, depth, visited, answer_stack):
    global cnt
    cnt += 1
    visited[point[0]][point[1]] = '1'
    if depth == 0 and point in goal_points:
        return point
    if depth > 0:
        for p in map(lambda d: (point[0]+d[0], point[1]+d[1]), [(1, 0), (-1, 0), (0, 1), (0, -1)]):
            if is_valid(p[0], p[1], row, col, maze, visited):
                found = depth_limited_search(row, col, maze, p, goal_points, depth - 1, visited, answer_stack)
                visited[p[0]][p[1]] = '0'
                if found is not None:
                    answer_stack.append(p)
                    return found
    return None


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
a = iterative_deepening_search(r, c, m, s, g)
write_answer(a, sum(l.count('5') for l in a), cnt)
