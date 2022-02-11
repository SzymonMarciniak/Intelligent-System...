from tkinter import *
import os
import tkinter

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

bg = PhotoImage(file=f"{prefix}/test1.png")
main = Label(tk, image=bg, width=1920, height=1080)
main.place(x=0, y=0)


def findXCenter(canvas, item):
    coords = canvas.bbox(item)
    xOffset = (windowWidth / 2) - ((coords[2] + coords[0]) / 2)
    yOffset = (windowHeight /2) - ((coords[3] + coords[1]) / 2)
    return xOffset, yOffset

def search_function():
    print(f"Searching: {ID.get()}")

def character_limit(entry_text):
    if len(entry_text.get()) > 8:
        entry_text.set(entry_text.get()[:-1])

def to_uppercase(*args):
    ID.set(ID.get().upper())



label_up = Label(tk,text="", bg=blue_color, width=1920, height=5)
label_up.config(anchor=N)
label_up.pack(side=TOP)

label_down = Label(tk,text="", bg=blue_color, width=1920, height=5)
label_down.config(anchor=E)
label_down.pack(side=BOTTOM)

hello_label = Label(main, text="Enter yours car registration numbers", fg="black", bg="white", font=large_font, \
      highlightbackground=blue_color, highlightthickness=8)
hello_label.place(relx=0.5, rely=0.35, anchor=CENTER)

main_canvas = Canvas(main, width=1000, height=500, bg=blue_color, highlightthickness=0)
main_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

ID = tkinter.StringVar()
search_place = Entry(main_canvas, width=20, textvariable=ID, font=large_font, justify=CENTER)
search_place.grid(row=0,column=1, padx=(10,10), ipady=20)
ID.trace("w", lambda *args: character_limit(ID))
ID.trace_add('write', to_uppercase)

search_button = Button(main_canvas, text="Search", command=search_function, pady=40, font=small_font, bg="white", bd=7, \
    activebackground="#cfcfcf", relief=GROOVE)
search_button.grid(row=0, column=2)

tk.mainloop()


# "#334cc0"












