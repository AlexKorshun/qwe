import random
import sys

# Saved route templates for one-time block levels.
# alpha - previous working template (kept for reference),
# beta  - new template from the latest user scheme.
ONE_TIME_TEMPLATE_ALPHA = [(0, 1), (1, 0), (0, 1), (-1, 0), (0, 1), (1, 0), (0, -1), (-1, 0), (0, 1)]
# Beta route (from point1): R, U, R(hit 8), D, L, D, U, R(through old 8), D(to finish)
ONE_TIME_TEMPLATE_BETA = [(0, 1), (-1, 0), (0, 1), (1, 0), (0, -1), (1, 0), (-1, 0), (0, 1), (1, 0)]
# Gamma route (fixed, one orientation):
# 1 R(hit 8), 2 D, 3 R, 4 D, 5 R, 6 U, 7 L, 8 U(through old 8), 9 L(to finish)
ONE_TIME_TEMPLATE_GAMMA = [(0, 1), (1, 0), (0, 1), (1, 0), (0, 1), (-1, 0), (0, -1), (-1, 0), (0, -1)]
ACTIVE_ONE_TIME_TEMPLATE = "gamma"
DECOY_ONE_TIME_BLOCKS_MIN = 1
DECOY_ONE_TIME_BLOCKS_MAX = 3


