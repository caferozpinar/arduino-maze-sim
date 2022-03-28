from tkinter import *
import serial
import time
import sys
import glob
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
import tkinter as tk
from tkinter import messagebox

connection_status = 0
set_connection_port = "none"
set_connection_baudrate = 0
simulation_start_value = 2
end = False
rotation = "up"
request = "size_x"


master_window = Tk()
master_window.title("Maze Simulation")
master_window.geometry('778x490')
master_window.resizable(False, False)

tab_control = ttk.Notebook(master_window)

tab_1 = ttk.Frame(tab_control)
tab_2 = ttk.Frame(tab_control)

tab_control.add(tab_1, text ='Simulation Screen')
tab_control.add(tab_2, text ='Connection')
tab_control.pack(expand = 1, fill ="both")

#Tab_1 start
tab_1_alt_window_1 = Canvas(tab_1, width=440, height=440)
tab_1_alt_window_1.grid(row = 0 ,rowspan=2, column = 0 ,padx = (10,10),pady = (10,10))
tab_1_alt_window_2 = Canvas(tab_1, width=280, height=415)
tab_1_alt_window_2.grid(row = 1 , column = 1 ,padx = (10,10),pady = (0,10))
tab_1_alt_window_3 = Canvas(tab_1, width=280, height=25)
tab_1_alt_window_3.grid(row = 0 , column = 1 ,padx = (10,10),pady = (10,0))

def startSimulation():
    global simulation_start_value
    simulation_start_value = 1;
    pause_button.configure(state="normal")
    start_button.configure(state="disabled")

start_button_frame = Frame(tab_1_alt_window_3, height=25, width=90)
start_button_frame.pack_propagate(0) # don't shrink
start_button_frame.place(x=0,y=2)
start_button = Button(start_button_frame, text="Start",bg="green",command=startSimulation,activebackground='blue')
start_button.pack(fill=BOTH, expand=1)
start_button.configure(state="disabled")

def pauseSimulation():
    global simulation_start_value
    simulation_start_value = 2;
    start_button.configure(state="normal")
    pause_button.configure(state="disabled")

pause_button_frame = Frame(tab_1_alt_window_3, height=25, width=90)
pause_button_frame.pack_propagate(0) # don't shrink
pause_button_frame.place(x=95,y=2)
pause_button = Button(pause_button_frame, text="Pause",bg="yellow",command = pauseSimulation,activebackground='blue')
pause_button.pack(fill=BOTH, expand=1)
pause_button.configure(state="disabled")

def stopSimulation():
    global simulation_start_value
    simulation_start_value = 0;

stop_button_frame = Frame(tab_1_alt_window_3, height=25, width=90)
stop_button_frame.pack_propagate(0) # don't shrink
stop_button_frame.place(x=190,y=2)
stop_button = Button(stop_button_frame, text="Exit",bg="red",command=stopSimulation,activebackground='blue')
stop_button.pack(fill=BOTH, expand=1)



tab_1_textbox_1 = Text(tab_1_alt_window_2)
tab_1_textbox_1.place(x=0,y=0,width=280, height=450)
scrollbar = Scrollbar(tab_1_alt_window_2,command=tab_1_alt_window_2.yview)
scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
tab_1_textbox_1['yscrollcommand'] = scrollbar.set
tab_1_textbox_1.see("end")



#Tab1 end

#Tab_2 start
tab_2_alt_window_1 = Canvas(tab_2, width=280, height=440)
tab_2_alt_window_1.grid(row = 0 , column = 0 ,padx = (10,10),pady = (10,10))
tab_2_alt_window_2 = Canvas(tab_2, width=440, height=440)
tab_2_alt_window_2.grid(row = 0 , column = 1 ,padx = (10,10),pady = (10,10))

image_1 = Image.open("5.png")
resized_image= image_1.resize((440,440), Image.ANTIALIAS)
test= ImageTk.PhotoImage(resized_image)
label1 = Label(tab_2_alt_window_2,image=test)
label1.image = test
label1.place(x=0, y=0)

