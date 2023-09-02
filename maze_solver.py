from tkinter import Tk, BOTH, Canvas

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
    def __init__(self, x1, x2, y1, y2, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        self.__win = window 

    def draw(self):
        top_left_point = Point(self.__x1, self.__y1)
        bottom_left_point = Point(self.__x1, self.__y2)
        top_right_point = Point(self.__x2, self.__y1)
        bottom_right_point = Point(self.__x2, self.__y2)

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
    
            


def main():
    win = Window(800, 600)

    cell = Cell(100,200, 300, 400, win)
    cell.draw()

    win.wait_for_close()

main()