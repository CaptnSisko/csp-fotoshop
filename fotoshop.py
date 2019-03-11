import Tkinter

root = Tkinter.Tk()
root.wm_title('Fotoshop')

canvas = Tkinter.Canvas(root, height=300, width=300, background='#FFFFFF')
canvas.grid(row=0, column=1, rowspan=3, columnspan=2)

red = Tkinter.IntVar()
green = Tkinter.IntVar()
blue = Tkinter.IntVar()

mouse_pressed = False
prev_x = 0
prev_y = 0

class ColorSlider(Tkinter.Scale): # ColorSlider is a subclass of Tkinter.Scale
    '''A Scale that reports to editor and stores in IntVar
    '''
    def __init__(self, parent, myLabel, model_intvar, canvas):
        '''Creates a new ColorSlider'''
        # Define the event handler for the slider moving 
        def slider_changed(new_val): return
            # Handler passes data from this controller to two views 
            
            #global red, green, blue # the sliders' data
            # Create a hex string from the model data
            # Tell the text window view about it
            # Tell the canvas view about it
            # The canvas view holds the model data in its internal canvas items
            # The viewer exposes the data through itemconfig() and itemcoords()

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

message = Tkinter.Label(root, text='Drag mouse to\ndraw shapes.\nDrag sliders\nto change color.')
message.grid(column=0, row=0, sticky=Tkinter.N)

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
    if not mouse_pressed or not tool.get()==3: return
    x, y = event.x, event.y
    tk_color_string = color(red, green, blue)
    if prev_x != -1: canvas.create_line(prev_x, prev_y, x, y, fill=tk_color_string, width=radius.get())
    #shapes.append(new_shape)
    prev_x, prev_y = x, y

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
tool.set(1) # otherwise they're both 'on'
circle_button.grid(row=3,column=1) 
square_button.grid(row=3,column=2)  
brush_button.grid(row=4, column=1)
eraser_button.grid(row=4, column=2)
radius_slider.grid(row=5, column=1)
radius_label.grid(row=5, column=0)
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
    '''Takes three IntVar and returns a color Tkinter string like #FFFFFF.        
    '''
    rx=hexstring(r)
    gx=hexstring(g)
    bx=hexstring(b)
    return '#'+rx+gx+bx

# Enter event loop
root.mainloop()
