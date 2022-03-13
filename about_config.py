import json 
import os 
from tkinter import *


small_font = ('Verdana',20)


class About:
    def __init__(self, tk_config) -> None:
        self.tk_config = tk_config

    def about_function(self):
        self.aboutFrame = LabelFrame(self.tk_config,bd=5, bg="white", width=800, height=800, highlightbackground="gray", background="gray")
        self.aboutFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        cancel_button = Button(self.aboutFrame, text="x", borderwidth=0, bg="gray", bd=0, highlightthickness=0, \
            activebackground="gray", command=self.exit_about, font=("Verdana", 17))
        cancel_button.place(relx=0.96, rely=0)

        description = Label(self.aboutFrame, bg="gray", bd=0, font=small_font, text="""About me: \nadiadiabdbadibaisdbi\naodoahdoahsd\noadsasodhaohd""")
        description.place(rely=0.25, relx=0.5, anchor=CENTER)


    def exit_about(self):
        self.aboutFrame.place_forget()