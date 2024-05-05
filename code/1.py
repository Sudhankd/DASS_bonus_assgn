import tkinter as tk

class MyObject:
    def _init_(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class DrawingApp:
    def _init_(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()

        self.line_button = tk.Button(master, text="Line", command=self.set_line_mode)
        self.line_button.pack()

        self.object = None
        self.draw_mode = False

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

    def set_line_mode(self):
        self.draw_mode = True

    def start_draw(self, event):
        if self.draw_mode:
            self.object = MyObject(event.x, event.y, event.x, event.y)

    def draw(self, event):
        if self.draw_mode and self.object:
            self.object.x2 = event.x
            self.object.y2 = event.y
            self.canvas.delete("current_line")
            self.canvas.create_line(self.object.x1, self.object.y1, self.object.x2, self.object.y2, fill="black", width=2, tags="current_line")

    def end_draw(self, event):
        if self.draw_mode and self.object:
            self.object.x2 = event.x
            self.object.y2 = event.y
            self.canvas.delete("current_line")
            self.canvas.create_line(self.object.x1, self.object.y1, self.object.x2, self.object.y2, fill="black", width=2)
            self.draw_mode = False
            self.object = None

def main():
    root = tk.Tk()
    # root.geometry("800x500")
    # root.title("Drawing Editor")
    app = DrawingApp(root)
    root.mainloop()

if "__name___ " == "_main_":
    main()














# import tkinter as tk



# class Object():
#     def _init_(self, id, color, object_type, x1, x2, y1, y2):
#         self.id = id
#         self.color = color
#         self.object_type = object_type
#         self.x1 = x1
#         self.x2 = x2
#         self.y1 = y1
#         self.y2 = y2

#         self.line_button = tk.Button(master, text="Line", command=self.set_line_mode)
#         self.line_button.pack()

#         self.canvas.bind("<Button-1>", self.start_draw)
#         self.canvas.bind("<B1-Motion>", self.draw)
#         self.canvas.bind("<ButtonRelease-1>", self.end_draw)

#         self.draw_mode = False

#     # def Highlight():
        

# class DrawingApp():



# def main():
    # root = tk.Tk()


    # root.geometry("800x500")
    # root.title("Drawing Editor")
    # editor = Object(root)
    # root.mainloop()


# if _name_ == "_main_":
#     main()