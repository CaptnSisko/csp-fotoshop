"""
Fotoshop Source Code
By Jeff and Trevor
Carrboro High School
3/14/19
"""

import Tkinter

root = Tkinter.Tk() # Create the Tkinter window
root.wm_title('Fotoshop')

preview = Tkinter.Canvas(root, height=50, width=50, background='#FFFFFF') # create the canvases
canvas = Tkinter.Canvas(root, height=480, width=640, background='#FFFFFF')
canvas.grid(row=0, column=1, rowspan=3, columnspan=2)

red = Tkinter.IntVar() # define rgb variables
green = Tkinter.IntVar()
blue = Tkinter.IntVar()

mouse_pressed = False # define global variables needed for drawing
prev_x = 0
prev_y = 0

class ColorSlider(Tkinter.Scale): # ColorSlider is a subclass of Tkinter.Scale
    '''A Scale that reports to editor and stores in IntVar
    '''
    def __init__(self, parent, myLabel, model_intvar, canvas):
        '''Creates a new ColorSlider'''
        # Define the event handler for the slider moving
        def slider_changed(new_val):
            tk_color_string = color(red, green, blue)
            preview.create_rectangle(0, 0, preview.winfo_width(), preview.winfo_height(), fill=tk_color_string)
            return

        # To finish creating a ColorSlider, call the constructor for a regular
        # Tkinter.Scale, associated with the model data and the event handler
        Tkinter.Scale.__init__(self, parent, orient=Tkinter.HORIZONTAL, from_=0, to=255,
                                variable=model_intvar, label=myLabel, command=slider_changed)

# Create and place the controllers
red_slider = ColorSlider(root, 'Red:', red, canvas)
red_slider.grid(row=1, column=0, sticky=Tkinter.W)

green_slider = ColorSlider(root, 'Green:', green, canvas)
green_slider.grid(row=2, column=0, sticky=Tkinter.W)

blue_slider = ColorSlider(root, 'Blue:', blue, canvas)
blue_slider.grid(row=3, column=0, sticky=Tkinter.W)    

startx, starty = 300, 300 

# Define canvas' mouse-button event handler
def down(event): # A mouse event will be passed in with x and y attributes
    global startx, starty, mouse_pressed, prev_x, prev_y # Use global variables for assignment
    startx = event.x # Store the mouse down coordinates in the global variables
    starty = event.y
    mouse_pressed = True
    prev_x, prev_y = -1, -1

def up(event):
    global mouse_pressed, red, green, blue
    mouse_pressed = False
    tk_color_string = color(red, green, blue)
    if tool.get()==1: # radio buttons say draw circle
        r = (startx-event.x)**2 + (starty-event.y)**2  # Pythagorean theorem
        r = int(r**.5)                                 # square root to get distance
        canvas.create_oval(startx-r, starty-r, startx+r, starty+r,
                                        fill=tk_color_string, outline='#000000')
    elif tool.get()==2: #radio buttons say draw rectangle
        canvas.create_rectangle(startx, starty, event.x, event.y,
                                        fill=tk_color_string, outline='#000000')
    #shapes.append(new_shape) # aggregate the canvas' item
    

def motion(event):
    global radius, mouse_pressed, prev_x, prev_y
    if not mouse_pressed or not (tool.get()==3 or tool.get()==4): return
    x, y = event.x, event.y
    tk_color_string = color(red, green, blue)
    if tool.get() == 4: tk_color_string = '#FFFFFF'
    if prev_x != -1:
        canvas.create_line(prev_x, prev_y, x, y, fill=tk_color_string, width=radius.get())
        r = radius.get() / 2
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=tk_color_string, outline=tk_color_string)
    prev_x, prev_y = x, y

def clear():
    canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill='#FFFFFF')

# Subscribe handlers to the Button-1 and ButtonRelease-1 events
canvas.bind('<Button-1>', down)
canvas.bind('<ButtonRelease-1>', up)
root.bind('<Motion>', motion)

######
# Create radio buttons to toggle between  circle/rectangle creation
######
tool = Tkinter.IntVar() # 'Most recent' to know which radio button is 'on'
radius = Tkinter.IntVar()
circle_button = Tkinter.Radiobutton(root, text='Circle', variable=tool, value=1)
square_button = Tkinter.Radiobutton(root, text='Square', variable=tool, value=2)
brush_button = Tkinter.Radiobutton(root, text='Brush', variable=tool, value=3)
eraser_button = Tkinter.Radiobutton(root, text='Eraser', variable=tool, value=4)
radius_slider = Tkinter.Scale(root, variable=radius, orient=Tkinter.HORIZONTAL, from_=1, to_=20)
radius_label = Tkinter.Label(root, text='Brush/Eraser Radius:')
clear_button = Tkinter.Button(root, text='Clear Canvas', command=clear)
tool.set(1) # otherwise they're both 'on'
circle_button.grid(row=3,column=1) 
square_button.grid(row=3,column=2)  
brush_button.grid(row=4, column=1)
eraser_button.grid(row=4, column=2)
radius_slider.grid(row=5, column=1)
radius_label.grid(row=5, column=0)
clear_button.grid(row=5, column=2)
preview.grid(row=0, column=0)
######
# Functions to transform Intvars into Tkinter color strings
#######
def hexstring(slider_intvar):
    '''A function to prepare data from controller's widget for view's consumption
    
    slider_intvar is an IntVar between 0 and 255, inclusive
    hexstring() returns a string representing two hexadecimal digits
    '''
    # Get an integer from an IntVar
    slider_int = slider_intvar.get()
    # Convert to hex
    slider_hex = hex(slider_int)
    # Drop the 0x at the beginning of the hex string
    slider_hex_digits = slider_hex[2:] 
    # Ensure two digits of hexadecimal:
    if len(slider_hex_digits)==1:
        slider_hex_digits = '0' + slider_hex_digits 
    return slider_hex_digits

def color(r,g,b):
    '''
    Takes three IntVar and returns a color Tkinter string like #FFFFFF.        
    '''
    rx=hexstring(r)
    gx=hexstring(g)
    bx=hexstring(b)
    return '#'+rx+gx+bx

# Enter event loop
root.mainloop()
