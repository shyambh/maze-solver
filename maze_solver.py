from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.window = Tk()
        self.window.title("Root Window Widget")
        self.window.protocol("WM_DELETE_WINDOW", self.close) 

        self.canvas = Canvas(self.window, width = self.width, height = self.height, background="white")
        self.canvas.pack(expand=1)

    def redraw(self):
        self.window.update_idletasks()
        self.window.update()
   
    
    def wait_for_close(self):
        self.window_is_running = True

        while(self.window_is_running):
            self.redraw() 

    def close(self):
        self.window_is_running = False
        self.window.destroy()

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill = fill_color, width = 4)
        canvas.pack()

class Cell:
    def __init__(self, x1, x2, y1, y2, window=None, has_left_wall = True, has_right_wall = True, has_top_wall = True, has_bottom_wall = True, visited=False):

        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        
        self.__x1_top_left = x1
        self.__y1_top_left = y1
        self.__x2_bottom_right = x2
        self.__y2_bottom_right = y2

        self.__win = window 
        self.visited = visited

    def draw(self):

        top_left_point = Point(self.__x1_top_left, self.__y1_top_left)
        bottom_left_point = Point(self.__x1_top_left, self.__y2_bottom_right)
        top_right_point = Point(self.__x2_bottom_right, self.__y1_top_left)
        bottom_right_point = Point(self.__x2_bottom_right, self.__y2_bottom_right)

        if(self.__win):
            left_wall = Line(top_left_point, bottom_left_point)
            right_wall = Line(top_right_point, bottom_right_point)
            top_wall = Line(top_left_point, top_right_point)
            bottom_wall = Line(bottom_left_point, bottom_right_point)

            if self.has_left_wall:
                self.__win.draw_line(left_wall, "black")
            else:
                self.__win.draw_line(left_wall, "white")

            if self.has_right_wall:
                self.__win.draw_line(right_wall, "black")
            else:
                self.__win.draw_line(right_wall, "white")

            if self.has_top_wall:
                self.__win.draw_line(top_wall, "black")
            else:
                self.__win.draw_line(top_wall, "white")

            if self.has_bottom_wall:
                self.__win.draw_line(bottom_wall, "black")
            else:
                self.__win.draw_line(bottom_wall, "white")
    
    def draw_move(self, to_cell, undo=False):
        self_center_x = (self.__x1_top_left + self.__x2_bottom_right) / 2
        self_center_y = (self.__y1_top_left + self.__y2_bottom_right) / 2
        self_center_point = Point(self_center_x, self_center_y)

        dest_cell_center_x = (to_cell.__x1_top_left + to_cell.__x2_bottom_right) / 2
        dest_cell_center_y = (to_cell.__y1_top_left + to_cell.__y2_bottom_right) / 2
        dest_cell_center_point = Point(dest_cell_center_x, dest_cell_center_y)

        color = "green" if not undo else "red"

        line = Line(self_center_point, dest_cell_center_point)

        if undo:
            time.sleep(0.1)

        line.draw(self.__win.canvas, color)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, window=None, seed=None):

        if seed is not None:
            random.seed(seed)

        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.__win = window

        self.__create_cells()

    def __create_cells(self):
        self.__cells = []
        first_cell_x = self.x1
        first_cell_y = self.y1

        for row in range(0, self.num_rows):
            for col in range(0, self.num_cols):
                top_left_x = first_cell_x + (col * self.cell_size_x)
                top_left_y = first_cell_y + (row * self.cell_size_y)

                bottom_right_x = top_left_x + self.cell_size_x
                bottom_right_y = top_left_y + self.cell_size_y

                if col == 0:
                    self.__cells.append([Cell(top_left_x, bottom_right_x, top_left_y, bottom_right_y, self.__win)])
                else:
                    self.__cells[row].append(Cell(top_left_x, bottom_right_x, top_left_y, bottom_right_y, self.__win))

        for i, row in enumerate(self.__cells):
            for j, col in enumerate(self.__cells[i]):
                self.__draw_cell(i, j)

        self.__break_entrance_and_exit()
        self.__break_walls_r(0,0)
        self.__reset_cells_visited()
        
    def __draw_cell(self, i , j):
        self.__cells[i][j].draw()
        self.__animate()
        
    def get_cells(self):
        return self.__cells

    def __animate(self):
        if(self.__win):
            self.__win.redraw()
            
            time.sleep(0.5 / (self.num_cols * self.num_rows))

    def __break_entrance_and_exit(self):

        cells = self.get_cells()

        self.__cells[0][0].has_top_wall = False
        self.__cells[-1][-1].has_bottom_wall = False

        self.__draw_cell(0,0)
        self.__draw_cell(-1,-1)

    def __break_walls_r(self,i,j):

        # Marking the current cell as visited
        self.__cells[i][j].visited = True

        while True:
            row_col_to_visit = []

            # Skip, if a cell is on the border
            # is_at_edge = i == 0 or i == self.num_rows - 1 or j == 0 or j == self.num_cols - 1 

            is_top_row = i == 0 
            is_bottom_row = i == self.num_rows - 1

            is_left_col = j == 0 
            is_right_col = j == self.num_cols - 1

            if(not is_top_row):
                top_adjacent_cell = self.__cells[i-1][j]
                if not top_adjacent_cell.visited:
                    row_col_to_visit.append({"top" : (i-1, j)})
            
            if(not is_bottom_row):
                bottom_adjacent_cell = self.__cells[i+1][j]
                if not bottom_adjacent_cell.visited:
                    row_col_to_visit.append({"bottom" : (i+1, j)})
            
            if(not is_left_col):
                left_adjacent_cell = self.__cells[i][j-1]
                if not left_adjacent_cell.visited:
                    row_col_to_visit.append({"left" : (i, j-1)})
            if(not is_right_col):
                right_adjacent_cell = self.__cells[i][j+1]
                if not right_adjacent_cell.visited:
                    row_col_to_visit.append({"right" : (i, j+1)})

            if len(row_col_to_visit) == 0:
                # if there are no directions left to visit then draw the current cell
                self.__cells[i][j].draw()
                return

            # Pick a random adjacent cell to move to
            random_cell = random.choice(row_col_to_visit)
            random_direction = list(random_cell.keys())[0]
            random_cell_i = list(random_cell.values())[0][0] 
            random_cell_j = list(random_cell.values())[0][1] 

            if random_direction == "top":
                self.__cells[i][j].has_top_wall = False
                self.__cells[random_cell_i][random_cell_j].has_bottom_wall = False
                
            elif random_direction == "bottom":
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[random_cell_i][random_cell_j].has_top_wall = False

            elif random_direction == "left":
                self.__cells[i][j].has_left_wall = False
                self.__cells[random_cell_i][random_cell_j].has_right_wall = False

            elif random_direction == "right":
                self.__cells[i][j].has_right_wall = False
                self.__cells[random_cell_i][random_cell_j].has_left_wall = False

            # Move to the destination cell
            self.__break_walls_r(random_cell_i, random_cell_j)

    def __reset_cells_visited(self):
        for row in self.get_cells():
            for col in row:
                col.visited = False

    def __solve_r(self, i , j):

        self.__animate()
        cells = self.get_cells()

        # Marking current cell as visited
        cells[i][j].visited = True

        # Return True if at the end cell (destination)
        if cells[i][j] == cells[-1][-1]:
            return True

        # Edge cells
        is_top_row = i == 0 
        is_bottom_row = i == self.num_rows - 1

        is_left_col = j == 0 
        is_right_col = j == self.num_cols - 1

        row_col_to_visit = []

        # Add all possible directions and corresponding cells to the list
        if(not is_top_row):
            top_adjacent_cell = self.__cells[i-1][j]
            if not top_adjacent_cell.visited:
                row_col_to_visit.append({"top" : (i-1, j)})
            
        if(not is_bottom_row):
            bottom_adjacent_cell = self.__cells[i+1][j]
            if not bottom_adjacent_cell.visited:
                row_col_to_visit.append({"bottom" : (i+1, j)})
        
        if(not is_left_col):
            left_adjacent_cell = self.__cells[i][j-1]
            if not left_adjacent_cell.visited:
                row_col_to_visit.append({"left" : (i, j-1)})
        if(not is_right_col):
            right_adjacent_cell = self.__cells[i][j+1]
            if not right_adjacent_cell.visited:
                row_col_to_visit.append({"right" : (i, j+1)})

        for idx, cell_with_direction in enumerate(row_col_to_visit):
            wall_exists = False

            cell_direction = list(cell_with_direction.keys())[0]
            destination_cell_i = list(row_col_to_visit[idx].values())[0][0]
            destination_cell_j = list(row_col_to_visit[idx].values())[0][1]
            destination_cell = cells[destination_cell_i][destination_cell_j]
            
            if cell_direction == 'top':
                wall_exists = destination_cell.has_bottom_wall
            elif cell_direction == 'bottom':
                wall_exists = destination_cell.has_top_wall
            elif cell_direction == 'left':
                wall_exists = destination_cell.has_right_wall
            elif cell_direction == 'right':
                wall_exists = destination_cell.has_left_wall

            if not wall_exists:
                cells[i][j].draw_move(destination_cell)
                if self.__solve_r(destination_cell_i, destination_cell_j):
                    return True
                else:
                    cells[i][j].draw_move(destination_cell, undo = True)


    def solve(self):
        self.__solve_r(i = 0 , j = 0)

def main():
    win = Window(2048, 1200)

    # cell_first = Cell(100,200, 300, 400, win)
    # cell_second = Cell(300,400, 300, 400, win)

    # cell_first.draw()
    # cell_second.draw()

    # cell_first.draw_move(cell_second, True)

    maze1 = Maze(x1=100, y1=200, num_rows=3, num_cols=3, cell_size_x=50, cell_size_y=50, window=win)

    maze2 = Maze(x1=400, y1=200, num_rows=7, num_cols=7, cell_size_x=50, cell_size_y=50, window=win)

    maze3 = Maze(x1=900, y1=200, num_rows=12, num_cols=12, cell_size_x=30, cell_size_y=30, window=win)

    maze1.solve()
    maze2.solve()
    maze3.solve()

    win.wait_for_close()

if __name__ == "__main__":
    main()