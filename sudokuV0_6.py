import os
from tkinter import *
import subprocess
import random as rand
import copy
import math


def quick_solve(string):
    # execute unpack to form a grid in the form of a list
    # execute solve function with the unpacked string
    sudoku = unpack(string)
    solve(sudoku)
    return solved_grid


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
    xb = (x // 3) * 3
    yb = (y // 3) * 3

    for k in range(3):
        for l in range(3):
            if g[yb + k][xb + l] == n:
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
                            # noinspection PyGlobalUndefined
                            global solved_grid
                            solved_grid = copy.deepcopy(grid)
                        else:
                            grid[y][x] = 0
                return


def check_unique(sud):
    # noinspection PyGlobalUndefined
    global solved_grid
    solved_grid = []
    test = copy.deepcopy(sud)

    solve(test)
    solve1 = copy.deepcopy(solved_grid)

    test = copy.deepcopy(sud)
    solve(test, True)
    solve2 = copy.deepcopy(solved_grid)

    if solve1 == solve2:
        return True
    else:
        return False


class UI:
    # main UI element defined as a class to modify geometry and widget easier
    def __init__(self):
        # create empty sudoku
        self.sud = []
        for x in range(9):
            temp = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.sud.append(temp)

        self.numbers = []
        self.difficulty = 60

        # build empty grid
        self.grid = []

        # main window
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
        self.diff = Menu(self.option_menu)
        self.option_menu.add_command(label='Show Solution', command=self.show_solution)
        self.option_menu.add_cascade(label='difficulty', menu=self.diff)

        self.diff.add_command(label='easy', command=lambda: self.set_diff(1))
        self.diff.add_command(label='normal', command=lambda: self.set_diff(2))
        self.diff.add_command(label='hard (might take a while)', command=lambda: self.set_diff(3))

        # main frame where in the sudoku is rendered
        self.frame = Canvas(self.root, width=454, height=454)
        self.frameS = Canvas(self.root, width=455, height=455)

        # main function to display the sudoku onto the frame
        self.display()

        # identifiers to keep track of the selected cell and the types of widgets the Canvas contains
        self.pos_x = 0
        self.pos_y = 0
        self.x = 3
        self.y = 3
        self.selection = []
        self.tags = ''

        # Lists keeping track of the solution and filled in numbers
        self.solved = []
        self.solution = []

        # generate new sudoku button
        generate_new = Button(self.root, text="New Sudoku", command=self.build)
        generate_new.grid(column=3, row=1, columnspan=3)

        # clear grid button
        clear_grid = Button(self.root, text='Clear Grid', command=self.frame_clear)
        clear_grid.grid(column=6, row=1, columnspan=3)

        # function that creates the grid
        self.create_frame()

        # pixel to convert padding from being character based to pixel based
        pixel_virtual = PhotoImage(width=1, height=1)

        # creating and displaying button to help fill in the sudoku for use without keyboard
        for i in range(9):
            self.numbers.append(
                Button(self.root, text=str(i + 1), image=pixel_virtual, height=45, width=45, compound='c',
                       command=lambda j=i: self.insert_num(j + 1)))
            self.numbers[i].grid(column=i, row=2)

        # Button to check the filled in solution
        self.check = Button(self.root, text='CHECK', command=self.check_solution)
        self.check.grid(column=0, row=1, columnspan=3)

        # force focus the frame so keyboard can fill numbers into the grid
        self.frame.focus_force()
        self.frame.config(highlightthickness=0)

        # adding functionality to keyboard shortcuts
        self.frame.bind('<Control-Button-1>', self.get_held_xy)
        self.frame.bind('<Button-1>', self.get_xy)
        self.frame.bind('<B1-Motion>', self.get_held_xy)
        self.frame.bind('<Key>', self.insert_key)
        for i in range(1, 10):
            self.frame.bind(str(i), self.insert_key)
        self.frame.bind('<Delete>', self.clear_num)

        # if the program is run natively a new board will directly be generated
        # without needing to call a separate function in the command window
        # if the program is not run directly other feature may be implemented easier
        if __name__ == '__main__':
            self.root.mainloop()

    # function to set the difficulty still not fully working
    def set_diff(self, diff):
        if diff == 1:
            self.difficulty = 40
        elif diff == 2:
            self.difficulty = 60
        else:
            self.difficulty = 100

    # frame creation
    """offset x and y are used to position the grid onto any size frame"""
    def create_frame(self, offset_x=3, offset_y=3, color=('black', 'grey')):
        for i in range(10):
            if i % 3:
                self.frame.create_line(offset_x + 50 * i, offset_y + 0, offset_x + 50 * i, offset_y + 450,
                                       fill=color[1],
                                       tag='gridlines')
                self.frame.create_line(offset_x + 0, offset_y + 50 * i, offset_x + 450, offset_y + 50 * i,
                                       fill=color[1],
                                       tag='gridlines')
            else:
                self.frame.create_line(offset_x + 50 * i, offset_y + 0, offset_x + 50 * i, offset_y + 450,
                                       fill=color[0],
                                       width=2,
                                       tag='main_gridlines')
                self.frame.create_line(offset_x + 0, offset_y + 50 * i, offset_x + 450, offset_y + 50 * i,
                                       fill=color[0],
                                       width=2,
                                       tag='main_gridlines')
        self.frame.tag_raise('main_gridlines')

    def build(self):
        self.hide_solution()
        print('building')
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
        sudoku = copy.deepcopy(solved_grid)
        self.solved = copy.deepcopy(solved_grid)

        x = rand.randrange(9)
        y = rand.randrange(9)
        b = sudoku[x][y]
        c = sudoku[8 - x][8 - y]
        sudoku[x][y] = 0
        sudoku[8 - x][8 - y] = 0
        tester = copy.deepcopy(sudoku)

        # check for uniqueness and store the boolean in the unique variable for possible exception
        unique = check_unique(tester)

        while tries < self.difficulty and empty < 54:
            while unique == 1 and tries < self.difficulty:
                self.root.update()
                x = rand.randrange(9)
                y = rand.randrange(9)
                b = sudoku[x][y]
                c = sudoku[8 - x][8 - y]
                if b != 0:
                    sudoku[x][y] = 0
                    sudoku[8 - x][8 - y] = 0
                    tester = copy.deepcopy(sudoku)
                    unique = check_unique(tester)
                    # if __name__ == '__main__':
                    # print(empty, ': ', sudoku)
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

    def frame_clear(self):
        self.frame.delete('mark', 'insert', 'highlight')
        self.frame.config(bg='WHITE')

    def display(self, solution=False):
        def fill_grid(offset_x=3, offset_y=3):
            for i in range(height):  # Rows
                for j in range(width):  # Columns
                    num = str(numbers[j][i])
                    num = str(num) if num != '0' else ''
                    self.frame.create_text((offset_x + 50 * i + 25, offset_y + 50 * j + 25), anchor='center', text=num,
                                           font=('times new roman', '25'), tag='text')
            self.frame.grid(column=0, row=0, padx=5, pady=5, columnspan=9)

        height = 9
        width = 9
        if not solution:
            self.frame_clear()
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
        # noinspection PyGlobalUndefined
        global solved_grid
        copy1 = copy.deepcopy(self.sud)
        solve(copy1)
        self.solution = solved_grid
        self.frame.configure(width=955)
        self.create_frame(500)
        self.option_menu.entryconfig(1, label='Hide Solution', command=self.hide_solution)
        self.display(True)

    def hide_solution(self):
        self.frame.configure(width=455)
        self.option_menu.entryconfig(1, label='Show Solution', command=self.show_solution)

    def get_xy(self, event, clear=True):
        self.frame.config(bg='White')
        self.x = 3 + int(50 * math.floor(event.x / 50))
        self.y = 3 + int(50 * math.floor(event.y / 50))
        # print(event.x, self.x, event.y, self.y)
        if clear:
            self.selection = []
        selected = (self.x, self.y)
        if selected not in self.selection:
            self.selection.append(selected)

        self.change_color(clear)

    def get_held_xy(self, event):
        self.get_xy(event, False)

    def change_color(self, clear=True):
        if clear:
            self.frame.delete('highlight')

        self.frame.create_rectangle(self.x + 1, self.y + 1, self.x + 50, self.y + 50, outline='',
                                    fill='#f5c0bc', tag='highlight')
        self.frame.tag_lower('highlight')

    def insert_key(self, event):
        # print(event)
        direction = ['Up', 'Down', 'Right', 'Left']
        if event.keysym.isdigit():
            self.insert_num(int(event.keysym))
        elif 49 <= event.keycode <= 57:
            self.insert_key_shifted(event)
        elif event.keysym in direction:
            if str(event.keysym) == direction[0] and self.y > 3:
                self.y -= 50
            elif str(event.keysym) == direction[1] and self.y < 403:
                self.y += 50
            elif str(event.keysym) == direction[2] and self.x < 403:
                self.x += 50
            elif str(event.keysym) == direction[3] and self.x > 3:
                self.x -= 50
            selected = (self.x, self.y)
            if selected not in self.selection:
                self.selection.append(selected)

            self.change_color()

    def insert_num(self, number):
        for self.x, self.y in self.selection:
            self.clear_num()
            self.frame.create_text((self.x + 25, self.y + 25),
                                   anchor='center',
                                   text=number,
                                   font=('times new roman', '25'),
                                   fill='blue',
                                   tags=(self.tags, 'insert')
                                   )

            self.sud[self.pos_y][self.pos_x] = number

    def insert_key_shifted(self, event):
        for self.x, self.y in self.selection:
            self.pos_x = math.floor(self.x / 50)
            self.pos_y = math.floor(self.y / 50)
            self.tags = 'id-%s%s' % (self.pos_x, self.pos_y)

            if 49 <= event.keycode <= 57 and self.sud[self.pos_y][self.pos_x] == 0:
                number = event.keycode - 48
                if self.frame.find_withtag(f'{self.tags}&&shifted_{number}'):
                    self.frame.delete(f'{self.tags}&&shifted_{number}')

                    positions = []
                    for i in range(9):
                        pos = (self.x + 10 * (i % 4), self.y + 10 * int(i / 4))
                        positions.append(pos)
                    for j in self.frame.find_withtag(self.tags):
                        pos = positions.pop(0)
                        self.frame.move(j, pos[0] - self.frame.coords(j)[0] + 10, pos[1] - self.frame.coords(j)[1])

                else:
                    cell = self.frame.find_withtag(self.tags)
                    offset_x = 10 * (len(cell) % 4) + 10
                    offset_y = 10 * int(len(cell) / 4)
                    self.frame.create_text((self.x + offset_x, self.y + offset_y),
                                           anchor='ne',
                                           text=number,
                                           font=('times new roman', '10'),
                                           fill='blue',
                                           tags=(self.tags, f'shifted_{number}', 'mark')
                                           )

    def clear_num(self, *_event):

        self.pos_x = math.floor(self.x / 50)
        self.pos_y = math.floor(self.y / 50)
        self.tags = 'id-%s%s' % (self.pos_x, self.pos_y)

        self.frame.delete(self.tags)
        self.sud[self.pos_y][self.pos_x] = 0

    def check_solution(self):
        if any(0 in i for i in self.sud):
            print('INCOMPLETE...')
            for i, k in enumerate(self.sud):
                for j, l in enumerate(k):
                    if l == 0:
                        self.frame.create_rectangle(j * 50 + 4, i * 50 + 4, j * 50 + 53, i * 50 + 53,
                                                    outline='',
                                                    fill='#99d3ff',
                                                    tag='highlight'
                                                    )
                        self.frame.tag_lower('highlight')
        elif self.sud == self.solved:
            self.frame.delete('highlight')
            print('CORRECT')
            self.frame.config(bg='#c4ffbd')
        else:
            print('INCORRECT, TRY AGAIN...')
            self.frame.config(bg='#f5c0bc')


if __name__ == '__main__':
    start = UI()
