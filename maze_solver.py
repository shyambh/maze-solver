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

def main():
    win = Window(800, 600)

    point1 = Point(100,100)
    point2 = Point(-20,-20)
    line = Line(point1, point2)
    win.draw_line(line, "red")
    win.wait_for_close()

main()