import tkinter as tk
import xml.etree.ElementTree as ET
import math


def point_to_line_distance(px, py, x1, y1, x2, y2):
    # Calculate line segment vector
    line_vec = (x2 - x1, y2 - y1)
    # Calculate point-to-start vector
    point_vec = (px - x1, py - y1)
    # Calculate dot product
    dot_product = point_vec[0] * line_vec[0] + point_vec[1] * line_vec[1]
    line_len_sq = line_vec[0] ** 2 + line_vec[1] ** 2
    # Calculate the projection factor
    t = max(0, min(1, dot_product / line_len_sq))
    # Find the projection point on the line segment
    projection = (x1 + t * line_vec[0], y1 + t * line_vec[1])
    # Calculate the distance from the point to the projection
    distance = math.sqrt((projection[0] - px) ** 2 + (projection[1] - py) ** 2)
    return distance

def point_to_rectangle_distance(px, py, x1, y1, x2, y2):
    # The rectangle's sides
    left = x1
    right = x2
    top = y1
    bottom = y2

    # Distances to each side of the rectangle
    distances = [
        abs(px - left),  # Left side
        abs(px - right),  # Right side
        abs(py - top),  # Top side
        abs(py - bottom)  # Bottom side
    ]

    # Return the minimum distance
    return min(distances)