options_1 = ["COM0"]
options_2 = ["300 baud",
            "1200 baud",
            "2400 baud",
            "4800 baud",
            "9600 baud",
            "19200 baud",
            "38400 baud",
            "57600 baud",
            "74880 baud",
            "115200 baud",
            "230400 baud",
            "250000 baud",
            "500000 baud",
            "1000000 baud",
            "2000000 baud"]
clicked_1 = StringVar()
clicked_1.set("Select Port")

clicked_2 = StringVar()
clicked_2.set("Select Baudrate")

#connection text label
connection_label = Label(tab_2,text = "CONNECTION")
connection_label.configure(font='Helvetica 10 bold')
connection_label.place(x=20,y=20)

#connectiopn port
conn_port_frame = Frame(tab_2, height=25, width=270)
conn_port_frame.pack_propagate(0) # don't shrink
conn_port_frame.place(x=20,y=50)
conn_port_dropmenu = OptionMenu(conn_port_frame,clicked_1,*options_1)
conn_port_dropmenu.pack(fill=BOTH, expand=1)

#connection baudrate
conn_baudrate_frame = Frame(tab_2, height=25, width=270)
conn_baudrate_frame.pack_propagate(0) # don't shrink
conn_baudrate_frame.place(x=20,y=85)
conn_baudrate_dropmenu = OptionMenu(conn_baudrate_frame,clicked_2,*options_2)
conn_baudrate_dropmenu.pack(fill=BOTH, expand=1)

def connectSerialDevice():
    temp = " "
    global serial_device
    global connection_status
    if connection_status == 0:
        connection_status = 1
        time.sleep(0.5)
        conn_baudrate_dropmenu.configure(state="disabled")
        conn_port_dropmenu.configure(state="disabled")
        set_connection_port = clicked_1.get()
        for m in clicked_2.get():
            if m.isdigit():
                temp = temp + m
        set_connection_baudrate = int(temp)
        printText(set_connection_port)
        printText(set_connection_baudrate)
        serial_device = serial.Serial(port = set_connection_port,baudrate=set_connection_baudrate,timeout=.1)
        tab_control.select(tab_1)
        conn_button.configure(text="Disconnect",bg="red")
        start_button.configure(state="normal")
        time.sleep(1)
    elif connection_status == 1:
        connection_status = 0
        time.sleep(0.5)
        clicked_1.set("Select Port")
        clicked_2.set("Select Baudrate")
        conn_baudrate_dropmenu.configure(state="normal")
        conn_port_dropmenu.configure(state="normal")
        conn_button.configure(text="Connect",bg="green")
        start_button.configure(state="disabled")
        pause_button.configure(state="disabled")
        time.sleep(1)

#connection buton also show connection status
conn_button_frame = Frame(tab_2, height=25, width=270)
conn_button_frame.pack_propagate(0) # don't shrink
conn_button_frame.place(x=20,y=120)
conn_button = Button(conn_button_frame, text="Connect",command = connectSerialDevice,bg="green",activebackground='grey')
conn_button.pack(fill=BOTH, expand=1)
conn_button.configure(state="disabled")

tab_2_alt_window_1.create_line(20,143,270,143,fill="black")
tab_2_alt_window_1.create_line(20,144,270,144,fill="black")
tab_2_alt_window_1.create_line(20,145,270,145,fill="black")

#image text
image_setting_label = Label(tab_2,text = "IMAGE SETTINGS")
image_setting_label.configure(font='Helvetica 10 bold')
image_setting_label.place(x=20,y=165)

def browseImageFile():
    image_file_name = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("all files","*.*"),("PNG files","*.PNG*"),("JPEG files","*.JPG")))
    image_path_entry.delete(0,END)
    image_path_entry.insert(0,image_file_name)
    printText(image_path_entry.get())

#select image
image_select_button_frame = Frame(tab_2, height=25, width=270)
image_select_button_frame.pack_propagate(0) # don't shrink
image_select_button_frame.place(x=20,y=200)
image_select_button = Button(image_select_button_frame,command=browseImageFile, text="Select Image")
image_select_button.pack(fill=BOTH, expand=1)
#img path
image_path_entry_frame = Frame(tab_2, height=25, width=270)
image_path_entry_frame.pack_propagate(0) # don't shrink
image_path_entry_frame.place(x=20,y=235)
image_path_entry = Entry(image_path_entry_frame)
image_path_entry.pack(fill=BOTH, expand=1)