class Engine():
    stop_tunneler = False

    def coinfliper(self):
        if random.randint(1, 3) == 1:
            return random.randint(2, self.rows)
        else:
            return random.randint(2, self.rows // 2)

    def generateTheWay(self):
        sys.setrecursionlimit(1000000)
        self.stop_tunneler = True
        for y in range(self.rows):
            for x in range(self.columns):
                self.map[y][x] = 0
        finishPoint = [random.randint(1, self.rows - 2), random.randint(1, self.columns - 2)]
        self.map[finishPoint[0]][finishPoint[1]] = 7  # generate finish point
        self.direction = random.randint(1, 4)
        if self.direction == 1:
            self.map[finishPoint[0]][finishPoint[1] + 1] = 99
            self.map[finishPoint[0] + 1][finishPoint[1]] = 99
            self.map[finishPoint[0] - 1][finishPoint[1]] = 99
        if self.direction == 2:
            self.map[finishPoint[0]][finishPoint[1] - 1] = 99
            self.map[finishPoint[0] + 1][finishPoint[1]] = 99
            self.map[finishPoint[0] - 1][finishPoint[1]] = 99
        if self.direction == 3:
            self.map[finishPoint[0]][finishPoint[1] + 1] = 99
            self.map[finishPoint[0]][finishPoint[1] - 1] = 99
            self.map[finishPoint[0] - 1][finishPoint[1]] = 99
        if self.direction == 4:
            self.map[finishPoint[0]][finishPoint[1] + 1] = 99
            self.map[finishPoint[0]][finishPoint[1] - 1] = 99
            self.map[finishPoint[0] + 1][finishPoint[1]] = 99
        currentPoint = finishPoint
        stoper = 0
        length = self.coinfliper()
        while stoper < 20:
            if self.direction == 4:
                if currentPoint[0] > 1 and length > 0 and (
                        self.map[currentPoint[0] - 1][currentPoint[1]] == 10 or self.map[currentPoint[0] - 1][
                    currentPoint[1]] == 0):
                    if self.map[currentPoint[0]][currentPoint[1]] == 10:
                        self.map[currentPoint[0]][currentPoint[1]] = 12
                    currentPoint[0] -= 1
                    if self.map[currentPoint[0]][currentPoint[1]] == 10:
                        self.map[currentPoint[0]][currentPoint[1]] = 12
                    else:
                        self.map[currentPoint[0]][currentPoint[1]] = 11
                    length -= 1
                else:
                    if self.map[currentPoint[0] + 1][currentPoint[1]] == 99:
                        self.map[currentPoint[0]][currentPoint[1]] = 6
                        if stoper < 10:
                            self.generateTheWay()
                            return
                        else:
                            break
                    elif self.map[currentPoint[0]][currentPoint[1] + 1] != 99 and self.map[currentPoint[0]][
                        currentPoint[1] + 1] != 0 and self.map[currentPoint[0]][currentPoint[1] - 1] != 99 and \
                            self.map[currentPoint[0]][currentPoint[1] - 1] != 0 or self.map[currentPoint[0]][
                        currentPoint[1] - 1] == 99 and self.map[currentPoint[0]][currentPoint[1] + 1] == 99:
                        if self.map[currentPoint[0]][currentPoint[1]] == 12:
                            self.map[currentPoint[0]][currentPoint[1]] = 10
                        else:
                            self.map[currentPoint[0]][currentPoint[1]] = 0
                        currentPoint[0] += 1
                    else:
                        if self.map[currentPoint[0]][currentPoint[1] - 1] == 99 and self.map[currentPoint[0]][
                            currentPoint[1] + 1] == 0:
                            self.direction = 2
                        elif self.map[currentPoint[0]][currentPoint[1] + 1] == 99 and self.map[currentPoint[0]][
                            currentPoint[1] - 1] == 0:
                            self.direction = 1
                        else:
                            if currentPoint[1] == 1:
                                self.direction = 2
                            elif currentPoint[1] == self.columns - 2:
                                self.direction = 1
                            else:
                                self.direction = random.randint(1, 2)
                        length = self.coinfliper()
                        stoper += 1
                        if self.direction == 1:
                            if self.map[currentPoint[0]][currentPoint[1] + 1] != 0:
                                self.generateTheWay()
                                return
                            self.map[currentPoint[0]][currentPoint[1] + 1] = 99
                        else:
                            if self.map[currentPoint[0]][currentPoint[1] - 1] != 0:
                                self.generateTheWay()
                                return
                            self.map[currentPoint[0]][currentPoint[1] - 1] = 99
            elif self.direction == 3:
                if currentPoint[0] < self.rows - 2 and length > 0 and (
                        self.map[currentPoint[0] + 1][currentPoint[1]] == 10 or self.map[currentPoint[0] + 1][
                    currentPoint[1]] == 0):
                    if self.map[currentPoint[0]][currentPoint[1]] == 10:
                        self.map[currentPoint[0]][currentPoint[1]] = 12
                    currentPoint[0] += 1
                    if self.map[currentPoint[0]][currentPoint[1]] == 10:
                        self.map[currentPoint[0]][currentPoint[1]] = 12
                    else:
                        self.map[currentPoint[0]][currentPoint[1]] = 11
                    length -= 1
                else:
                    if self.map[currentPoint[0] - 1][currentPoint[1]] == 99:
                        self.map[currentPoint[0]][currentPoint[1]] = 6
                        if stoper < 10:
                            self.generateTheWay()
                            return
                        else:
                            break
                    elif self.map[currentPoint[0]][currentPoint[1] + 1] != 99 and self.map[currentPoint[0]][
                        currentPoint[1] + 1] != 0 and self.map[currentPoint[0]][currentPoint[1] - 1] != 99 and \
                            self.map[currentPoint[0]][currentPoint[1] - 1] != 0 or self.map[currentPoint[0]][
                        currentPoint[1] - 1] == 99 and self.map[currentPoint[0]][currentPoint[1] + 1] == 99:
                        if self.map[currentPoint[0]][currentPoint[1]] == 12:
                            self.map[currentPoint[0]][currentPoint[1]] = 10
                        else:
                            self.map[currentPoint[0]][currentPoint[1]] = 0
                        currentPoint[0] -= 1
                    else:
                        if self.map[currentPoint[0]][currentPoint[1] - 1] == 99 and self.map[currentPoint[0]][
                            currentPoint[1] + 1] == 0:
                            self.direction = 2
                        elif self.map[currentPoint[0]][currentPoint[1] + 1] == 99 and self.map[currentPoint[0]][
                            currentPoint[1] - 1] == 0:
                            self.direction = 1
                        else:
                            if currentPoint[1] == 1:
                                self.direction = 2
                            elif currentPoint[1] == self.columns - 2:
                                self.direction = 1
                            else:
                                self.direction = random.randint(1, 2)
                        length = self.coinfliper()
                        stoper += 1
                        if self.direction == 1:
                            if self.map[currentPoint[0]][currentPoint[1] + 1] != 0:
                                self.generateTheWay()
                                return
                            self.map[currentPoint[0]][currentPoint[1] + 1] = 99
                        else:
                            if self.map[currentPoint[0]][currentPoint[1] - 1] != 0:
                                self.generateTheWay()
                                return
                            self.map[currentPoint[0]][currentPoint[1] - 1] = 99
            elif self.direction == 2:
                if currentPoint[1] < self.columns - 2 and length > 0 and (
                        self.map[currentPoint[0]][currentPoint[1] + 1] == 11 or self.map[currentPoint[0]][
                    currentPoint[1] + 1] == 0):
                    if self.map[currentPoint[0]][currentPoint[1]] == 11:
                        self.map[currentPoint[0]][currentPoint[1]] = 12
                    currentPoint[1] += 1
                    if self.map[currentPoint[0]][currentPoint[1]] == 11:
                        self.map[currentPoint[0]][currentPoint[1]] = 12
                    else:
                        self.map[currentPoint[0]][currentPoint[1]] = 10
                    length -= 1
                else:
                    if self.map[currentPoint[0]][currentPoint[1] - 1] == 99:
                        self.map[currentPoint[0]][currentPoint[1]] = 6
                        if stoper < 10:
                            self.generateTheWay()
                            return
                        else:
                            break
                    elif self.map[currentPoint[0] + 1][currentPoint[1]] != 99 and self.map[currentPoint[0] + 1][
                        currentPoint[1]] != 0 and self.map[currentPoint[0] - 1][currentPoint[1]] != 99 and \
                            self.map[currentPoint[0] - 1][currentPoint[1]] != 0 or self.map[currentPoint[0] - 1][
                        currentPoint[1]] == 99 and self.map[currentPoint[0] + 1][currentPoint[1]] == 99:
                        if self.map[currentPoint[0]][currentPoint[1]] == 12:
                            self.map[currentPoint[0]][currentPoint[1]] = 11
                        else:
                            self.map[currentPoint[0]][currentPoint[1]] = 0
                        currentPoint[1] -= 1
                    else:
                        if self.map[currentPoint[0] - 1][currentPoint[1]] == 99 and self.map[currentPoint[0] + 1][
                            currentPoint[1]] == 0:
                            self.direction = 3
                        elif self.map[currentPoint[0] + 1][currentPoint[1]] == 99 and self.map[currentPoint[0] - 1][
                            currentPoint[1]] == 0:
                            self.direction = 4
                        else:
                            if currentPoint[0] == 1:
                                self.direction = 3
                            elif currentPoint[0] == self.rows - 2:
                                self.direction = 4
                            else:
                                self.direction = random.randint(3, 4)
                        length = self.coinfliper()
                        stoper += 1
                        if self.direction == 3:
                            if self.map[currentPoint[0] - 1][currentPoint[1]] != 0:
                                self.generateTheWay()
                                return
                            self.map[currentPoint[0] - 1][currentPoint[1]] = 99
                        else:
                            if self.map[currentPoint[0] + 1][currentPoint[1]] != 0:
                                self.generateTheWay()
                                return
                            self.map[currentPoint[0] + 1][currentPoint[1]] = 99
            elif self.direction == 1:
                if currentPoint[1] > 1 and length > 0 and (
                        self.map[currentPoint[0]][currentPoint[1] - 1] == 11 or self.map[currentPoint[0]][
                    currentPoint[1] - 1] == 0):
                    if self.map[currentPoint[0]][currentPoint[1]] == 11:
                        self.map[currentPoint[0]][currentPoint[1]] = 12
                    currentPoint[1] -= 1
                    if self.map[currentPoint[0]][currentPoint[1]] == 11:
                        self.map[currentPoint[0]][currentPoint[1]] = 12
                    else:
                        self.map[currentPoint[0]][currentPoint[1]] = 10
                    length -= 1
                else:
                    if self.map[currentPoint[0]][currentPoint[1] + 1] == 99:
                        self.map[currentPoint[0]][currentPoint[1]] = 6
                        if stoper < 10:
                            self.generateTheWay()
                            return
                        else:
                            break
                    elif self.map[currentPoint[0] + 1][currentPoint[1]] != 99 and self.map[currentPoint[0] + 1][
                        currentPoint[1]] != 0 and self.map[currentPoint[0] - 1][currentPoint[1]] != 99 and \
                            self.map[currentPoint[0] - 1][currentPoint[1]] != 0 or self.map[currentPoint[0] - 1][
                        currentPoint[1]] == 99 and self.map[currentPoint[0] + 1][currentPoint[1]] == 99:
                        if self.map[currentPoint[0]][currentPoint[1]] == 12:
                            self.map[currentPoint[0]][currentPoint[1]] = 11
                        else:
                            self.map[currentPoint[0]][currentPoint[1]] = 0
                        currentPoint[1] += 1
                    else:
                        if self.map[currentPoint[0] - 1][currentPoint[1]] == 99 and self.map[currentPoint[0] + 1][
                            currentPoint[1]] == 0:
                            self.direction = 3
                        elif self.map[currentPoint[0] + 1][currentPoint[1]] == 99 and self.map[currentPoint[0] - 1][
                            currentPoint[1]] == 0:
                            self.direction = 4
                        else:
                            if currentPoint[0] == 1:
                                self.direction = 3
                            elif currentPoint[0] == self.rows - 2:
                                self.direction = 4
                            else:
                                self.direction = random.randint(3, 4)
                        length = self.coinfliper()
                        stoper += 1
                        if self.direction == 3:
                            if self.map[currentPoint[0] - 1][currentPoint[1]] != 0:
                                self.generateTheWay()
                                return
                            self.map[currentPoint[0] - 1][currentPoint[1]] = 99
                        else:
                            if self.map[currentPoint[0] + 1][currentPoint[1]] != 0:
                                self.generateTheWay()
                                return
                            self.map[currentPoint[0] + 1][currentPoint[1]] = 99
        self.checker()
        self.cleanTheWay()

    def checker(self):
        we_have_7 = False
        we_have_6 = False
        for y in range(self.rows):
            for x in range(self.columns):
                if self.map[y][x] == 7:
                    we_have_7 = True
                if self.map[y][x] == 6:
                    we_have_6 = True
            if we_have_7:
                break
        if not we_have_7 or not we_have_6:
            self.generateTheWay()

    def cleanTheWay(self):
        flag = False
        for y in range(self.rows):
            for x in range(self.columns):
                if self.map[y][x] == 10:
                    flag = True
        if flag:
            for y in range(self.rows):
                for x in range(self.columns):
                    if self.map[y][x] == 0 and random.randint(1, 15) == 1:
                        self.map[y][x] = 99
        for y in range(self.rows):
            for x in range(self.columns):
                if self.map[y][x] == 99:
                    self.map[y][x] = 1
                elif self.map[y][x] != 6 and self.map[y][x] != 7 and self.map[y][x] != 1:
                    self.map[y][x] = 0
        starter = [999, 999]
        for y in range(self.rows):
            for x in range(self.columns):
                if self.map[y][x] == 6:
                    starter = [y, x]
                    break
            if starter != [999, 999]:
                break
        self.stop_tunneler = False
        self.tunneler(1, starter, 0)
        self.tunneler(2, starter, 0)
        self.tunneler(3, starter, 0)
        self.tunneler(4, starter, 0)
        self.stop_tunneler = True

    def tunneler(self, direction, lastpoint, count):
        if self.stop_tunneler or count > 10:
            return
        currentPoint = [0, 0]
        currentPoint[0] = lastpoint[0]
        currentPoint[1] = lastpoint[1]
        if direction == 1:
            while currentPoint[1] > 0 and self.map[currentPoint[0]][currentPoint[1] - 1] != 1 and \
                    self.map[currentPoint[0]][currentPoint[1]] != 7:
                currentPoint[1] -= 1
            if self.map[currentPoint[0]][currentPoint[1]] == 7:
                self.generateTheWay()
                return
            if currentPoint[1] > 0:
                self.tunneler(3, currentPoint, count + 1)
                self.tunneler(4, currentPoint, count + 1)
        elif direction == 2:
            while currentPoint[1] < self.columns - 1 and self.map[currentPoint[0]][currentPoint[1] + 1] != 1 and \
                    self.map[currentPoint[0]][currentPoint[1]] != 7:
                currentPoint[1] += 1
            if self.map[currentPoint[0]][currentPoint[1]] == 7:
                self.generateTheWay()
                return
            if currentPoint[1] < self.columns - 1:
                self.tunneler(3, currentPoint, count + 1)
                self.tunneler(4, currentPoint, count + 1)
        elif direction == 3:
            while currentPoint[0] < self.rows - 1 and self.map[currentPoint[0] + 1][currentPoint[1]] != 1 and \
                    self.map[currentPoint[0]][currentPoint[1]] != 7:
                currentPoint[0] += 1
            if self.map[currentPoint[0]][currentPoint[1]] == 7:
                self.generateTheWay()
                return
            if currentPoint[1] < self.rows - 1:
                self.tunneler(1, currentPoint, count + 1)
                self.tunneler(2, currentPoint, count + 1)
        elif direction == 4:
            while currentPoint[0] > 0 and self.map[currentPoint[0] - 1][currentPoint[1]] != 1 and \
                    self.map[currentPoint[0]][currentPoint[1]] != 7:
                currentPoint[0] -= 1
            if self.map[currentPoint[0]][currentPoint[1]] == 7:
                self.generateTheWay()
                return
            if currentPoint[1] > 0:
                self.tunneler(1, currentPoint, count + 1)
                self.tunneler(2, currentPoint, count + 1)
        return

    def __init__(self):
        self.map = []
        self.columns = random.randint(9, 20)
        self.rows = random.randint(9, self.columns)
        for y in range(self.rows):
            self.map.append([])
            for x in range(self.columns):
                self.map[y].append(0)


maps = [
    [
        [0, 0, 1, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 6, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0]
    ]
]


def _neighbors(y, x, rows, cols):
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < rows and 0 <= nx < cols:
            yield ny, nx


def _find_value(game_map, value):
    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            if game_map[y][x] == value:
                return y, x
    return None


def _bfs_path(game_map, start, finish, passable_values):
    rows, cols = len(game_map), len(game_map[0])
    queue = [start]
    parent = {start: None}
    while queue:
        current = queue.pop(0)
        if current == finish:
            break
        cy, cx = current
        for ny, nx in _neighbors(cy, cx, rows, cols):
            if (ny, nx) in parent:
                continue
            if game_map[ny][nx] not in passable_values:
                continue
            parent[(ny, nx)] = current
            queue.append((ny, nx))
    if finish not in parent:
        return []
    path = []
    cur = finish
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


def _bfs_exists(game_map, start, finish, passable_values):
    return len(_bfs_path(game_map, start, finish, passable_values)) > 0


def _flood_component(game_map, start, passable_values):
    rows, cols = len(game_map), len(game_map[0])
    stack = [start]
    seen = {start}
    while stack:
        y, x = stack.pop()
        for ny, nx in _neighbors(y, x, rows, cols):
            if (ny, nx) in seen:
                continue
            if game_map[ny][nx] not in passable_values:
                continue
            seen.add((ny, nx))
            stack.append((ny, nx))
    return seen


def _state_route_exists(game_map, start, finish, block_cell):
    """
    Validate gameplay sequence on sliding movement:
    - hit one-time block (break it),
    - next move must be a turn (different direction),
    - later pass through former block cell,
    - reach finish.
    """
    rows, cols = len(game_map), len(game_map[0])
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # state: (y, x, broken, passed_block_after_break, need_turn, hit_direction)
    # hit_direction is index in dirs (the direction used to hit one-time block).
    start_state = (start[0], start[1], False, False, False, -1)
    queue = [start_state]
    seen = {start_state}

    def is_wall(y, x, broken):
        value = game_map[y][x]
        if value == 1:
            return True
        if value == 8 and not broken:
            return True
        return False

    while queue:
        y, x, broken, passed, need_turn, hit_direction = queue.pop(0)
        if (y, x) == finish and broken and passed:
            return True

        for dir_idx, (dy, dx) in enumerate(dirs):
            # After hitting one-time block, next move must change direction
            # (cannot repeat the same direction that hit the block).
            if need_turn:
                if dir_idx == hit_direction:
                    continue

            cy, cx = y, x
            new_broken = broken
            new_passed = passed
            hit_happened = False

            while True:
                ny, nx = cy + dy, cx + dx
                # Border behavior in game: leaving map means death, so invalid for successful route.
                if ny < 0 or ny >= rows or nx < 0 or nx >= cols:
                    hit_happened = False
                    break

                if game_map[ny][nx] == 8 and not new_broken:
                    # Hit one-time block: break and stop before it.
                    new_broken = True
                    hit_happened = True
                    break

                if is_wall(ny, nx, new_broken):
                    break

                cy, cx = ny, nx
                if new_broken and (cy, cx) == block_cell:
                    new_passed = True

            # No movement and no hit -> ignore.
            if (cy, cx) == (y, x) and not hit_happened:
                continue

            new_need_turn = False
            new_hit_direction = -1
            if hit_happened:
                new_need_turn = True
                new_hit_direction = dir_idx

            state = (cy, cx, new_broken, new_passed, new_need_turn, new_hit_direction)
            if state not in seen:
                seen.add(state)
                queue.append(state)
    return False


def _has_forbidden_early_finish(game_map, start, finish, block_cell):
    """
    Return True if finish can be reached too early:
    before both conditions are satisfied:
    - one-time block has been broken
    - former one-time block cell has been passed after break
    """
    rows, cols = len(game_map), len(game_map[0])
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # state: (y, x, broken, passed_block_after_break, need_turn, hit_direction)
    start_state = (start[0], start[1], False, False, False, -1)
    queue = [start_state]
    seen = {start_state}

    def is_wall(y, x, broken):
        value = game_map[y][x]
        if value == 1:
            return True
        if value == 8 and not broken:
            return True
        return False

    while queue:
        y, x, broken, passed, need_turn, hit_direction = queue.pop(0)
        if (y, x) == finish and not (broken and passed):
            return True

        for dir_idx, (dy, dx) in enumerate(dirs):
            if need_turn:
                if dir_idx == hit_direction:
                    continue

            cy, cx = y, x
            new_broken = broken
            new_passed = passed
            hit_happened = False

            while True:
                ny, nx = cy + dy, cx + dx
                if ny < 0 or ny >= rows or nx < 0 or nx >= cols:
                    hit_happened = False
                    break

                # Reaching finish at any point of the slide is a win in-game.
                if (ny, nx) == finish and not (new_broken and new_passed):
                    return True

                if game_map[ny][nx] == 8 and not new_broken:
                    new_broken = True
                    hit_happened = True
                    break

                if is_wall(ny, nx, new_broken):
                    break

                cy, cx = ny, nx
                if new_broken and (cy, cx) == block_cell:
                    new_passed = True

            if (cy, cx) == (y, x) and not hit_happened:
                continue

            new_need_turn = False
            new_hit_direction = -1
            if hit_happened:
                new_need_turn = True
                new_hit_direction = dir_idx

            state = (cy, cx, new_broken, new_passed, new_need_turn, new_hit_direction)
            if state not in seen:
                seen.add(state)
                queue.append(state)
    return False


def _can_hit_one_time_on_first_move(game_map, start):
    """True if one-time block can be hit from spawn in one key press."""
    rows, cols = len(game_map), len(game_map[0])
    y, x = start
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        cy, cx = y, x
        while True:
            ny, nx = cy + dy, cx + dx
            if ny < 0 or ny >= rows or nx < 0 or nx >= cols:
                break
            cell = game_map[ny][nx]
            if cell == 8:
                return True
            if cell == 1:
                break
            cy, cx = ny, nx
    return False


def _can_reach_finish_actual_rules(game_map, start, finish, block_cell):
    """
    Reachability with gameplay-accurate rules:
    - sliding until wall/border/8
    - hitting 8 stops before it, and it breaks for the next move
    - after hit, next move must change direction
    - crossing finish during slide counts as win
    """
    rows, cols = len(game_map), len(game_map[0])
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # state: (y, x, broken, passed_block_after_break, need_turn, hit_direction)
    start_state = (start[0], start[1], False, False, False, -1)
    queue = [start_state]
    seen = {start_state}

    while queue:
        y, x, broken, passed, need_turn, hit_direction = queue.pop(0)
        for dir_idx, (dy, dx) in enumerate(dirs):
            if need_turn:
                if dir_idx == hit_direction:
                    continue

            cy, cx = y, x
            new_broken = broken
            new_passed = passed
            hit_happened = False

            while True:
                ny, nx = cy + dy, cx + dx
                if ny < 0 or ny >= rows or nx < 0 or nx >= cols:
                    hit_happened = False
                    break

                if (ny, nx) == finish and new_broken and new_passed:
                    return True

                cell = game_map[ny][nx]
                if cell == 8 and not new_broken:
                    new_broken = True
                    hit_happened = True
                    break
                if cell == 1:
                    break

                cy, cx = ny, nx
                if new_broken and (cy, cx) == block_cell:
                    new_passed = True

            if (cy, cx) == (y, x) and not hit_happened:
                continue

            new_need_turn = False
            new_hit_direction = -1
            if hit_happened:
                new_need_turn = True
                new_hit_direction = dir_idx

            state = (cy, cx, new_broken, new_passed, new_need_turn, new_hit_direction)
            if state not in seen:
                seen.add(state)
                queue.append(state)

    return False


def _min_actions_to_finish(game_map, start, finish):
    """
    Minimal number of key presses to reach finish with current movement rules.
    Returns None if finish is unreachable.
    """
    rows, cols = len(game_map), len(game_map[0])
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    # state: (y, x, broken, need_turn, hit_direction)
    start_state = (start[0], start[1], False, False, -1)
    queue = [(start_state, 0)]
    seen = {start_state}

    while queue:
        (y, x, broken, need_turn, hit_direction), steps = queue.pop(0)
        for dir_idx, (dy, dx) in enumerate(dirs):
            if need_turn and dir_idx == hit_direction:
                continue

            cy, cx = y, x
            new_broken = broken
            hit_happened = False

            while True:
                ny, nx = cy + dy, cx + dx
                if ny < 0 or ny >= rows or nx < 0 or nx >= cols:
                    hit_happened = False
                    break
                if (ny, nx) == finish:
                    return steps + 1

                cell = game_map[ny][nx]
                if cell == 8 and not new_broken:
                    new_broken = True
                    hit_happened = True
                    break
                if cell == 1:
                    break

                cy, cx = ny, nx

            if (cy, cx) == (y, x) and not hit_happened:
                continue

            new_need_turn = hit_happened
            new_hit_direction = dir_idx if hit_happened else -1
            state = (cy, cx, new_broken, new_need_turn, new_hit_direction)
            if state not in seen:
                seen.add(state)
                queue.append((state, steps + 1))

    return None


def _actual_finish_metrics(game_map, start, finish, block_cell):
    """
    Exact BFS by in-game one-time behavior.
    Returns (min_any_finish_steps, min_progress_finish_steps),
    where progress means: one-time consumed and former block cell passed.
    """
    rows, cols = len(game_map), len(game_map[0])
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # state: (y, x, block_alive, pending_hit_direction, passed_after_break)
    start_state = (start[0], start[1], True, -1, False)
    queue = [(start_state, 0)]
    seen = {start_state}

    min_any = None
    min_progress = None

    while queue:
        (y, x, block_alive, pending_dir, passed), steps = queue.pop(0)
        for dir_idx, (dy, dx) in enumerate(dirs):
            new_block_alive = block_alive
            new_pending = pending_dir
            new_passed = passed

            # One-time block disappears only when next direction differs from hit direction.
            if new_pending != -1 and dir_idx != new_pending and new_block_alive:
                new_block_alive = False
                new_pending = -1

            cy, cx = y, x
            hit_happened = False
            died = False

            while True:
                ny, nx = cy + dy, cx + dx
                if ny < 0 or ny >= rows or nx < 0 or nx >= cols:
                    died = True
                    break

                if (ny, nx) == finish:
                    candidate = steps + 1
                    if min_any is None or candidate < min_any:
                        min_any = candidate
                    if (not new_block_alive) and new_passed:
                        if min_progress is None or candidate < min_progress:
                            min_progress = candidate
                    break

                cell = game_map[ny][nx]
                if cell == 1:
                    break
                if cell == 8 and new_block_alive:
                    hit_happened = True
                    new_pending = dir_idx
                    break

                cy, cx = ny, nx
                if (not new_block_alive) and (cy, cx) == block_cell:
                    new_passed = True

            if died:
                continue
            if (cy, cx) == (y, x) and not hit_happened:
                continue

            state = (cy, cx, new_block_alive, new_pending, new_passed)
            if state not in seen:
                seen.add(state)
                queue.append((state, steps + 1))

    return min_any, min_progress


def _gamma_has_backtrack_skip(game_map, start, first_move, revisit_stop):
    """
    Detect gamma exploit:
    hit one-time -> go back -> go toward former one-time,
    and instantly land on revisit step stop.
    """
    rows, cols = len(game_map), len(game_map[0])

    def slide_once(y, x, dy, dx, block_alive, pending_dir, move_dir_idx):
        # One-time disappears when direction changes after hit.
        if pending_dir != -1 and move_dir_idx != pending_dir and block_alive:
            block_alive = False
            pending_dir = -1

        cy, cx = y, x
        hit = False
        while True:
            ny, nx = cy + dy, cx + dx
            if ny < 0 or ny >= rows or nx < 0 or nx >= cols:
                return None
            cell = game_map[ny][nx]
            if cell == 1:
                break
            if cell == 8 and block_alive:
                hit = True
                pending_dir = move_dir_idx
                break
            cy, cx = ny, nx
        return cy, cx, block_alive, pending_dir, hit

    move_to_idx = {(1, 0): 0, (-1, 0): 1, (0, 1): 2, (0, -1): 3}
    dy1, dx1 = first_move
    dir1 = move_to_idx[(dy1, dx1)]
    dir_back = move_to_idx[(-dy1, -dx1)]

    # 1) Hit one-time block on first move.
    r1 = slide_once(start[0], start[1], dy1, dx1, True, -1, dir1)
    if r1 is None:
        return False
    y, x, block_alive, pending_dir, hit = r1
    if not hit:
        return False

    # 2) Go back (block disappears here).
    r2 = slide_once(y, x, -dy1, -dx1, block_alive, pending_dir, dir_back)
    if r2 is None:
        return False
    y, x, block_alive, pending_dir, _ = r2

    # 3) Go toward former one-time again.
    r3 = slide_once(y, x, dy1, dx1, block_alive, pending_dir, dir1)
    if r3 is None:
        return False
    y, x, _, _, _ = r3

    return (y, x) == revisit_stop


def _slide_can_reach_finish_without_break(game_map, start, finish):
    """Check if finish is reachable when one-time blocks are treated as solid walls."""
    rows, cols = len(game_map), len(game_map[0])
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    queue = [start]
    seen = {start}
    while queue:
        y, x = queue.pop(0)
        if (y, x) == finish:
            return True
        for dy, dx in dirs:
            cy, cx = y, x
            while True:
                ny, nx = cy + dy, cx + dx
                if ny < 0 or ny >= rows or nx < 0 or nx >= cols:
                    break
                if game_map[ny][nx] in (1, 8):
                    break
                cy, cx = ny, nx
            if (cy, cx) != (y, x) and (cy, cx) not in seen:
                seen.add((cy, cx))
                queue.append((cy, cx))
    return False


def _matches_required_sequence(game_map, stops, moves, hit_move_idx, revisit_move_idx):
    """
    Validate exact movement sequence and exact stop points.
    """
    rows, cols = len(game_map), len(game_map[0])
    block_cell = None
    for y in range(rows):
        for x in range(cols):
            if game_map[y][x] == 8:
                block_cell = (y, x)
                break
        if block_cell is not None:
            break
    if block_cell is None:
        return False

    y, x = stops[0]
    broken = False
    pending_break = False

    finish_cell = stops[-1]

    for i, (dy, dx) in enumerate(moves, start=1):
        if pending_break:
            broken = True
            pending_break = False

        cy, cx = y, x
        traversed = []
        hit_block = False
        while True:
            ny, nx = cy + dy, cx + dx
            if ny < 0 or ny >= rows or nx < 0 or nx >= cols:
                return False
            cell = game_map[ny][nx]
            # Finish must be reached only on the last move endpoint.
            if (ny, nx) == finish_cell and i != len(moves):
                return False
            if cell == 1:
                break
            if cell == 8 and not broken:
                hit_block = True
                pending_break = True
                break
            cy, cx = ny, nx
            traversed.append((cy, cx))

        y, x = cy, cx
        if (y, x) != stops[i]:
            return False
        if i == hit_move_idx and not hit_block:
            return False
        # On revisit move we must pass through former one-time point.
        if i == revisit_move_idx and block_cell not in traversed:
            return False

    return True


def _add_decoy_one_time_blocks(game_map, protected_cells):
    """Place extra one-time blocks outside required route cells."""
    rows, cols = len(game_map), len(game_map[0])
    candidates = []
    for y in range(1, rows - 1):
        for x in range(1, cols - 1):
            if (y, x) in protected_cells:
                continue
            if game_map[y][x] != 0:
                continue
            candidates.append((y, x))

    if not candidates:
        return

    random.shuffle(candidates)
    amount = random.randint(DECOY_ONE_TIME_BLOCKS_MIN, DECOY_ONE_TIME_BLOCKS_MAX)
    amount = min(amount, len(candidates))
    for y, x in candidates[:amount]:
        game_map[y][x] = 8


def generate_one_time_map(base_map):
    """
    Build one-time puzzle as continuation of a normally generated level:
    normal start -> normal finish(point1) -> one-time puzzle -> new finish.
    """
    if not base_map or not base_map[0]:
        return None

    rows, cols = len(base_map), len(base_map[0])
    start_cell = _find_value(base_map, 6)
    point1 = _find_value(base_map, 7)
    if start_cell is None or point1 is None:
        return None

    def in_bounds(y, x):
        return 0 <= y < rows and 0 <= x < cols

    if ACTIVE_ONE_TIME_TEMPLATE == "beta":
        base_moves = ONE_TIME_TEMPLATE_BETA
        hit_move_idx = 3
        revisit_move_idx = 8
    elif ACTIVE_ONE_TIME_TEMPLATE == "gamma":
        base_moves = ONE_TIME_TEMPLATE_GAMMA
        hit_move_idx = 1
        revisit_move_idx = 8
    else:
        base_moves = ONE_TIME_TEMPLATE_ALPHA
        hit_move_idx = 3
        revisit_move_idx = 8

    # 4 reflections of one base template:
    # original, horizontal mirror, vertical mirror, both mirrors.
    templates = [
        base_moves,
        [(dy, -dx) for dy, dx in base_moves],
        [(-dy, dx) for dy, dx in base_moves],
        [(-dy, -dx) for dy, dx in base_moves],
    ]

    # Random segment-length variation while preserving route order.
    # Beta has a long right-side "exit" branch, so last segment allows larger range.
    if ACTIVE_ONE_TIME_TEMPLATE == "beta":
        length_ranges = [(1, 4), (1, 3), (1, 4), (1, 3), (1, 4), (1, 4), (1, 3), (1, 4), (2, 6)]
    elif ACTIVE_ONE_TIME_TEMPLATE == "gamma":
        length_ranges = [(1, 4), (1, 3), (2, 5), (1, 3), (2, 5), (2, 5), (1, 4), (1, 3), (1, 4)]
    else:
        length_ranges = [(1, 4), (1, 3), (1, 3), (1, 3), (1, 3), (1, 4), (1, 3), (1, 3), (1, 3)]

    valid_maps_by_template = [[] for _ in templates]
    for template_idx, moves in enumerate(templates):
        for _ in range(180):
            if ACTIVE_ONE_TIME_TEMPLATE == "beta":
                # Beta geometry constraints to guarantee revisit through one-time cell:
                # move7 length must cancel vertical offset from moves4+6,
                # move8 must be long enough to cross former one-time x.
                l1 = random.randint(1, 4)
                l2 = random.randint(1, 3)
                l3 = random.randint(2, 4)
                l4 = random.randint(1, 2)
                l5 = random.randint(1, 3)
                l6 = random.randint(1, 4)
                l7 = l4 + l6
                l8 = random.randint(l5 + 1, l5 + 4)
                l9 = random.randint(2, 6)
                lengths = [l1, l2, l3, l4, l5, l6, l7, l8, l9]
            elif ACTIVE_ONE_TIME_TEMPLATE == "gamma":
                # Gamma with first move hitting one-time block, then random variation.
                l1 = 0
                l2 = random.randint(1, 3)
                l3 = random.randint(2, 5)
                l4 = random.randint(1, 3)
                l5 = random.randint(2, 5)
                l6 = random.randint(1, 4)
                # Keep move8 vertical line passing through former one-time x.
                l7 = l3 + l5 - 1
                y_before_up = l2 + l4 - l6
                if y_before_up < 1:
                    continue
                l8 = random.randint(y_before_up, y_before_up + 2)
                l9 = random.randint(1, 3)
                lengths = [l1, l2, l3, l4, l5, l6, l7, l8, l9]
            else:
                lengths = [random.randint(lo, hi) for lo, hi in length_ranges]

            # Build stops from point1 (former normal finish).
            stops = [point1]
            for i, (dy, dx) in enumerate(moves):
                py, px = stops[-1]
                stops.append((py + dy * lengths[i], px + dx * lengths[i]))

            if not all(in_bounds(y, x) for y, x in stops):
                continue

            game_map = [row[:] for row in base_map]
            block_cell = None
            ok = True
            route_cells = set()
            stopper_cells = set()

            # Collect all cells the intended route passes through.
            for i in range(1, len(stops)):
                py, px = stops[i - 1]
                cy, cx = stops[i]
                if py == cy:
                    for x in range(min(px, cx), max(px, cx) + 1):
                        route_cells.add((py, x))
                elif px == cx:
                    for y in range(min(py, cy), max(py, cy) + 1):
                        route_cells.add((y, px))

            for i in range(1, len(stops)):
                py, px = stops[i - 1]
                cy, cx = stops[i]
                dy, dx = moves[i - 1]
                by, bx = cy + dy, cx + dx

                if not in_bounds(by, bx):
                    ok = False
                    break
                if (by, bx) in stops:
                    ok = False
                    break
                # Ordinary stop blocks must not block any other route segment.
                # (one-time block on hit_move_idx is allowed on route by design)
                if i != hit_move_idx and (by, bx) in route_cells:
                    ok = False
                    break
                stopper_cells.add((by, bx))

            if not ok:
                continue

            # Remove normal finish marker: now it's point1 (ordinary part end).
            p1y, p1x = point1
            game_map[p1y][p1x] = 0

            # Keep combined level valid: normal random walls must not occupy special route.
            # Clear route and stopper cells before placing required puzzle blockers.
            for ry, rx in route_cells:
                if (ry, rx) == start_cell:
                    ok = False
                    break
                game_map[ry][rx] = 0
            if not ok:
                continue
            for by, bx in stopper_cells:
                if (by, bx) == start_cell:
                    ok = False
                    break
                game_map[by][bx] = 0
            if not ok:
                continue

            for i in range(1, len(stops)):
                cy, cx = stops[i]
                dy, dx = moves[i - 1]
                by, bx = cy + dy, cx + dx
                if i == hit_move_idx:
                    game_map[by][bx] = 8
                    block_cell = (by, bx)
                else:
                    game_map[by][bx] = 1

            if block_cell is None:
                continue

            sy, sx = stops[0]
            fy, fx = stops[-1]
            game_map[start_cell[0]][start_cell[1]] = 6
            game_map[sy][sx] = 0
            game_map[fy][fx] = 7

            if _slide_can_reach_finish_without_break(game_map, (sy, sx), (fy, fx)):
                continue
            if not _state_route_exists(game_map, start_cell, (fy, fx), block_cell):
                continue
            if not _can_reach_finish_actual_rules(game_map, start_cell, (fy, fx), block_cell):
                continue
            if _has_forbidden_early_finish(game_map, start_cell, (fy, fx), block_cell):
                continue
            min_steps = _min_actions_to_finish(game_map, start_cell, (fy, fx))
            if min_steps is None or min_steps <= 2:
                continue
            min_any, min_progress = _actual_finish_metrics(game_map, start_cell, (fy, fx), block_cell)
            if min_progress is None:
                continue
            if min_any is not None and min_any < min_progress:
                continue
            if ACTIVE_ONE_TIME_TEMPLATE == "gamma":
                # Gamma expects immediate first-hit behavior by template definition.
                if not _can_hit_one_time_on_first_move(game_map, (sy, sx)):
                    continue
            else:
                if _can_hit_one_time_on_first_move(game_map, (sy, sx)):
                    continue
            if not _matches_required_sequence(
                game_map,
                stops,
                moves,
                hit_move_idx=hit_move_idx,
                revisit_move_idx=revisit_move_idx
            ):
                continue
            if ACTIVE_ONE_TIME_TEMPLATE == "gamma":
                if _gamma_has_backtrack_skip(game_map, (sy, sx), moves[0], stops[revisit_move_idx]):
                    continue

            protected_cells = set(route_cells)
            protected_cells.update(stopper_cells)
            protected_cells.add(start_cell)
            protected_cells.add((sy, sx))
            protected_cells.add((fy, fx))
            protected_cells.add(block_cell)
            _add_decoy_one_time_blocks(game_map, protected_cells)

            valid_maps_by_template[template_idx].append(game_map)

    non_empty_groups = [group for group in valid_maps_by_template if group]
    if not non_empty_groups:
        return None

    # Keep template diversity: first pick template group, then map variant.
    chosen_group = random.choice(non_empty_groups)
    return random.choice(chosen_group)


