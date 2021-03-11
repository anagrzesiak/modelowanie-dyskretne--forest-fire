from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from numpy import *
import cv2
from math import *
from time import *
from winsound import *
import os
import random

paused = False
root = Tk()
root.title("FOREST FIRE")
root.configure(bg="#F0F2F0")
root.iconbitmap("icon.ico")

im1 = Image.open("lake.jpg").convert('RGB')
width, height = im1.size
mode = im1.mode
orig_pixel_map = im1.load()

new_image2 = Image.new(mode, (width, height))
new_pixel_map2 = new_image2.load()
orig_pixel_map2 = im1.load()

new_image3 = Image.new(mode, (width, height))
new_pixel_map3 = new_image3.load()
orig_pixel_map3 = im1.load()

OPTIONS = [
    "Wind",
    "North",
    "South",
    "East",
    "West",
    "North-West",
    "North-East",
    "South-West",
    "South-East"
]
variable = StringVar(root)
variable.set("Wind")
option = OptionMenu(root, variable, *OPTIONS).grid(row=8, column=0, columnspan=2, sticky='nesw')


def colorize():  # colorize the image so its blue and green
    for x in range(width):
        for y in range(height):
            new_pixel_map2[x, y] = orig_pixel_map2[x, y]
    #
    threshold = 100
    for x in range(width):
        for y in range(height):
            orig_pixel = orig_pixel_map[x, y]
            orig_r = orig_pixel[0]
            orig_g = orig_pixel[1]
            orig_b = orig_pixel[2]

            if (orig_r) <= threshold:
                new_r = int(0)
            else:
                new_r = int(34)
            if (orig_g) <= threshold:
                new_g = int(0)
            else:
                new_g = int(139)
            if int(orig_b) <= threshold:
                new_b = int(255)
            else:
                new_b = int(34)
            new_pixel2 = (new_r, new_g, new_b)
            new_pixel_map2[x, y] = new_pixel2

    return new_image2


def binarize():  # binarization with threshold=100
    for x in range(width):
        for y in range(height):
            new_pixel_map3[x, y] = orig_pixel_map3[x, y]
    #
    threshold = 100
    for x in range(width):
        for y in range(height):
            orig_pixel = orig_pixel_map[x, y]
            orig_r = orig_pixel[0]
            orig_g = orig_pixel[1]
            orig_b = orig_pixel[2]

            if (orig_r) <= threshold:
                new_r = int(0)
            else:
                new_r = int(255)
            if (orig_g) <= threshold:
                new_g = int(0)
            else:
                new_g = int(255)
            if int(orig_b) <= threshold:
                new_b = int(0)
            else:
                new_b = int(255)
            new_pixel3 = (new_r, new_g, new_b)
            new_pixel_map3[x, y] = new_pixel3

    return new_image3


im3 = colorize()
im4 = im3.save("../pozar.jpg")


def convert_to_matrix(img):  # converts the binarized image to an 0/1 array
    image = img;
    image = image.convert('1')
    A = array(image)
    new_A = empty((A.shape[0], A.shape[1]), None)
    for i in range(len(A)):
        for j in range(len(A[0])):
            if A[i][j] == True:
                new_A[i][j] = 0
            else:
                new_A[i][j] = 1
    return new_A


width_ = width
height = height