def prewievImage():
    resized_image_2= Image.open(image_path_entry.get()).resize((440,440), Image.ANTIALIAS)
    image_2= ImageTk.PhotoImage(resized_image_2)
    label1.configure(image=image_2)
    label1.image = image_2

#prewiev
image_preview_button_frame = Frame(tab_2, height=25, width=270)
image_preview_button_frame.pack_propagate(0) # don't shrink
image_preview_button_frame.place(x=20,y=270)
image_preview_frame_button = Button(image_preview_button_frame,command=prewievImage, text="Prewiew Image")
image_preview_frame_button.pack(fill=BOTH, expand=1)

def convertImage():
    #read maze
    global maze_image_x
    global maze_image_y
    global map_array
    global grid_size
    #tab_control.select(tab_1)
    maze_image = Image.open(image_path_entry.get())
    px = maze_image.load()
    px[4, 4] = (0, 0, 0)
    width, height = maze_image.size
    maze_image_x = int(width / 20)
    maze_image_y = int(height / 20)

    map_array = [[0for y in range(maze_image_y)]for x in range(maze_image_x)]

    for o in range(maze_image_x):
        for l in range(maze_image_y):
            coordinate = ((l * 20) + 10, (o * 20) + 10)
            if maze_image.getpixel(coordinate) == (0, 0, 0, 255):
                map_array[o][l] = 1
            if maze_image.getpixel(coordinate) == (255, 255, 255, 255):
                map_array[o][l] = 0
            if maze_image.getpixel(coordinate) == (255, 0, 0, 255):
                map_array[o][l] = 25
            if maze_image.getpixel(coordinate) == (0, 0, 255, 255):
                map_array[o][l] = 35
    conn_button.configure(state="normal")            
    #write maze
    grid_size = int(460 / maze_image_x)
    for y in range(maze_image_x):
        for x in range(maze_image_y):
            if map_array[y][x] == True:
                tab_1_alt_window_1.create_rectangle((x * grid_size), (y * grid_size), ((x * grid_size) + grid_size), ((y * grid_size) + grid_size), fill=("black"),outline="")
            if map_array[y][x] == False:
                tab_1_alt_window_1.create_rectangle((x * grid_size), (y * grid_size), ((x * grid_size) + grid_size), ((y * grid_size) + grid_size), fill=("white"),outline="")
            if map_array[y][x] == 25:
                tab_1_alt_window_1.create_rectangle((x * grid_size), (y * grid_size), ((x * grid_size) + grid_size), ((y * grid_size) + grid_size), fill=("red"),outline="")
                tab_1_alt_window_1.create_polygon( ((x * grid_size)+(grid_size/6)),((y * grid_size)+(grid_size/6)),((x * grid_size)+(grid_size/6)),((y * grid_size)+((grid_size/6)*5)),((x * grid_size)+((grid_size/6)*5)),((y * grid_size)+((grid_size/6)*3)), fill='black')
            if map_array[y][x] == 35:
                tab_1_alt_window_1.create_rectangle((x * grid_size), (y * grid_size), ((x * grid_size) + grid_size),((y * grid_size) + grid_size), fill=("blue"),outline="")



#Convert Image
image_convert_button_frame = Frame(tab_2, height=25, width=270)
image_convert_button_frame.pack_propagate(0) # don't shrink
image_convert_button_frame.place(x=20,y=305)
image_convert_button = Button(image_convert_button_frame,command=convertImage, text="Convert Image")
image_convert_button.pack(fill=BOTH, expand=1)

#image settings
image_color_setting_label = Label(tab_2,text = "IMAGE COLOR SETTINGS")
image_color_setting_label.configure(font='Helvetica 10 bold')
image_color_setting_label.place(x=20,y=340)

#wall colors
wall_color_label = Label(tab_2,text = "WALL'S COLOR")
wall_color_label.configure(font='Helvetica 10 bold')
wall_color_label.place(x=20,y=375)

label_4 = Label(tab_2,text = "R")
label_4.configure(font='Helvetica 10 bold')
label_4.place(x=145,y=375)
frame_8 = Frame(tab_2, height=25, width=30)
frame_8.pack_propagate(0) # don't shrink
frame_8.place(x=160,y=375)
Entry_2 = Entry(frame_8)
Entry_2.pack(fill=BOTH, expand=1)

