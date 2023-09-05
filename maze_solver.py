from tkinter import Tk, BOTH, Canvas
import time

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.window = Tk()
        self.window.title("Root Window Widget")
        self.window.protocol("WM_DELETE_WINDOW", self.close) 

        self.canvas = Canvas(self.window, width = self.width, height = self.height)
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
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill = fill_color, width = 2)
        canvas.pack()

class Cell:
    def __init__(self, x1, x2, y1, y2, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        
        self.__x1_top_left = x1
        self.__y1_top_left = y1
        self.__x2_bottom_right = x2
        self.__y2_bottom_right = y2

        self.__win = window 

    def draw(self):

        top_left_point = Point(self.__x1_top_left, self.__y1_top_left)
        bottom_left_point = Point(self.__x1_top_left, self.__y2_bottom_right)
        top_right_point = Point(self.__x2_bottom_right, self.__y1_top_left)
        bottom_right_point = Point(self.__x2_bottom_right, self.__y2_bottom_right)

        if(self.__win):
            if self.has_left_wall:
                left_wall = Line(top_left_point, bottom_left_point)
                self.__win.draw_line(left_wall, "red")

            if self.has_right_wall:
                right_wall = Line(top_right_point, bottom_right_point)
                self.__win.draw_line(right_wall, "red")

            if self.has_top_wall:
                top_wall = Line(top_left_point, top_right_point)
                self.__win.draw_line(top_wall, "red")

            if self.has_bottom_wall:
                bottom_wall = Line(bottom_left_point, bottom_right_point)
                self.__win.draw_line(bottom_wall, "red")
    
    def draw_move(self, to_cell, undo=False):
        self_center_x = (self.__x1_top_left + self.__x2_bottom_right) / 2
        self_center_y = (self.__y1_top_left + self.__y2_bottom_right) / 2
        self_center_point = Point(self_center_x, self_center_y)

        dest_cell_center_x = (to_cell.__x1_top_left + to_cell.__x2_bottom_right) / 2
        dest_cell_center_y = (to_cell.__y1_top_left + to_cell.__y2_bottom_right) / 2
        dest_cell_center_point = Point(dest_cell_center_x, dest_cell_center_y)

        color = "red" if not undo else "gray"

        line = Line(self_center_point, dest_cell_center_point)
        line.draw(self.__win.canvas, color)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, window=None):
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
        
        for col in self.__cells:
            for col_cell in col:
                col_cell.draw()
                self.__animate()


    def get_cells(self):
        return self.__cells

    
    def __animate(self):
        if(self.__win):
            self.__win.redraw()
            time.sleep(0.05)
        

def main():
    win = Window(800, 600)

    # cell_first = Cell(100,200, 300, 400, win)
    # cell_second = Cell(300,400, 300, 400, win)

    # cell_first.draw()
    # cell_second.draw()

    # cell_first.draw_move(cell_second, True)

    maze = Maze(x1=100, y1=200, num_rows=10, num_cols=10, cell_size_x=50, cell_size_y=30, window=win)

    win.wait_for_close()

if __name__ == "__main__":
    main()