class Line:
    def __init__(self, canvas):
        self.canvas = canvas
        self.drawing_object = None
        self.draw_mode = True
        self.type = 'Line'
        self.color = 'Black'

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
        self.type = 'Rectangle'
        self.color = 'Black'
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
        
        self.object_types = {}
        self.group_list = []
        self.group_list_temp = []
        self.groups_involved_temp = []
        
        self.line_button = tk.Button(master, text="Line", command=self.set_line_mode)
        self.line_button.pack(side="left")

        self.rect_button = tk.Button(master, text="Rectangle", command=self.set_rect_mode)
        self.rect_button.pack(side="left")

        self.group_button = tk.Button(master, text="Group", command=self.set_group_mode)
        self.group_button.pack(side="left")

        self.done_button = tk.Button(master, text="Done", command=self.set_done_mode)
        self.done_button.pack(side="left")

        self.save_button = tk.Button(master,text="save",command=self.set_save_mode)
        self.save_button.pack(side="left")

        self.open_button = tk.Button(master,text="open",command=self.set_open_mode)
        self.open_button.pack(side="left")

        self.export_button = tk.Button(master,text="export as xml",command=self.set_export_mode)
        self.export_button.pack(side="left")


        self.drawing_tool = None
        self.grouping_mode = False

        self.previous_object = None
        self.selected_object = None
        self.copied_object_coords = None
        self.copied_object_type = None
        self.selected_object_type = None
        self.selected_object_color = None

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-3>",self.check_for_dialog)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        self.master.bind("<BackSpace>", self.delete_object)
        self.master.bind("<Control-c>", self.copy_object)
        self.master.bind("<Control-v>", self.paste_object)
        # self.canvas.bind("<Button-1>", self.highlight_on_click)

        # if self.canvas.drawing_tool:
        #     self.canvas.tag_bind(self.drawing_tool, "<Button-1>", self.highlight_on_click)  # Highlight when clicked
        #     self.canvas.tag_bind(self.drawing_tool, "<Leave>", self.remove_highlight)       # Remove highlight when mouse leaves rectangle

    def check_for_dialog(self,event):
        if not self.drawing_tool:

            if self.selected_object:
                self.canvas.itemconfig(self.selected_object, width=2)
            for obj,type in self.object_types.items():
                bbox = self.canvas.bbox(obj)
                if len(bbox) and bbox[0] <= event.x <= bbox[2] and bbox[1] <= event.y <= bbox[3]:
                    print("Object exists at this location.")
                    self.selected_object = obj
                    self.selected_object_type = type
                    self.show_context_menu(event)
                    return
                            
        print("No object exists at this location")

    def change_color(self, color):
        self.selected_object_color = color
        if self.selected_object_type == 'Rectangle':
            self.canvas.itemconfig(self.selected_object, outline=color)
        elif self.selected_object_type == 'Line':
            self.canvas.itemconfig(self.selected_object, fill=color)

    def change_corner_style(self,sorner_style):
        radius = 7
        if sorner_style == "rounded":
            try:
                x1,y1,x2,y2 = self.canvas.coords(self.selected_object)
                print(x1,y1)
                self.delete_object()
                x_left = x1
                x_right = x2
                y_top = y1
                y_bottom = y2

                # Coordinates of the control points for rounded corners
                control_points = [
                    (x_left + radius, y_top),
                    (x_left, y_top + radius),
                    (x_left, y_bottom - radius),
                    (x_left + radius, y_bottom),
                    (x_right - radius, y_bottom),
                    (x_right, y_bottom - radius),
                    (x_right, y_top + radius),
                    (x_right - radius, y_top)
                ]

                # Draw the rounded rectangle
                new_object = self.canvas.create_polygon(control_points, outline=self.selected_object_color, fill='', width='2',smooth=True)
                self.object_types[new_object] = 'Rectangle'
            except:
                print("Corners already Rounded")
        else:
            try:
                x = self.canvas.coords(self.selected_object)[0] - radius
                y = self.canvas.coords(self.selected_object)[1]
                x1 = self.canvas.coords(self.selected_object)[8] + radius
                y1 = self.canvas.coords(self.selected_object)[9]
                self.delete_object()
                new_object = self.canvas.create_rectangle(x, y, x1, y1, outline=self.selected_object_color, fill='', width='2')
                self.object_types[new_object] = 'Rectangle'
            except:
                print("Corners already Square")


    def show_context_menu(self, event):
        context_menu = tk.Menu(self.master, tearoff=0)
        color_menu = tk.Menu(context_menu, tearoff=0)
        color_menu.add_command(label="Black", command=lambda: self.change_color("black"))
        color_menu.add_command(label="Red", command=lambda: self.change_color("red"))
        color_menu.add_command(label="Blue", command=lambda: self.change_color("blue"))
        color_menu.add_command(label="Green", command=lambda: self.change_color("green"))

        context_menu.add_cascade(label="Color", menu=color_menu)

        if self.selected_object_type == "Rectangle":
            corner_menu = tk.Menu(context_menu, tearoff=0)
            corner_menu.add_command(label="Square", command=lambda: self.change_corner_style("square"))
            corner_menu.add_command(label="Rounded", command=lambda: self.change_corner_style("rounded"))
            context_menu.add_cascade(label="Corner Style", menu=corner_menu)

        context_menu.post(event.x_root, event.y_root)

    def set_line_mode(self):
        self.drawing_tool = Line(self.canvas)

    def set_rect_mode(self):
        self.drawing_tool = Rectangle(self.canvas)

    def set_group_mode(self):
        if self.selected_object and self.is_object_in_group(self.selected_object) == False:
            self.canvas.itemconfig(self.selected_object, width=2)
            self.selected_object = None
        self.grouping_mode = True

    def set_done_mode(self):
        self.grouping_mode = False
        
        self.group_list.append({
            "objects":self.group_list_temp,
            "groups":self.groups_involved_temp                    
            })
        self.groups_involved_temp = []
        self.group_list_temp = []
        print(self.group_list)
        self.remove_highlight()

    def set_save_mode(self):
        try:
            f = open("Drawing.txt","w")
            for obj,type in self.object_types.items():
                cordinates = self.canvas.coords(obj)
                cordinates_str = " ".join(str(x) for x in cordinates)
                if type == "Line":
                    textt = f"line "
                    coloor = self.canvas.itemcget(obj,"fill")
                elif type == "Rectangle":
                    textt = f"rect "
                    coloor = self.canvas.itemcget(obj,"outline")
                textt += f"{cordinates_str} {coloor}"

                if textt:
                    print(textt)
                    f.write(textt + "\n")
            f.close()
        except Exception as e:
            print("error occured!")

    
    def set_open_mode(self):
        try: 
            f = open("Drawing.txt","r")
            lines = f.readlines()
            for line in lines:
                data = line.split()
                coord = [float(data[i]) for i in range(1,5)]
                if data[0] == "rect":
                    self.drawing_object = self.canvas.create_rectangle(coord, outline="black", width=2)
                    print(self.drawing_object)
                    typee = "Rectangle"
                elif data[0] == "line":
                    print(coord)
                    self.drawing_object = self.canvas.create_line(coord, fill="black", width=2)
                    typee = "Line"

                self.object_types[self.drawing_object] = typee
                
        except Exception as e:
            print("error occured!")
            
    def set_export_mode(self):
        print("hrll")
        textt = ""
        root = ET.Element('root')
        for obj,type in self.object_types.items():
            if type == "Line":
                line = ET.SubElement(root,"line")
                # textt += "<line>\n"
                cordinates = self.canvas.coords(obj)
                coloor = self.canvas.itemcget(obj,"fill")
                for i in range(2):
                    if i == 0:
                        begin = ET.SubElement(line,"begin")
                        x1 = ET.SubElement(begin,"x")
                        y1 = ET.SubElement(begin,"y")
                        x1.text = str(cordinates[i])
                        y1.text = str(cordinates[i+1])
                    else:
                        end = ET.SubElement(line,"end")
                        x2 = ET.SubElement(end,"x")
                        y2 = ET.SubElement(end,"y")
                        x2.text = str(cordinates[i+1])
                        y2.text = str(cordinates[i+2])
                colr = ET.SubElement(line,"color")
                colr.text = coloor
            elif type == "Rectangle":
                coloor = self.canvas.itemcget(obj,"outline")
                rectangle = ET.SubElement(root,"rectangle")
                # textt += "<line>\n"
                cordinates = self.canvas.coords(obj)
                coloor = self.canvas.itemcget(obj,"fill")
                for i in range(2):
                    if i == 0:
                        upper_left = ET.SubElement(rectangle,"upper-left")
                        x1 = ET.SubElement(upper_left,"x")
                        y1 = ET.SubElement(upper_left,"y")
                        x1.text = str(cordinates[i])
                        y1.text = str(cordinates[i+1])
                    else:
                        lower_right = ET.SubElement(rectangle,"lower-right")
                        x2 = ET.SubElement(lower_right,"x")
                        y2 = ET.SubElement(lower_right,"y")
                        x2.text = str(cordinates[i+1])
                        y2.text = str(cordinates[i+2])
                colr = ET.SubElement(rectangle,"color")
                colr.text = coloor

        tree = ET.ElementTree(root)
        tree.write('draw.xml')
        print(textt)
            


    def start_draw(self, event):
        if self.drawing_tool:
            print(event)
            object_drawn = self.drawing_tool.start_draw(event)
            print(object_drawn)
            self.object_types[object_drawn] = self.drawing_tool.type
        elif self.grouping_mode:
            self.group_objects(event)
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

    def is_object_in_group(self, obj):
        for sub_list in self.group_list:
            if obj in sub_list:
                return True
        return False
    
    def highlight_on_click(self, event):
        if self.selected_object and self.is_object_in_group(self.selected_object) == False:
            self.canvas.itemconfig(self.selected_object, width=2)
        closest_object = None
        threshold = 5
        closest_distance = float("inf")  # Start with a large distance
        
        # Check each object for the shortest distance to the event point
        for obj, obj_type in self.object_types.items():
            bbox = self.canvas.bbox(obj)
            
            if obj_type == "Rectangle":
                if bbox:
                    # Calculate the distance from the point to the rectangle's sides
                    distance = point_to_rectangle_distance(
                        event.x, event.y, bbox[0], bbox[1], bbox[2], bbox[3]
                    )
                    if distance < closest_distance:
                        closest_object = obj
                        closest_distance = distance
            
            elif obj_type == "Line":
                if bbox:
                    # Calculate the distance from the point to the line segment
                    distance = point_to_line_distance(
                        event.x, event.y, bbox[0], bbox[1], bbox[2], bbox[3]
                    )
                    if distance < closest_distance:
                        closest_object = obj
                        closest_distance = distance
        
        # Highlight the closest object
        if closest_object is not None and closest_distance < threshold:
            self.canvas.itemconfig(closest_object, width=4)  # Highlight the object
            self.selected_object = closest_object
        else:
            print("No object found at this location.")
    def remove_highlight(self, event):
        self.canvas.itemconfig(self.drawing_object, fill="blue")    # Change fill color back to blue when not clicked
        
    def copy_object(self, event=None):
        print("inCopy")
        if self.selected_object:
            print("inCopy1")
            self.copied_object_coords = self.canvas.coords(self.selected_object)
            self.copied_object_type = self.selected_object_type

    def paste_object(self, event):
        print("inPaste")
        if self.copied_object_coords:
            print("inPaste1")
            x1, y1, x2, y2 = self.copied_object_coords
            dx = event.x - x1
            dy = event.y - y1
            print(self.copied_object_type)
            if self.copied_object_type == 'Rectangle':
                print("inPaste2")
                object_pasted = self.canvas.create_rectangle(x1 + dx, y1 + dy, x2 + dx, y2 + dy, outline="black", width=2)
                self.object_types[object_pasted] = 'Rectangle'
            elif self.copied_object_type == 'Line':
                print("inPaste2")
                object_pasted = self.canvas.create_line(x1 + dx, y1 + dy, x2 + dx, y2 + dy, fill="black", width=2)
                self.object_types[object_pasted] = 'Line'
                
    def delete_object(self, event=None):
        if self.selected_object:
            self.canvas.delete(self.selected_object)
            self.object_types.pop(self.selected_object)
            self.selected_object = None
            self.selected_object_type = None


    # def write_file():

        
def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()