label_5 = Label(tab_2,text = "G")
label_5.configure(font='Helvetica 10 bold')
label_5.place(x=195,y=375)
frame_9 = Frame(tab_2, height=25, width=30)
frame_9.pack_propagate(0) # don't shrink
frame_9.place(x=210,y=375)
Entry_3 = Entry(frame_9)
Entry_3.pack(fill=BOTH, expand=1)

label_6 = Label(tab_2,text = "B")
label_6.configure(font='Helvetica 10 bold')
label_6.place(x=245,y=375)
frame_10 = Frame(tab_2, height=25, width=30)
frame_10.pack_propagate(0) # don't shrink
frame_10.place(x=260,y=375)
Entry_4 = Entry(frame_10)
Entry_4.pack(fill=BOTH, expand=1)

#Path colors
path_color_label = Label(tab_2,text = "PATH'S COLOR")
path_color_label.configure(font='Helvetica 10 bold')
path_color_label.place(x=20,y=410)

label_5 = Label(tab_2,text = "R")
label_5.configure(font='Helvetica 10 bold')
label_5.place(x=145,y=410)
frame_11 = Frame(tab_2, height=25, width=30)
frame_11.pack_propagate(0) # don't shrink
frame_11.place(x=160,y=410)
Entry_5 = Entry(frame_11)
Entry_5.pack(fill=BOTH, expand=1)

label_6 = Label(tab_2,text = "G")
label_6.configure(font='Helvetica 10 bold')
label_6.place(x=195,y=410)
frame_12 = Frame(tab_2, height=25, width=30)
frame_12.pack_propagate(0) # don't shrink
frame_12.place(x=210,y=410)
Entry_6 = Entry(frame_12)
Entry_6.pack(fill=BOTH, expand=1)

label_7 = Label(tab_2,text = "B")
label_7.configure(font='Helvetica 10 bold')
label_7.place(x=245,y=410)
frame_13 = Frame(tab_2, height=25, width=30)
frame_13.pack_propagate(0) # don't shrink
frame_13.place(x=260,y=410)
Entry_7 = Entry(frame_13)
Entry_7.pack(fill=BOTH, expand=1)

#Tab2 end


for y in range(22):
        for x in range(22):
            if y%2 == True:
                if x%2 == True:
                    tab_1_alt_window_1.create_rectangle((x * 20), (y * 20), ((x * 20) + 20), ((y * 20) + 20), fill=("white"),outline="")
                if x%2 == False:
                    tab_1_alt_window_1.create_rectangle((x * 20), (y * 20), ((x * 20) + 20), ((y * 20) + 20), fill=("black"),outline="")
            if y%2 == False:
                if x%2 == False:
                    tab_1_alt_window_1.create_rectangle((x * 20), (y * 20), ((x * 20) + 20), ((y * 20) + 20), fill=("white"),outline="")
                if x%2 == True:
                    tab_1_alt_window_1.create_rectangle((x * 20), (y * 20), ((x * 20) + 20), ((y * 20) + 20), fill=("black"),outline="")


def start():
    checkAvailableSerial()
    if simulation_start_value == 1:
        mazeSimulation()
    if simulation_start_value == 0:
        onClose()


def checkAvailableSerial():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
            conn_port_dropmenu['menu'].delete(0, 'end')
            new_choices = result
            for choice in new_choices:
                conn_port_dropmenu['menu'].add_command(label=choice, command=tk._setit(clicked_1, choice))
        except (OSError, serial.SerialException):
            pass

