from threading import Thread
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
from PIL import Image
import psutil
from multiprocessing import Queue

global i, plus, j, firstX, firstY, isClicked, speedy, addImage
i = 5
j = 900
speedy = 70
plus = True
addImage = 0
yplus = True
firstX = 0
firstY = 0
isClicked = 0

main_frame = tk.Tk()
setting_frame = tk.Tk()
im = Image.open("dDog.gif")
fim = Image.open("fDog.gif")
# print(ImageSequence.Iterator(im)[0].convert("RGB").g etpixel((800,600)))

running_dog = [tk.PhotoImage(file="dDog.gif", format="gif -index %i" %(i)) for i in range(im.n_frames)]
rrunning_dog = [tk.PhotoImage(file="fDog.gif", format="gif -index %i" %(i)) for i in range(im.n_frames)]
hold_dog = tk.PhotoImage(file="그림1.png")


def update_window(cycle):
    global i, plus, j, yplus, speedy
    if(isClicked==0):
        cycle = (cycle + 1) % len(running_dog)
        if(plus):
            if(i>=main_frame.winfo_screenwidth()):
                plus = False
            i += 5
            if(addImage == 0):
                frame = rrunning_dog[cycle]
            else:
                frame = rnewDog[cycle]
        else:
            if(i<=-50):
                plus = True
            if(addImage == 0):
                frame = running_dog[cycle]
            else:
                frame = newDog[cycle]
            i -= 5
        label.configure(image=frame)
    elif(isClicked == 1):
        frame = hold_dog
        label.configure(image=frame)
    main_frame.after(100-speedy,update_window,cycle)
    main_frame.geometry('+'+str(i)+'+'+str(j))
    
def click_doggy(event):
    global isClicked, firstX, firstY
    print("clicked")
    isClicked = 1
    firstX = event.x
    firstY = event.y

def unclick_doggy(event):
    global isClicked
    print("unclicked")
    isClicked = 0

def motion_doggy(event):
    global isClicked, i, j, firstX, firstY
    print(event.x, event.y)
    print(event.x - firstX, event.y - firstY)
    i += event.x - firstX
    j += event.y - firstY
    print("d")
    main_frame.geometry('+'+str(i)+'+'+str(j))
    isClicked = 1

def getSpeed(self):
    global speedy
    speedy = scale.get()

def fileOpen():
    global addImage, newDog, rnewDog
    fileDir = ""
    fileDir = tk.filedialog.askopenfilename(initialdir = "/",\
        title = "gif파일을 선택 해 주세요", \
            filetypes = ("*.gif", "*gif"))
    if file == "":
        messagebox.showwarning("경고", "파일을 추가해주세요")
    else:
        sim = Image.open(file)
        normalImage = []
        flippedImage = []
        for frame in range(sim.n_frames):
            sim.seek(frame)
            resized = sim.resize((100, 100))
            normalImage.append(resized)
            flippedImage.append(resized.transpose(Image.FLIP_LEFT_RIGHT))
        normalImage[0].save("normalImage.gif", save_all=True, append_images = normalImage[1:], loop = 0)
        flippedImage[0].save("flippedImage.gif", save_all=True, append_images = flippedImage[1:], loop = 0)

        newDog = [tk.PhotoImage(file="normalImage.gif", format="gif -index %i" %(i)) for i in range(sim.n_frames)]
        rnewDog = [tk.PhotoImage(file="flippedImage.gif", format="gif -index %i" %(i)) for i in range(sim.n_frames)]
        addImage = 1
    


label = tk.Label(main_frame,bd=0,bg='blue')
label.bind('<Button-1>', click_doggy)
label.bind('<ButtonRelease-1>', unclick_doggy)
label.bind('<B1-Motion>', motion_doggy)
main_frame.overrideredirect(True)
setting_frame.geometry("400x700")
scale = tk.Scale(setting_frame, variable = speedy, orient = "horizontal", from_ = 0, to_ = 95, resolution= 1, command=getSpeed)
scale.pack(anchor = "center")
'''fileButton = tk.Button(setting_frame, command="fileOpen")
fileButton.pack()'''
main_frame.wm_attributes('-transparentcolor','blue')
main_frame.wm_attributes('-topmost',True)
main_frame.geometry("100x100+500+5")
label.pack()
main_frame.after(1,update_window,0)

main_frame.mainloop()
