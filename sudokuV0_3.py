import os
from tkinter import *
import subprocess
import random as rand
import copy


def unpack(string):
    unpacked = []
    if len(string) != 81:
        raise Exception('Not a valid sudoku must be 9x9 = 81 in lenght')
    pack1 = list(string)
    for x in range(9):
        temp = list()
        for y in pack1[x * 9:(x + 1) * 9]:
            temp.append(int(y))
        unpacked.append(temp)
    return unpacked

def repack(grid):
    repacked = ''
    for x in grid:
        for y in x:
            repacked += str(y)
    return repacked


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


def solve(grid, reverse=False):
    order = list(range(9, 0, -1)) if reverse else list(range(1, 10))
    for x in range(9):
        for y in range(9):
            if grid[y][x] == 0:
                for n in order:
                    if check(x, y, n, grid):
                        grid[y][x] = n
                        solve(grid, reverse)
                        if not any(0 in i for i in grid):
                            global solvedgrid
                            solvedgrid = copy.deepcopy(grid)
                        else:
                            grid[y][x] = 0
                return


def check_unique(sud):
    global solvedgrid
    solvedgrid = []
    test = copy.deepcopy(sud)

    solve(test)
    solve1 = copy.deepcopy(solvedgrid)
    print(solve1)

    test = copy.deepcopy(sud)
    solve(test, True)
    solve2 = copy.deepcopy(solvedgrid)
    print(solve2)

    if solve1 == solve2:
        return True
    else:
        return False


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


class UI:
    def __init__(self):
        # create empty sudoku
        self.sud = []
        for x in range(9):
            temp = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.sud.append(temp)

        # self.sud =  [[2, 9, 7, 3, 6, 8, 1, 4, 5], [8, 4, 5, 1, 9, 7, 3, 2, 6], [6, 3, 1, 4, 5, 2, 7, 8, 9], [1, 8, 9, 5, 4, 6, 2, 3, 7], [5, 2, 6, 7, 3, 1, 4, 9, 8], [3, 7, 4, 2, 8, 9, 6, 5, 1], [7, 1, 8, 9, 2, 4, 5, 6, 3], [4, 6, 3, 8, 7, 5, 9, 1, 2], [9, 5, 2, 6, 1, 3, 8, 7, 4]]
        self.root = Tk()

        # create menus
        main_menu = Menu(self.root)
        self.root.config(menu=main_menu)

        self.file_menu = Menu(main_menu)
        self.option_menu = Menu(main_menu)
        main_menu.add_cascade(label='File', menu=self.file_menu)
        main_menu.add_cascade(label='Options', menu=self.option_menu)

        # add file menu commands
        self.file_menu.add_command(label='print to PDF', command=self.generate_pdf)
        self.file_menu.add_command(label='Save as...', command=self.save)
        self.file_menu.add_command(label='Exit', command=exit)

        # add options under option menu
        self.option_menu.add_command(label='Show Solution', command=self.show_solution)

        self.frame = Canvas(self.root, width=455, height=455)
        self.frameS = Canvas(self.root, width=455, height=455)
        self.display()

        # generate new sudoku
        generate_new = Button(self.root, text="New Sudoku", command=self.build)
        generate_new.grid(column=0, row=1)

        self.create_frame()
        self.root.mainloop()

    def create_frame(self, offset_x=3, offset_y=3):
        for i in range(10):
            if i % 3:
                self.frame.create_line(offset_x + 50 * i, offset_y + 0, offset_x + 50 * i, offset_y + 450, fill='grey', tag='gridlines')
                self.frame.create_line(offset_x + 0, offset_y + 50 * i, offset_x + 450, offset_y + 50 * i, fill='grey', tag='gridlines')
            else:
                self.frame.create_line(offset_x + 50 * i, offset_y + 0, offset_x + 50 * i, offset_y + 450, fill='black', width=2, tag='gridlines')
                self.frame.create_line(offset_x + 0, offset_y + 50 * i, offset_x + 450, offset_y + 50 * i, fill='black', width=2, tag='gridlines')

    def build(self):
        self.hide_solution()
        print('building')
        # build empty grid
        self.grid = []
        for x in range(9):
            temp = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.grid.append(temp)

        # build random diagonal
        for x in [0, 3, 6]:
            a, b, c = rand.sample(range(1, 10), 3)
            self.grid[x][x] = a
            self.grid[x + 1][x + 1] = b
            self.grid[x + 2][x + 2] = c

        empty = 0
        tries = 0

        print(self.grid)
        solve(self.grid)
        sudoku = copy.deepcopy(solvedgrid)

        x = rand.randrange(9)
        y = rand.randrange(9)
        b = sudoku[x][y]
        c = sudoku[8 - x][8 - y]
        sudoku[x][y] = 0
        sudoku[8 - x][8 - y] = 0
        tester = copy.deepcopy(sudoku)

        unique = check_unique(tester)

        while tries < 60 and empty < 50:
            while unique == 1 and tries < 60:
                x = rand.randrange(9)
                y = rand.randrange(9)
                b = sudoku[x][y]
                c = sudoku[8 - x][8 - y]
                if b != 0:
                    sudoku[x][y] = 0
                    sudoku[8 - x][8 - y] = 0
                    tester = copy.deepcopy(sudoku)
                    unique = check_unique(tester)
                    if __name__ == '__main__':
                        print(empty, ': ', sudoku)
                tries += 1
                if tries % 10 == 1:
                    print('=', end='')

            sudoku[8 - x][8 - y] = c
            sudoku[x][y] = b
            tester = copy.deepcopy(sudoku)
            unique = check_unique(tester)

            empty = 0
            for s in sudoku:
                empty += s.count(0)

        self.sud = sudoku
        self.display()

    def display(self, solution=False):
        def fill_grid(offset_x=3, offset_y=3):
            for i in range(height):  # Rows
                for j in range(width):  # Columns
                    num = str(numbers[j][i])
                    num = str(num) if num != '0' else ''
                    self.frame.create_text((offset_x + 50 * i + 25, offset_y + 50 * j + 25), anchor='center', text=num,
                                           font=('times new roman', '25'), tag='text')
            self.frame.grid(column=0, row=0, padx=5, pady=5)

        height = 9
        width = 9
        if not solution:
            self.frame.delete('text')
            numbers = self.sud
            fill_grid()
        else:
            self.frame.delete('textS')
            numbers = self.solution
            fill_grid(500)

    def save(self):
        save_file = repack(self.sud)
        save_data = open('.\\saves\\sudoku.txt', 'w+')
        save_data_str = str(save_data.read())
        save_data_str += f'\n{save_file}'
        save_data.write(save_data_str)
        save_data.close()

    def generate_pdf(self):
        self.hide_solution()
        self.frame.update()
        self.frame.postscript(file="tmp.ps", colormode='color')
        process = subprocess.Popen([".\\lib\\ps2pdf", "tmp.ps", ".\\saves\\sudoku.pdf"], shell=True)
        process.wait()
        os.remove('tmp.ps')
        subprocess.Popen('.\\saves\\sudoku.pdf', shell=True)

    def show_solution(self):
        global solvedgrid
        copy1 = copy.deepcopy(self.sud)
        solve(copy1)
        self.solution = solvedgrid
        self.frame.configure(width=955)
        self.create_frame(500)
        self.option_menu.entryconfig(1, label='Hide Solution', command=self.hide_solution)
        self.display(True)

    def hide_solution(self):
        self.frame.configure(width=455)
        self.option_menu.entryconfig(1, label='Show Solution', command=self.show_solution)



if __name__ == '__main__':
    start = UI()