def mazeSimulation():
    #in here start the simulation.
    #first check first screen start and stop buttons.
    #if start button clicked start simulation.
    #if not just do normal loop but disable change image.
    #and if end simulation is clicked stop sim permanent and destroy maze
    #also activate image select path.

    #now just check connection status.
    global request
    time.sleep(0.01)
    serial_device.write(bytes("1",'utf-8'))
    #say device im ready to read
    time.sleep(0.01)
    request = serial_device.readline()
    request = request.decode("utf-8")

    while request == 'size_x':
        serial_device.write(bytes(str(maze_image_x),'utf-8'))
        time.sleep(0.05)
        done = serial_device.readline(serial_device.inWaiting()).decode("utf-8")
        request = "none"
        printText("device--> size_x done")
        if done != 'size_x_done':
            printText("Error ! map size x-axis not done")

    while request == 'size_y':
        serial_device.write(bytes(str(maze_image_y),'utf-8'))
        time.sleep(0.05)
        done = serial_device.readline(serial_device.inWaiting()).decode("utf-8")
        request = "none"
        printText("device--> size_y done")
        if done != 'size_y_done':
            printText("Error ! map size y-axis not done")

    if request == 'setRotationRight':
        printText("device--> " + request)
        while rotation != 'right':
            movePlayer("right")

    elif request == 'turnRight':
        printText("device--> " + request)
        movePlayer("right")

    elif request == 'turnLeft':
        printText("device--> " + request)
        movePlayer("left")

    elif request == 'turnBack':
        printText("device--> " + request)
        movePlayer("right")
        movePlayer("right")

    elif request == 'go':
        printText("device--> " + request)
        movePlayer("go")

    elif request == 'getVal':
        #printText("device--> " + request)
        if end == True:
            value = 35
        if end == False:
            value = setValue()
        serial_device.write(bytes(str(value),'utf-8'))
    else:
        if request != 'none':
            printText("User print -->" + request)

def setValue():

    for y in range(maze_image_x):
        for x in range(maze_image_y):
            if int(map_array[y][x]) == 25:
                device_location = x,y
                break
    x = device_location[0]
    y = device_location[1]

    if rotation == 'right':
        left = map_array[y - 1][x]#left
        forward = map_array[y][x + 1]#forward
        right = map_array[y + 1][x]#right

    if rotation == 'down':
        left = map_array[y][x + 1]#left
        forward = map_array[y + 1][x]#forward
        right = map_array[y][x - 1]#right

    if rotation == 'left':
        left = map_array[y + 1][x]#left
        forward = map_array[y][x - 1]#forward
        right = map_array[y - 1][x]#right

    if rotation == 'up':
        left = map_array[y][x - 1]#left
        forward = map_array[y - 1][x]#forward
        right = map_array[y][x + 1]#right

    # calculate. left-forward-right bit encode
    if left == 35:
        left = 0
    if forward == 35:
        forward = 0
    if right == 35:
        right = 0
    temp = (left * (1*1)) + (forward * (2*1)) + (right * (2*2))

    return temp

def movePlayer(action):
    global rotation
    global end

    for y in range(maze_image_x):
        for x in range(maze_image_y):
            if map_array[y][x] == 25:
                device_location = x,y
                break

    x = device_location[0]
    y = device_location[1]

    if action == "go":
        #print("go")
        if rotation == "right":
            #check right
            if map_array[y][x+1] == 0:
                map_array[y][x + 1] = 25
                map_array[y][x] = 0
                change_red(x+1,y)
                right_arrow(x+1,y)
                change_white(x, y)
            if map_array[y][x+1] == 35:
                map_array[y][x + 1] = 25
                map_array[y][x] = 0
                change_red(x+1,y)
                right_arrow(x+1,y)
                change_white(x, y)
                end = True

        if rotation == "down":
            #check down
            if map_array[y+1][x] == 0:
                map_array[y+1][x] = 25
                map_array[y][x] = 0
                change_red(x, y+1)
                down_arrow(x,y+1)
                change_white(x, y)
            if map_array[y+1][x] == 35:
                map_array[y+1][x] = 25
                map_array[y][x] = 0
                change_red(x, y+1)
                down_arrow(x,y+1)
                change_white(x, y)
                end = True


        if rotation == "left":
            #check left
            if map_array[y][x-1] == 0:
                map_array[y][x - 1] = 25
                map_array[y][x] = 0
                change_red(x-1, y)
                left_arrow(x-1,y)
                change_white(x, y)
            if map_array[y][x-1] == 35:
                map_array[y][x - 1] = 25
                map_array[y][x] = 0
                change_red(x-1, y)
                left_arrow(x-1,y)
                change_white(x, y)
                end = True

        if rotation == "up":
            #check up
            if map_array[y-1][x] == 0:
                map_array[y-1][x] = 25
                map_array[y][x] = 0
                change_red(x, y-1)
                up_arrow(x,y-1)
                change_white(x, y)

            if map_array[y-1][x] == 35:
                map_array[y-1][x] = 25
                map_array[y][x] = 0
                change_red(x, y-1)
                up_arrow(x,y-1)
                change_white(x, y)
                end = True


    if action == "left":
        if rotation == "up":
            rotation = "left"
            change_red(x,y)
            left_arrow(x,y)

        elif rotation == "left":
            rotation = "down"
            change_red(x,y)
            down_arrow(x,y)

        elif rotation == "down":
            rotation = "right"
            change_red(x,y)
            right_arrow(x,y)

        elif rotation == "right":
            rotation = "up"
            change_red(x,y)
            up_arrow(x,y)

    if action == "back":
        printText("now useles")

    if action == "right":
        if rotation == "up":
            rotation = "right"
            change_red(x,y)
            right_arrow(x,y)

        elif rotation == "right":
            rotation = "down"
            change_red(x,y)
            down_arrow(x,y)

        elif rotation == "down":
            rotation = "left"
            change_red(x,y)
            left_arrow(x,y)

        elif rotation == "left":
            rotation = "up"
            change_red(x,y)
            up_arrow(x,y)

