import sys
from random import *
# a = []
# for i in range(7):
#     a.append([int(x) for x in input()])
a = [[int(i) for i in line.replace('\n', '')] for line in sys.stdin]

EMPTY = 0
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4
HEAD = 5
START = 7
FINAL = 8
WALL = 9

# direction = {0: "up", 1: "right", 2: "down", 3: "left"}


class Board:
    # __slots__ = ('matrix', 'empty')

    moves = {WALL: u'▓', EMPTY: ' ', UP: u'↑', RIGHT: u'→',
             DOWN: u'↓', LEFT: u'←', START: 'S', FINAL: 'F'}

    def __init__(self, matrix: list[list[int]]) -> None:
        self.matrix = matrix
        self.empty = set()
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if not self.matrix[i][j]:
                    self.empty.add((i, j))

    def __repr__(self) -> str:
        return '\n'.join([''.join(self.moves[x] for x in a[i]) for i in range(len(a))]) + '\n'

    # def get_starts(self) -> list[tuple[int, int]]:
    #     return [(i, j) for i in range(len(self.matrix)) for j in range(len(self.matrix[i])) if not self.matrix[i][j]]

    def set_loc(self, coords: tuple[int, int], val: int) -> None:
        row, col = coords
        if not self.matrix[row][col]:
            self.empty.remove((row, col))
        if not val:
            self.empty.add((row, col))
        self.matrix[row][col] = val

    def walk(self, coords: tuple[int, int], d: int) -> tuple[int, int]:
        row, col = coords
        if d == UP:
            while row > 0 and not self.matrix[row-1][col]:
                row -= 1
                self.empty.remove((row, col))
                self.matrix[row][col] = UP
            return (row, col)
        elif d == RIGHT:
            col_max = len(self.matrix[row]) - 1
            while col < col_max and not self.matrix[row][col+1]:
                col += 1
                self.empty.remove((row, col))
                self.matrix[row][col] = RIGHT
            return (row, col)
        elif d == DOWN:
            row_max = len(self.matrix) - 1
            while row < row_max and not self.matrix[row+1][col]:
                row += 1
                self.empty.remove((row, col))
                self.matrix[row][col] = DOWN
            return (row, col)
        elif d == LEFT:
            while col > 0 and not self.matrix[row][col-1]:
                col -= 1
                self.empty.remove((row, col))
                self.matrix[row][col] = LEFT
            return (row, col)

    def undo(self, start: tuple[int, int], end: tuple[int, int]) -> bool:
        if (start[0] < end[0]):
            # (0, 0) -> (2, 0)
            row1 = start[0]
            row2 = end[0]
            while row1 < row2:
                self.empty.add((row1, start[1]))
                self.matrix[row1][start[1]] = EMPTY
                row1 += 1
                break
        elif (start[0] > end[0]):
            # (2, 0) -> (0, 0)
            row1 = start[0]
            row2 = end[0]
            while row1 > row2:
                self.empty.add((row1, start[1]))
                self.matrix[row1][start[1]] = EMPTY
                row1 -= 1
                break
        elif (start[1] < end[1]):
            # (0, 0) -> (0, 2)
            col1 = start[1]
            col2 = end[1]
            while col1 < col2:
                self.empty.add((start[0], col1))
                self.matrix[start[0]][col1] = EMPTY
                col1 += 1
                break
        elif (start[1] < end[1]):
            # (0, 2) -> (0, 0)
            col1 = start[1]
            col2 = end[1]
            while col1 > col2:
                self.empty.add((start[0], col1))
                self.matrix[start[0]][col1] = EMPTY
                col1 -= 1
                break
        return True

    def is_solved(self) -> bool:
        return len(self.empty) == 0

    def can_be_solved(self) -> bool:
        start = choice(tuple(self.empty))
        not_seen = self.empty.copy()

        not_seen.remove(start)
        stack: list[tuple[int, int]] = [start]

        while stack:
            x, y = stack.pop()
            if (x+1, y) in not_seen:
                stack.append((x+1, y))
                not_seen.remove((x+1, y))
            if (x-1, y) in not_seen:
                stack.append((x-1, y))
                not_seen.remove((x-1, y))
            if (x, y+1) in not_seen:
                stack.append((x, y+1))
                not_seen.remove((x, y+1))
            if (x, y-1) in not_seen:
                stack.append((x, y-1))
                not_seen.remove((x, y-1))
        return len(not_seen) == 0

    def find_solutions(self) -> list[str]:
        solutions = []
        starts = self.empty.copy()
        d = 0

        while starts:
            start = choice(tuple(self.empty))
            moves = {start: [UP, RIGHT, LEFT, DOWN]}
            while moves:
                moves[start].remove(UP)
                self.walk(start, UP)

                moves[start].remove(LEFT)
                self.walk(start, LEFT)

                moves[start].remove(DOWN)
                self.walk(start, DOWN)

                moves[start].remove(RIGHT)
                self.walk(start, RIGHT)
                break
            break
        # list of starts = all whitespace
        # get random start
        # v2 smart start

        # dfs (return solution if found)
        # break if more than 2 bubbles found
        # repeat
        return solutions

# test 1
# b = Board(a)
# print(b)
# b.set_loc(2, 2, START)
# print(b)
# print(b.can_be_solved())
# x, y = b.walk(2, 2, DOWN)
# print(b)
# print(b.can_be_solved())
# x, y = b.walk(x, y, LEFT)
# print(b)
# print(b.can_be_solved())
# x, y = b.walk(x, y, UP)
# print(b)
# print(b.can_be_solved())
# x, y = b.walk(x, y, RIGHT)
# print(b)
# print(b.can_be_solved())
# x, y = b.walk(x, y, DOWN)
# print(b)
# print(b.can_be_solved())
# x, y = b.walk(x, y, LEFT)
# print(b)
# print(b.can_be_solved())
# x, y = b.walk(x, y, DOWN)
# print(b)
# print(b.can_be_solved())
# x, y = b.walk(x, y, RIGHT)
# print(b)
# print(b.can_be_solved())
# x, y = b.walk(x, y, UP)
# print(b)
# print(b.can_be_solved())


b = Board(a)
print(b)
b.set_loc((2, 1), START)
print(b)
print(b.can_be_solved())
x, y = b.walk((2, 1), RIGHT)
print(b)
print(b.empty)
print(b.can_be_solved())