def neighbourhood(M, i,
                  # returns the list of neighbours for a specific cell depending on its coordinates and chosen wind
                  j):
    xd = choose_wind()
    lista = []
    if i == 0:
        if j == 0:
            if xd == "Wind":
                lista = [M[i + 1][0], M[i + 1][j + 1], M[i][j + 1]]
            elif xd == "West":
                pass
            elif xd == "East":
                lista = [M[i + 1][j + 1], M[i][j + 1]]
            elif xd == "North":
                pass
            elif xd == "South":
                lista = [M[i + 1][0], M[i + 1][j + 1]]
            return lista
        if j == len(M[0]) - 1:
            if xd == "Wind":
                lista = [M[i][len(M[0]) - 2], M[i + 1][len(M[0]) - 2], M[i + 1][len(M[0]) - 1]]
            elif xd == "West":
                lista = [M[i][len(M[0]) - 2], M[i + 1][len(M[0]) - 2]]
            elif xd == "East":
                pass
            elif xd == "North":
                pass
            elif xd == "South":
                lista = [M[i + 1][len(M[0]) - 2], M[i + 1][len(M[0]) - 1]]
            return lista
        else:
            if xd == "Wind":
                lista = [M[i][j - 1], M[i + 1][j - 1], M[i + 1][j], M[i + 1][j + 1], M[i][j + 1]]
            elif xd == "West":
                lista = [M[i][j - 1], M[i + 1][j - 1]]
            elif xd == "East":
                lista = [M[i + 1][j + 1], M[i][j + 1]]
            elif xd == "North":
                pass
            elif xd == "South":
                lista = [M[i + 1][j - 1], M[i + 1][j], M[i + 1][j + 1]]
            return lista

    if i == 330 - 1:
        if j == 0:
            if xd == "Wind":
                lista = [M[len(M) - 2][j], M[len(M) - 2][j + 1], M[len(M) - 1][j + 1]]
            elif xd == "West":
                pass
            elif xd == "East":
                lista = [M[len(M) - 2][j + 1], M[len(M) - 1][j + 1]]
            elif xd == "North":
                lista = [M[len(M) - 2][j], M[len(M) - 2][j + 1]]
            elif xd == "South":
                pass
            return lista
        if j == len(M[0]) - 1:
            if xd == "Wind":
                lista = [M[len(M) - 1][len(M[0]) - 2], M[len(M) - 2][len(M[0]) - 2], M[len(M) - 2][len(M[0]) - 1]]
            elif xd == "West":
                lista = [M[len(M) - 1][len(M[0]) - 2], M[len(M) - 2][len(M[0]) - 2]]
            elif xd == "East":
                pass
            elif xd == "North":
                lista = [M[len(M) - 2][len(M[0]) - 2], M[len(M) - 2][len(M[0]) - 1]]
            elif xd == "South":
                pass
            return lista
        else:
            if xd == "Wind":
                lista = [M[i][j - 1], M[i - 1][j - 1], M[i - 1][j], M[i - 1][j + 1], M[i][j + 1]]
            elif xd == "West":
                lista = [M[i][j - 1], M[i - 1][j - 1]]
            elif xd == "East":
                lista = M[i - 1][j + 1], M[i][j + 1]
            elif xd == "North":
                lista = [M[i - 1][j - 1], M[i - 1][j], M[i - 1][j + 1]]
            elif xd == "South":
                pass
            return lista

    if j == 0:
        if xd == "Wind":
            lista = [M[i - 1][j], M[i - 1][j + 1], M[i][j + 1], M[i + 1][j + 1], M[i + 1][j]]
        elif xd == "West":
            pass
        elif xd == "East":
            lista = [M[i - 1][j + 1], M[i][j + 1], M[i + 1][j + 1]]
        elif xd == "North":
            lista = [M[i - 1][j], M[i - 1][j + 1]]
        elif xd == "South":
            lista = [M[i + 1][j + 1], M[i + 1][j]]
        return lista

    if j == len(M[0]) - 1:
        if xd == "Wind":
            lista = [M[i - 1][j], M[i - 1][j - 1], M[i][j - 1], M[i + 1][j - 1], M[i + 1][j]]
        elif xd == "West":
            lista = [M[i - 1][j - 1], M[i][j - 1], M[i + 1][j - 1]]
        elif xd == "East":
            pass
        elif xd == "North":
            lista = [M[i - 1][j], M[i - 1][j - 1]]
        elif xd == "South":
            lista = [M[i + 1][j - 1], M[i + 1][j]]
        return lista

    else:
        if xd == "Wind":
            lista = [M[i - 1][j - 1], M[i - 1][j], M[i - 1][j + 1], M[i][j + 1], M[i + 1][j + 1], M[i + 1][j],
                     M[i + 1][j - 1], M[i][j - 1]]
        elif xd == "West":
            lista = [M[i - 1][j - 1], M[i + 1][j - 1], M[i][j - 1]]
        elif xd == "East":
            lista = [M[i - 1][j + 1], M[i][j + 1], M[i + 1][j + 1]]
        elif xd == "North":
            lista = [M[i - 1][j - 1], M[i - 1][j], M[i - 1][j + 1]]
        elif xd == "South":
            lista = [M[i + 1][j + 1], M[i + 1][j], M[i + 1][j - 1]]
        elif xd == "North-West":
            lista = [M[i - 1][j - 1], M[i + 1][j - 1], M[i][j - 1], M[i - 1][j - 1], M[i - 1][j], M[i - 1][j + 1]]
        elif xd == "North-East":
            lista = [M[i - 1][j + 1], M[i][j + 1], M[i + 1][j + 1], M[i - 1][j - 1], M[i - 1][j], M[i - 1][j + 1]]
        elif xd == "South-West":
            lista = [M[i + 1][j + 1], M[i + 1][j], M[i + 1][j - 1], M[i - 1][j - 1], M[i + 1][j - 1], M[i][j - 1]]
        elif xd == "South-East":
            lista = [M[i + 1][j + 1], M[i + 1][j], M[i + 1][j - 1], M[i - 1][j + 1], M[i][j + 1], M[i + 1][j + 1]]

        return lista


def evolution(cell):  # changes the cell value depending on its actual state
    if cell == 2:
        return (3)
    if cell == 3:
        return (3)
    if cell == 0:
        return (2)
    else:
        return (1)


def indexForMouseEvent(x):  # get coordinates of mouse event
    x = float(x)
    i = int(x)
    return (i)


im2 = binarize()
Matrix = convert_to_matrix(im2)


def clic(event):  # put the point of origin on canvas(it takes more than one pixel so its more visible)
    global Matrix
    x, y = event.x, event.y
    i, j = indexForMouseEvent(y), indexForMouseEvent(x)
    value = Matrix[i][j]
    if value == 0:
        Matrix[i][j] = 2
        Matrix[i - 1][j] = 2
        Matrix[i + 1][j] = 2
        Matrix[i][j - 1] = 2
        Matrix[i][j + 1] = 2
        can.itemconfig(cells[i - 1, j], fill='red')
        can.itemconfig(cells[i + 1, j], fill='red')
        can.itemconfig(cells[i, j + 1], fill='red')
        can.itemconfig(cells[i, j - 1], fill='red')
        can.itemconfig(cells[i, j], fill='red')


