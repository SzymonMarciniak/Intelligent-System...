from cgitb import text
from tkinter import *
import os 

blue_color = "#4da6ff"
large_font = ('Verdana bold',25)

class Info:
    def __init__(self, tk:LabelFrame, cancel_icon:PhotoImage) -> None:
        self.tk = tk
        self.cancel_icon = cancel_icon
    
    def exit_info(self):
        self.infoFrame.place_forget()
        self.tk.InfoIsOpen = False

    def main(self, language):
        self.infoFrame = LabelFrame(self.tk, bd=5, bg="white", width=800, height=800, highlightbackground=blue_color, background=blue_color )
        self.infoFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        cancel_button = Button(self.infoFrame, image=self.cancel_icon, borderwidth=0, bg=blue_color, bd=0, highlightthickness=0, \
            activebackground=blue_color, command=self.exit_info)
        cancel_button.place(relx=0.92, rely=0)
        cancel_button.image = self.cancel_icon 

        self.description = Label(self.infoFrame, bg=blue_color, bd=0, font=large_font, text="""Hello,\n Have you forgotten where you parked your car?\n
If so, you've come to the right place.\n\n I am a system that will find the location\n of yours car in the underground parking.""")
        self.description.place(rely=0.25, relx=0.5, anchor=CENTER)
    
        if language == "en":
            self.english_language() 
        elif language == "pl":
            self.polish_language()

    def polish_language(self):
        self.description.config(text="""Cześć,\n Zapomniałeś gdzie zaparkowałeś samochód?\n
Jeśli tak to dobrze trafiłeś.\n\n Jestem systemem, który znajdzie polożenie\n Twojego samochodu, na parkingu podziemnym.""") 
    def english_language(self):
        self.description.config(text="""Hello,\n Have you forgotten where you parked your car?\n
If so, you've come to the right place.\n\n I am a system that will find the location\n of your car, in the underground parking.""") 