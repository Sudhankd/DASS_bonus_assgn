import tkinter as tk

class Line:
    def __init__(self, canvas):
        self.canvas = canvas
        self.object = None

    def start_draw(self, event):
        self.object = self.canvas.create_line(event.x, event.y, event.x, event.y, fill="black", width=2)

    def draw(self, event):
        self.canvas.coords(self.object, (self.canvas.coords(self.object)[0], self.canvas.coords(self.object)[1], event.x, event.y))

    def end_draw(self, event):
        pass

class Rectangle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.object = None

    def start_draw(self, event):
        self.object = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="black")

    def draw(self, event):
        self.canvas.coords(self.object, (self.canvas.coords(self.object)[0], self.canvas.coords(self.object)[1], event.x, event.y))

    def end_draw(self, event):
        pass

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()

        self.line_button = tk.Button(master, text="Line", command=self.set_line_mode)
        self.line_button.pack(side="left")

        self.rect_button = tk.Button(master, text="Rectangle", command=self.set_rect_mode)
        self.rect_button.pack(side="left")

        self.drawing_tool = None

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

    def set_line_mode(self):
        self.drawing_tool = Line(self.canvas)

    def set_rect_mode(self):
        self.drawing_tool = Rectangle(self.canvas)

    def start_draw(self, event):
        if self.drawing_tool:
            self.drawing_tool.start_draw(event)

    def draw(self, event):
        if self.drawing_tool:
            self.drawing_tool.draw(event)

    def end_draw(self, event):
        if self.drawing_tool:
            self.drawing_tool.end_draw(event)

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()







# import tkinter as tk

# class MyObject:
#     def __init__(self, x1, y1, x2, y2):
#         self.x1 = x1
#         self.y1 = y1
#         self.x2 = x2
#         self.y2 = y2

# class DrawingApp:
#     def __init__(self, master):
#         self.master = master
#         self.canvas = tk.Canvas(master, width=400, height=400)
#         self.canvas.pack()

#         self.line_button = tk.Button(master, text="Line", command=self.set_line_mode)
#         self.line_button.pack(side="left")

#         self.rect_button = tk.Button(master, text="Rectangle", command=self.set_rect_mode)
#         self.rect_button.pack(side="left")

#         self.object = None
#         self.draw_mode = False

#         self.canvas.bind("<Button-1>", self.start_draw)
#         self.canvas.bind("<B1-Motion>", self.draw)
#         self.canvas.bind("<ButtonRelease-1>", self.end_draw)

#     def set_line_mode(self):
#         self.draw_mode = "line"

#     def set_rect_mode(self):
#         self.draw_mode = "rect"

#     def start_draw(self, event):
#         if self.draw_mode:
#             if self.draw_mode == "line":
#                 self.object = MyObject(event.x, event.y, event.x, event.y)
#             elif self.draw_mode == "rect":
#                 self.object = MyObject(event.x, event.y, event.x, event.y)
#                 self.rect_id = self.canvas.create_rectangle(self.object.x1, self.object.y1, self.object.x2, self.object.y2, outline="black")

#     def draw(self, event):
#         if self.draw_mode and self.object:
#             self.object.x2 = event.x
#             self.object.y2 = event.y
#             if self.draw_mode == "line":
#                 self.canvas.delete("current_line")
#                 self.canvas.create_line(self.object.x1, self.object.y1, self.object.x2, self.object.y2, fill="black", width=2, tags="current_line")
#             elif self.draw_mode == "rect":
#                 self.canvas.coords(self.rect_id, self.object.x1, self.object.y1, self.object.x2, self.object.y2)

#     def end_draw(self, event):
#         if self.draw_mode and self.object:
#             self.object.x2 = event.x
#             self.object.y2 = event.y
#             if self.draw_mode == "line":
#                 self.canvas.delete("current_line")
#                 self.canvas.create_line(self.object.x1, self.object.y1, self.object.x2, self.object.y2, fill="black", width=2)
#             elif self.draw_mode == "rect":
#                 pass
#             self.draw_mode = False
#             self.object = None

# def main():
#     root = tk.Tk()
#     app = DrawingApp(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()