def firefighters():  # searches for red(burning) cells and changes their state to extinguished(actually the state is the same as grass so they can still burn but the color is different)
    global paused
    paused = True
    global Matrix
    print("ok")
    for i in range(330):
        for j in range(600):
            value = Matrix[i][j]
            some_number = random.randint(0, 10)
            if value == 2 and some_number > 5:
                Matrix[i][j] = 0
                can.itemconfig(cells[i, j], fill='green')


def grow_trees():  # grows new trees everywhere except from where trees are currently burning!!! more of a "reset canvas" but yeah
    for i in range(330):
        for j in range(600):
            value = Matrix[i][j]
            if value == 0 or value == 3:
                Matrix[i][j] = 0
                can.itemconfig(cells[i, j], fill='green')
    # root.after(1000, grow_trees())


def check():  # main function - checks neighbours and if there is at least one burning our cell ignites + animation with speed based on chosen humidity
    global Matrix
    global paused
    xd = choose_humidity()
    xd = 100 - xd
    if xd < 20:
        xd = 20
    global Matrix
    global paused
    if paused is True:
        return None
    help()
    for i in range(330):
        for j in range(600):
            value = Matrix[i][j]
            lista2 = lista[i, j]
            licznik = 0;
            some_number = random.randint(0, int((xd) / 2))
            for a in range(len(lista[i, j])):
                if lista2[a] == 2:
                    licznik += 1
                if Matrix[i][j] == 2:
                    Matrix[i][j] = 3
                    can.itemconfig(cells[i, j], fill='#654321')
                if licznik >= 1 and some_number > 5:
                    new_cell = evolution(value)
                    Matrix[i][j] = new_cell
                    if new_cell == 0:
                        can.itemconfig(cells[i, j], fill='green')
                    if new_cell == 1:
                        can.itemconfig(cells[i, j], fill='blue')
                    if new_cell == 2:
                        can.itemconfig(cells[i, j], fill='red')
                    elif new_cell == 3:
                        can.itemconfig(cells[i, j], fill='#654321')
    root.after(10, check)


def help():
    global Matrix
    for i in range(330):
        for j in range(600):
            value = Matrix[i][j]
            lista[i, j] = neighbourhood(Matrix, i, j)


def pause_false():
    global paused
    paused = False


def stop():
    global paused
    paused = True


def start_again():
    pause_false()
    check()


def choose_wind():
    a = variable.get()
    return a


def choose_humidity():  # nom
    a = humidity_scale.get()
    return a


def put_out_fire():
    # PlaySound("sound1.wav", SND_ASYNC)
    root.after(500, firefighters())
    # root.after(50000, grow_trees()) #DLACZEGO


photoimage = ImageTk.PhotoImage(file="../pozar.jpg")
can = Canvas(root, bg='light gray', width=width_, height=height)
can.grid(row=1, column=0, columnspan=2)
can.create_image(0, 0, image=photoimage, anchor=NW)

cells = {}
for i in range(330):
    for j in range(660):
        cells[i, j] = can.create_rectangle(j, i, (j + 1), (i + 1), fill="", outline="")

lista = {}
for i in range(330):
    for j in range(600):
        lista[i, j] = neighbourhood(Matrix, i, j)

can.bind("<Button-1>", clic)
image_to_label = PhotoImage(file='cool.gif')
hehe_label = Label(root, image=image_to_label).grid(row=0, column=0, columnspan=2)
scale_label = Label(root, text="HUMIDITY", fg="#E92308", bg="#F0F2F0").grid(row=2, column=0)
humidity_scale = Scale(root, from_=0, to=100, length=542, orient=HORIZONTAL)
humidity_scale.grid(row=2, column=1)
start_fire_button = Button(root, text="Start the fire!", command=check, padx=50, pady=5,
                           fg="#F0F2F0", bg="#E92308").grid(row=3, column=0, columnspan=2, sticky='nesw')
put_out_fire_button = Button(root, text="Put out the fire!", command=put_out_fire, padx=50, pady=5,
                             fg="#F0F2F0", bg="#E92308").grid(row=4, column=0, columnspan=2, sticky='nesw')
stop_fire_button = Button(root, text="Pause simulation", command=stop, padx=50, pady=5,
                          fg="#F0F2F0", bg="#E92308").grid(row=5, column=0, columnspan=2, sticky='nesw')
start_fire_again_button = Button(root, text="Restart simulation", command=start_again, padx=50, pady=5,
                                 fg="#F0F2F0", bg="#E92308").grid(row=6, column=0, columnspan=2, sticky='nesw')
grow_trees_again_button = Button(root, text="Regrowth", command=grow_trees, padx=50, pady=5,
                                 fg="#F0F2F0", bg="#E92308").grid(row=7, column=0, columnspan=2, sticky='nesw')

root.mainloop()
