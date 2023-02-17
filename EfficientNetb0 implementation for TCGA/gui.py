import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from time import time
from classification import *

my_w = tk.Tk()
my_w.geometry("410x300")
my_w.title("SERB's sanction No. CRG/20211005752")
my_w.configure(bg="white")
my_font1 = ("times", 18, "bold")
f = open("/home/pi/Ajinkya/Heading.txt","r")
text = f.read()
f.close()
#l1 = tk.Label(my_w, text="").grid(row=1,column=1)
l2 = tk.Label(my_w, anchor="center", text=text, width=70, font=my_font1, background="#FFF250").place(x=0,y=0)
#l3 = tk.Label(my_w, text="").grid(row=1,column=3)

l3 = tk.Label(my_w, text="Pl:DEEP GUPTA\nCO-Pl:ANKIT A. BHURANE, NISHA B. MESHRAM", font=my_font1).place(x=100,y=100)
b1 = tk.Button(my_w, text="Upload File", command=lambda:upload_file()).place(x=350,y=200)

def upload_file():
    global img
    f_types = [("Png Files", "*.png"),("Jpg Files", "*.jpg"),]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = Image.open(filename)
    img_resized = img.resize((256,256))
    img = ImageTk.PhotoImage(img_resized)
    b2 = tk.Button(my_w, image=img).place(x=50,y=250)
    
    t1 = time()
    label = filename.split("/")[-1].split(".")[0][-3]
    cancerType, outputs, loss = predictType(filename,int(label))
    t2 = time()
    
    refy = 280
    refx = 360
    bgs = ["#B3FF6F","#F3FF5E","#FF6C3D"]
    c1 = Canvas(my_w, bg="#E5E4DD", height=256, width=370).place(x=refx-10,y=250)
    l4 = Label(my_w, text="Severity level", font=("times", 12, "bold")).place(x=refx,y=refy)
    text = "{}/2".format(cancerType)
    l5 = Label(my_w, text=text).place(x=refx,y=refy+20)
    s2 = Label(my_w, text="    ",bg=bgs[cancerType]).place(x=refx+40,y=refy+20)
    l6 = Label(my_w, text="Probabilities of cancer Types", font=("times", 12, "bold")).place(x=refx, y=refy+60)
    temp = [str(round(i.item(),6)) for i in outputs[0]]
    text = ""
    for i in range(len(temp)):
        text += "Type{}: {},  ".format(i,temp[i])
    text = text.strip()[:-1]
    print(text)
    l7 = Label(my_w, text=text).place(x=refx,y=refy+80)
    l8 = Label(my_w, text="CrossEntropyLoss", font=("times", 12, "bold")).place(x=refx, y=refy+120)
    l9 = Label(my_w, text=str(loss)).place(x=refx,y=refy+140)
    
    time_req = "{0:.3f} sec".format(t2-t1)
    print("Time required for img acquisition, model building, and prediction = {}".format(time_req))

    l8 = Label(my_w, text="Inference Time", font=("times", 12, "bold")).place(x=refx, y=refy+180)
    l9 = Label(my_w, text=time_req).place(x=refx,y=refy+200)

    l10 = Label(my_w, text="Type0(normal)", bg="#B3FF6F").place(x=500,y=180)
    l10 = Label(my_w, text="Type0(low)", bg="#F3FF5E").place(x=500,y=200)
    l10 = Label(my_w, text="Type0(highest)", bg="#FF6C3D").place(x=500,y=220)
    



my_w.mainloop()
