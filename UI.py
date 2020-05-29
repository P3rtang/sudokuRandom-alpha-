from tkinter import *
import subprocess
import ghostscript
import os
import random as rand
import copy


def check(x, y, n, g):
    xb = (x // 3)*3
    yb = (y // 3)*3

    for k in range(3):
        for l in range(3):
            if g[yb+k][xb+l] == n:
                return False

    for k in range(9):
        if g[y][k] == n:
            return False

    for k in range(9):
        if g[k][x] == n:
            return False

    return True


def solve(g):
    for x in range(9):
        for y in range(9):
            if g[y][x] == 0:
                for n in range(1,10):
                    if check(x, y, n, g):
                        g[y][x] = n
                        if not any(0 in i for i in g):
                            solutions.append(g)
                            global sols
                            sols = copy.deepcopy(solutions)
                            return
                        solve(g)
                        g[y][x] = 0
                return

def solveAll(g):
    global solutions
    solutions = list()
    global sols

    solve(g)

    return sols


def format(string):
    sudoku = []
    puzzle = str(string).split()
    if len(puzzle) != 81:
        raise Exception
    for x in range(9):
        temp = list()
        for y in puzzle[x*9:(x+1)*9]:
            temp.append(int(y))
        sudoku.append(temp)
    solve(sudoku)


def build():
    # build empty grid
    grid = []
    for x in range(9):
        temp = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        grid.append(temp)

    # build random diagonal
    for x in [0, 3, 6]:
        a, b, c = rand.sample(range(1, 10), 3)
        grid[x][x] = a
        grid[x + 1][x + 1] = b
        grid[x + 2][x + 2] = c

    bestSudoku = {}
    empty = 0
    tries = 0

    a = solveAll(grid)

    sudoku = a[-1]

    x = rand.randrange(9)
    y = rand.randrange(9)
    b = sudoku[x][y]
    c = sudoku[8 - x][8 - y]
    sudoku[x][y] = 0
    sudoku[8 - x][8 - y] = 0
    tester = copy.deepcopy(sudoku)

    pos = solveAll(tester)

    while empty < 52 and tries < 100:
        while len(pos) == 1 and tries < 100:
            x = rand.randrange(9)
            y = rand.randrange(9)
            b = sudoku[x][y]
            c = sudoku[8 - x][8 - y]
            if b != 0:
                sudoku[x][y] = 0
                sudoku[8 - x][8 - y] = 0
                tester = copy.deepcopy(sudoku)
                pos = solveAll(tester)
                if __name__ == '__main__':
                    print(empty, ': ', sudoku)
            tries += 1
            if tries % 10 == 1:
                print('=', end='')

        sudoku[8 - x][8 - y] = c
        sudoku[x][y] = b
        tester = copy.deepcopy(sudoku)
        pos = solveAll(tester)

        empty = 0
        for s in sudoku:
            empty += s.count(0)

    return sudoku


class UI:
    def __init__(self):
        self.sud = build()
        # self.sud =  [[0, 0, 0, 0, 0, 0, 6, 3, 2], [6, 0, 1, 0, 0, 0, 0, 5, 0], [0, 2, 0, 7, 0, 6, 9, 0, 0], [0, 7, 3, 5, 0, 0, 0, 8, 0], [0, 0, 0, 0, 4, 0, 0, 0, 0], [0, 6, 0, 0, 0, 7, 5, 2, 0], [0, 0, 2, 3, 0, 4, 0, 6, 0], [0, 5, 0, 0, 0, 0, 3, 0, 1], [3, 4, 9, 0, 0, 0, 0, 0, 0]]
        print('\n', self.sud)

        self.root = Tk()

        self.frame = Canvas(self.root, width=446, height=446)

        height = 9
        width = 9
        for i in range(height):  # Rows
            for j in range(width):  # Columns
                num = str(self.sud[i][j])
                num = str(num) if num != '0' else ''
                self.frame.create_text((50 * i + 25, 50 * j + 25), anchor='center', text=num, font=('times new roman', '25'))
        self.frame.pack()
        print_button = Button(self.root, text="print", command=self.generate_pdf)
        print_button.pack()

        for i in range(11):
            if i % 3:
                self.frame.create_line(50 * i, 0, 50 * i, 500, fill='grey')
                self.frame.create_line(0, 50 * i, 500, 50 * i, fill='grey')
            else:
                self.frame.create_line(50 * i, 0, 50 * i, 500, fill='black', width=2)
                self.frame.create_line(0, 50 * i, 500, 50 * i, fill='black', width=2)


        self.root.mainloop()

    def generate_pdf(self):
        self.frame.update()
        self.frame.postscript(file="tmp.ps", colormode='color')
        process = subprocess.Popen(["C:\\Users\\tom-v\\Documents\\sudokuRandom_V0.1\\lib\\ps2pdf", "tmp.ps",
                                    "result.pdf"], shell=True)
        process.wait()
        os.remove('tmp.ps')

start = UI()
