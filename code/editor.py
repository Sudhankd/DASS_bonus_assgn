import tkinter as tk

class Line:
    def __init__(self, canvas):
        self.canvas = canvas
        self.drawing_object = None
        self.draw_mode = True

    def start_draw(self, event):
        if self.draw_mode:
            self.drawing_object = self.canvas.create_line(event.x, event.y, event.x, event.y, fill="black", width=2)
        
        return self.drawing_object

    def draw(self, event):
        if self.draw_mode:
            self.canvas.coords(self.drawing_object, (self.canvas.coords(self.drawing_object)[0], self.canvas.coords(self.drawing_object)[1], event.x, event.y))

    def end_draw(self, event):
        self.draw_mode = False
        pass
    

class Rectangle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.drawing_object = None
        self.draw_mode = True

    def start_draw(self, event):
        if self.draw_mode:
            self.drawing_object = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="black", width=2)
        
        return self.drawing_object

    def draw(self, event):
        if self.draw_mode:
            self.canvas.coords(self.drawing_object, (self.canvas.coords(self.drawing_object)[0], self.canvas.coords(self.drawing_object)[1], event.x, event.y))

    def end_draw(self, event):
        self.draw_mode = False
        pass

    


class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()

        self.object_list = []
        
        
        
        self.line_button = tk.Button(master, text="Line", command=self.set_line_mode)
        self.line_button.pack(side="left")

        self.rect_button = tk.Button(master, text="Rectangle", command=self.set_rect_mode)
        self.rect_button.pack(side="left")


        self.drawing_tool = None

        self.previous_object = None
        self.selected_object = None


        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        # self.canvas.bind("<Button-1>", self.highlight_on_click)

        # if self.canvas.drawing_tool:
        #     self.canvas.tag_bind(self.drawing_tool, "<Button-1>", self.highlight_on_click)  # Highlight when clicked
        #     self.canvas.tag_bind(self.drawing_tool, "<Leave>", self.remove_highlight)       # Remove highlight when mouse leaves rectangle


    def set_line_mode(self):
        self.drawing_tool = Line(self.canvas)

    def set_rect_mode(self):
        self.drawing_tool = Rectangle(self.canvas)

    def start_draw(self, event):
        if self.drawing_tool:
            object_drawn = self.drawing_tool.start_draw(event)
            self.object_list.append(object_drawn)
        else:
            print("hi")
            self.highlight_on_click(event)

    def draw(self, event):
        if self.drawing_tool:
            self.drawing_tool.draw(event)

    def end_draw(self, event):
        if self.drawing_tool:
            self.drawing_tool.end_draw(event)
            self.drawing_tool = None

    
    def highlight_on_click(self, event):
        # nearest_object = self.canvas.find_closest(event.x, event.y)
        # if self.selected_object:
        #     self.canvas.itemconfig(self.selected_object, width=2)
        
        # self.selected_object = nearest_object
        # self.canvas.itemconfig(self.selected_object, width=4)  # Change fill color to yellow when clicked

        if self.selected_object:
            self.canvas.itemconfig(self.selected_object, width=2)
        
        
        for obj in self.object_list:
        # Get the bounding box of the object
            bbox = self.canvas.bbox(obj)
        
        # Check if the clicked coordinates are within the bounding box
            if bbox[0] <= event.x <= bbox[2] and bbox[1] <= event.y <= bbox[3]:
                print("Object exists at this location.")
                self.selected_object = obj
                self.canvas.itemconfig(self.selected_object, width=4)  # Change fill color to yellow when clicked
                return
    # If no object was found at the clicked coordinates
        
        print("No object exists at this location.")

    def remove_highlight(self, event):
        self.canvas.itemconfig(self.drawing_object, fill="blue")    # Change fill color back to blue when not clicked


        
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

#         self.drawing_object = None
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
#                 self.drawing_object = MyObject(event.x, event.y, event.x, event.y)
#             elif self.draw_mode == "rect":
#                 self.drawing_object = MyObject(event.x, event.y, event.x, event.y)
#                 self.rect_id = self.canvas.create_rectangle(self.drawing_object.x1, self.drawing_object.y1, self.drawing_object.x2, self.drawing_object.y2, outline="black")

#     def draw(self, event):
#         if self.draw_mode and self.drawing_object:
#             self.drawing_object.x2 = event.x
#             self.drawing_object.y2 = event.y
#             if self.draw_mode == "line":
#                 self.canvas.delete("current_line")
#                 self.canvas.create_line(self.drawing_object.x1, self.drawing_object.y1, self.drawing_object.x2, self.drawing_object.y2, fill="black", width=2, tags="current_line")
#             elif self.draw_mode == "rect":
#                 self.canvas.coords(self.rect_id, self.drawing_object.x1, self.drawing_object.y1, self.drawing_object.x2, self.drawing_object.y2)

#     def end_draw(self, event):
#         if self.draw_mode and self.drawing_object:
#             self.drawing_object.x2 = event.x
#             self.drawing_object.y2 = event.y
#             if self.draw_mode == "line":
#                 self.canvas.delete("current_line")
#                 self.canvas.create_line(self.drawing_object.x1, self.drawing_object.y1, self.drawing_object.x2, self.drawing_object.y2, fill="black", width=2)
#             elif self.draw_mode == "rect":
#                 pass
#             self.draw_mode = False
#             self.drawing_object = None

# def main():
#     root = tk.Tk()
#     app = DrawingApp(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()











