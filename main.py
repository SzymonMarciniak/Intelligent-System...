from tkinter import *
import os
import tkinter
import PIL.Image, PIL.ImageTk

from search import Search


prefix = os.getcwd()

tk = Tk()
tk.attributes("-fullscreen", True)
tk.bind("<Escape>", exit)
tk.configure(background="white")
windowWidth = 1920
windowHeight = 1080

extralarge_font = ('Verdana bold',40)
large_font = ('Verdana bold',35)
small_font = ('Verdana bold',28)
blue_color = "#4da6ff"

bg = PhotoImage(file=f"{prefix}/data/bg.png")
cancel_icon_ = PIL.Image.open(f"{prefix}/data/cancel-icon.png")
cancel_icon = cancel_icon_.resize((60,60))
cancel_icon = PIL.ImageTk.PhotoImage(cancel_icon)

main = Label(tk, image=bg, width=1920, height=1080)
main.place(x=0, y=0)

search = Search(tk, cancel_icon)

def findXCenter(canvas, item):
    coords = canvas.bbox(item)
    xOffset = (windowWidth / 2) - ((coords[2] + coords[0]) / 2)
    yOffset = (windowHeight /2) - ((coords[3] + coords[1]) / 2)
    return xOffset, yOffset

def search_function():
    search.main(ID.get())

def character_limit(entry_text):
    if len(entry_text.get()) > 8:
        entry_text.set(entry_text.get()[:-1])

def to_uppercase(*args):
    ID.set(ID.get().upper())

toolFrame = LabelFrame(main, bd=3, bg="white", width=875, height=250, highlightbackground=blue_color, background=blue_color)
toolFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

label_up = Label(tk,text="", bg=blue_color, width=1920, height=5)
label_up.config(anchor=N)
label_up.pack(side=TOP)

english_flag_photo_ = PIL.Image.open(f"{prefix}/data/ef.png")
english_flag_photo_ = english_flag_photo_.resize((57,57))
english_flag_photo = PIL.ImageTk.PhotoImage(english_flag_photo_)

english_flag = Button(tk, image=english_flag_photo, borderwidth=0, bg=blue_color, bd=0, highlightthickness=0, activebackground=blue_color)
english_flag.place(relx=0.95, rely=0)
english_flag.image = english_flag_photo

polish_flag_photo_ = PIL.Image.open(f"{prefix}/data/pf.png")
polish_flag_photo_ = polish_flag_photo_.resize((57,57))
polish_flag_photo = PIL.ImageTk.PhotoImage(polish_flag_photo_)

polish_flag = Button(tk, image=polish_flag_photo, borderwidth=0, bg=blue_color, bd=0, highlightthickness=0, activebackground=blue_color)
polish_flag.place(relx=0.90, rely=0)
polish_flag.image = polish_flag_photo

info_photo_ = PIL.Image.open(f"{prefix}/data/info.png")
info_photo_ = info_photo_.resize((57,57))
info_photo = PIL.ImageTk.PhotoImage(info_photo_)

info = Button(tk, image=info_photo, borderwidth=0, bg=blue_color, bd=0, highlightthickness=0, activebackground=blue_color)
info.place(relx=0.02, rely=0)
info.image = info_photo


label_down = Label(tk,text="", bg=blue_color, width=1920, height=5)
label_down.config(anchor=E)
label_down.pack(side=BOTTOM)

hello_label = Label(toolFrame, text="Enter yours car registration numbers", fg="black", bg="white", font=large_font, \
      highlightbackground="white", highlightthickness=8)
hello_label.place(relx=0.5, rely=0.2, anchor=CENTER)

main_canvas = Canvas(toolFrame, width=1000, height=500, bg=blue_color, highlightthickness=0)
main_canvas.place(relx=0.5, rely=0.7, anchor=CENTER)

ID = tkinter.StringVar()
search_place = Entry(main_canvas, width=20, textvariable=ID, font=large_font, justify=CENTER, bd=3)
search_place.grid(row=0,column=1, padx=(10,10), ipady=20)
ID.trace("w", lambda *args: character_limit(ID))
ID.trace_add('write', to_uppercase)

search_button = Button(main_canvas, text="Search", command=search_function, pady=22, padx=60, font=small_font, bg="white", bd=7, \
    activebackground="#cfcfcf", relief=GROOVE)
search_button.grid(row=0, column=2, padx=(20,0))

tk.mainloop()


# "#334cc0"












