from tkinter import *
import os
import json
import tkinter
import threading
import PIL.Image, PIL.ImageTk

from search import Search
from information import Info
from AImain import AImanager

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

prefix = os.getcwd()
db = f"{prefix}/DataBase.json"

class Main:
    def __init__(self, tk:Frame) -> None:

        self.tk = tk
        self.prefix = os.getcwd()

        self.bg = PhotoImage(file=f"{self.prefix}/data/bg.png")
        self.cancel_icon_ = PIL.Image.open(f"{self.prefix}/data/cancel-icon.png")
        self.cancel_icon = self.cancel_icon_.resize((60,60))
        self.cancel_icon = PIL.ImageTk.PhotoImage(self.cancel_icon)

        self.main = Label(self.tk, image=self.bg, width=1920, height=1080)
        self.main.place(x=0, y=0)

        self.search = Search(self.tk, self.cancel_icon)
        self.info = Info(self.tk, self.cancel_icon)
        self.language = "en"

        self.tk.SearchIsOpen = False
        self.tk.InfoIsOpen = False
    
    def findXCenter(self, canvas, item):
        coords = canvas.bbox(item)
        xOffset = (windowWidth / 2) - ((coords[2] + coords[0]) / 2)
        yOffset = (windowHeight /2) - ((coords[3] + coords[1]) / 2)
        return xOffset, yOffset

    def character_limit(self, entry_text):
        if len(entry_text.get()) > 8:
            entry_text.set(entry_text.get()[:-1])

    def to_uppercase(self, *args):
        self.ID.set(self.ID.get().upper())
    
    def main_function(self):        

        toolFrame = LabelFrame(self.main, bd=3, bg="white", width=875, height=275, highlightbackground=blue_color, background=blue_color)
        toolFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        label_up = Label(self.tk,text="", bg=blue_color, width=1920, height=5)
        label_up.config(anchor=N)
        label_up.pack(side=TOP)

        car_photo_ = PIL.Image.open(f"{self.prefix}/data/car.jpg")
        car_photo_ = car_photo_.resize((650,450))
        self.car_photo = PIL.ImageTk.PhotoImage(car_photo_)

        english_flag_photo_ = PIL.Image.open(f"{self.prefix}/data/ef.png")
        english_flag_photo_ = english_flag_photo_.resize((57,57))
        english_flag_photo = PIL.ImageTk.PhotoImage(english_flag_photo_)

        english_flag = Button(self.tk, image=english_flag_photo, borderwidth=0, bg=blue_color, bd=0, highlightthickness=0,\
             activebackground=blue_color, command=self.english_language)
        english_flag.place(relx=0.95, rely=0)
        english_flag.image = english_flag_photo

        polish_flag_photo_ = PIL.Image.open(f"{self.prefix}/data/pf.png")
        polish_flag_photo_ = polish_flag_photo_.resize((57,57))
        polish_flag_photo = PIL.ImageTk.PhotoImage(polish_flag_photo_)

        polish_flag = Button(self.tk, image=polish_flag_photo, borderwidth=0, bg=blue_color, bd=0, highlightthickness=0,\
             activebackground=blue_color, command=self.polish_language)
        polish_flag.place(relx=0.90, rely=0)
        polish_flag.image = polish_flag_photo

        info_photo_ = PIL.Image.open(f"{self.prefix}/data/info.png")
        info_photo_ = info_photo_.resize((57,57))
        info_photo = PIL.ImageTk.PhotoImage(info_photo_)

        info = Button(self.tk, image=info_photo, borderwidth=0, bg=blue_color, bd=0, highlightthickness=0,\
             activebackground=blue_color, command=self.info_function)
        info.place(relx=0.02, rely=0)
        info.image = info_photo

        label_down = Label(self.tk,text="", bg=blue_color, width=1920, height=5)
        label_down.config(anchor=E)
        label_down.pack(side=BOTTOM)

        self.hello_label = Label(toolFrame, text="Enter yours car registration numbers", fg="black", bg="white", font=large_font, \
            highlightbackground="white", highlightthickness=8)
        self.hello_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        main_canvas = Canvas(toolFrame, width=1000, height=500, bg=blue_color, highlightthickness=0)
        main_canvas.place(relx=0.5, rely=0.7, anchor=CENTER)

        self.ID = tkinter.StringVar()
        self.search_place = Entry(main_canvas, width=20, textvariable=self.ID, font=large_font, justify=CENTER, bd=3)
        self.search_place.grid(row=0,column=1, padx=(10,10), ipady=20)
        self.ID.trace("w", lambda *args: self.character_limit(self.ID))
        self.ID.trace_add('write', self.to_uppercase)

        self.search_button = Button(main_canvas, text="Search", command=self.search_function, pady=22, padx=60, font=small_font, bg="white", bd=7, \
            activebackground="#cfcfcf", relief=GROOVE)
        self.search_button.grid(row=0, column=2, padx=(20,0))

        self.cameras = []
        self.cameras_nr = []

        self.check_cameras()
        print(self.cameras)
        
        img_path = os.path.join("data", "sad.png")
        img = PIL.Image.open(img_path)
        img = img.resize((400,400))
        self.sad_image = PIL.ImageTk.PhotoImage(img)

        self.tk.mainloop()
    
    def polish_language(self):
        self.language = "pl"
        self.hello_label.config(text="Wpisz numer rejestracyjny\n swojego samochodu")
        self.hello_label.place(relx=0.5, rely=0.25)
        self.search_button.config(text="Wyszukaj", padx=42)

        if self.tk.SearchIsOpen:
            self.search_function(reopen=True)
        if self.tk.InfoIsOpen:
            self.info_function(reopen=True)
        
    
    def english_language(self):
        self.language = "en"
        self.hello_label.config(text="Enter yours car registration numbers")
        self.hello_label.place(relx=0.5, rely=0.2)
        self.search_button.config(text="Search", padx=60)

        if self.tk.SearchIsOpen:
            self.search_function(reopen=True)
        if self.tk.InfoIsOpen:
            self.info_function(reopen=True)
        
    def search_function(self, reopen=False):
        if reopen:
            self.search.exit_search()
        self.tk.SearchIsOpen = True
        self.search.main(self.ID.get(), self.language, self.car_photo, self.cameras, self.sad_image)
        self.search_place.delete(0, 'end')
    
    def info_function(self, reopen=False):
        if reopen:
            self.info.exit_info()
        self.tk.InfoIsOpen = True
        self.info.main(self.language) 
    

    def check_cameras(self):
        with open(db, "r", encoding="utf-8") as file:
            data = json.load(file)
            cameras = data["db"]["cameras"]

        for nr in cameras:
            if not nr in self.cameras_nr:
                self.cameras_nr.append(nr)
                img_car_path = os.path.join("AIData", "test", f"Cars{nr}.png")
                car_img = PIL.Image.open(img_car_path)
                car_img = car_img.resize((650,450))
                car_img = PIL.ImageTk.PhotoImage(car_img)
                self.cameras.append(car_img)
            print(self.cameras)
    
        self.tk.after(5000, self.check_cameras)

    

if __name__=="__main__":

    AIThread = threading.Thread(target=AImanager)
    AIThread.start()

    main = Main(tk)
    main.main_function()














