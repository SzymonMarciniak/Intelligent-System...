from tkinter import *
import os 

blue_color = "#4da6ff"
large_font = ('Verdana bold',35)

class Search:
    def __init__(self, tk: LabelFrame, cancel_icon: PhotoImage) -> None:
        self.tk = tk
        self.cancel_icon = cancel_icon
    
    def destroy_me(self):
        self.searchFrame.place_forget()

    def main(self, car_registration):
        self.searchFrame = LabelFrame(self.tk, bd=5, bg="white", width=1300, height=650, highlightbackground=blue_color, background=blue_color)
        self.searchFrame.place(relx=0.5, rely=0.5, anchor=CENTER) 

        cancel_button = Button(self.searchFrame, image=self.cancel_icon, borderwidth=0, bg=blue_color, bd=0, highlightthickness=0, \
            activebackground=blue_color, command=self.destroy_me)
        cancel_button.place(relx=0.95, rely=0)
        cancel_button.image = self.cancel_icon

        textLabel = Label(self.searchFrame, text=f"Searchig: {car_registration}", bg=blue_color, font=large_font)
        textLabel.place(relx=0.35, rely=0.1)