def change_red(x,y):
    tab_1_alt_window_1.create_rectangle((x * grid_size), (y * grid_size), ((x * grid_size) + grid_size), ((y * grid_size) + grid_size), fill=("red"))

def change_white(x,y):
    tab_1_alt_window_1.create_rectangle((x * grid_size), (y * grid_size), ((x * grid_size) + grid_size), ((y * grid_size) + grid_size), fill=("blue"),outline="")

def up_arrow(x,y):
    tab_1_alt_window_1.create_polygon(((x * grid_size) + ((grid_size / 6) * 3)), ((y * grid_size) + ((grid_size / 6) * 1)), ((x * grid_size) + ((grid_size / 6) * 1)),
                     ((y * grid_size) + ((grid_size / 6) * 5)), ((x * grid_size) + ((grid_size / 6) * 5)),
                     ((y * grid_size) + ((grid_size / 6) * 5)), fill='black')

def left_arrow(x,y):
    tab_1_alt_window_1.create_polygon(((x * grid_size) + ((grid_size / 6) * 1)), ((y * grid_size) + ((grid_size / 6) * 3)),
                     ((x * grid_size) + ((grid_size / 6) * 5)),
                     ((y * grid_size) + ((grid_size / 6) * 1)), ((x * grid_size) + ((grid_size / 6) * 5)),
                     ((y * grid_size) + ((grid_size / 6) * 5)), fill='black')

def down_arrow(x,y):
    tab_1_alt_window_1.create_polygon(((x * grid_size) + ((grid_size / 6) * 1)), ((y * grid_size) + ((grid_size / 6) * 1)),
                     ((x * grid_size) + ((grid_size / 6) * 5)), ((y * grid_size) + ((grid_size / 6) * 1)),
                     ((x * grid_size) + ((grid_size / 6) * 3)), ((y * grid_size) + ((grid_size / 6) * 5)), fill='black')

def right_arrow(x,y):
    tab_1_alt_window_1.create_polygon(((x * grid_size) + ((grid_size / 6) * 1)), ((y * grid_size) + ((grid_size / 6) * 1)), ((x * grid_size) + ((grid_size / 6) * 1)),
                     ((y * grid_size) + ((grid_size / 6) * 5)), ((x * grid_size) + ((grid_size / 6) * 5)),
                     ((y * grid_size) + ((grid_size / 6) * 3)), fill='black')

def onClose():
    if messagebox.askyesno("Quit", "Do you want to quit?"):
        master_window.destroy()
        sys.exit()

def printText(anystr):
    tab_1_textbox_1.configure(state='normal')
    tab_1_textbox_1.insert('end',anystr)
    tab_1_textbox_1.insert('end',"\n")
    tab_1_textbox_1.see("end")
    tab_1_textbox_1.configure(state='disabled')

tab_control.select(tab_2)
time.sleep(0.05)
while True:
    master_window.update_idletasks()
    master_window.update()
    start()