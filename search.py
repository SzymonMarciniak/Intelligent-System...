from tkinter import *
import os 

blue_color = "#4da6ff"
large_font = ('Verdana bold',35)

class Search:
    def __init__(self, tk: LabelFrame, cancel_icon: PhotoImage) -> None:
        self.tk = tk
        self.cancel_icon = cancel_icon
    
    def exit_search(self):
        self.searchFrame.place_forget()
        self.tk.SearchIsOpen = False

    def main(self, car_registration, language):

        self.car_registration = car_registration

        self.searchFrame = LabelFrame(self.tk, bd=5, bg="white", width=1300, height=650, highlightbackground=blue_color, background=blue_color)
        self.searchFrame.place(relx=0.5, rely=0.5, anchor=CENTER) 

        cancel_button = Button(self.searchFrame, image=self.cancel_icon, borderwidth=0, bg=blue_color, bd=0, highlightthickness=0, \
            activebackground=blue_color, command=self.exit_search)
        cancel_button.place(relx=0.95, rely=0)
        cancel_button.image = self.cancel_icon

        self.textLabel = Label(self.searchFrame, text=f"Searching: {car_registration}", bg=blue_color, font=large_font)
        self.textLabel.place(relx=0.35, rely=0.1)

        if language == "en":
            self.english_language() 
        elif language == "pl":
            self.polish_language()
    
    def english_language(self):
        self.textLabel.config(text=f"Searching: {self.car_registration}")

    def polish_language(self):
        self.textLabel.config(text=f"Wyszukiwanie: {self.car_registration}") 