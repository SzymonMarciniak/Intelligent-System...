from tkinter import messagebox
from tkinter.ttk import Notebook, Style
import PIL.Image, PIL.ImageTk
from tkinter import *
import json 
import os

from camera_config import CameraConfig
from about_config import About


mini_font = ("Verdana", 15)                                                                                                                                                              
small_font = ('Verdana',20)

prefix = os.getcwd()
db = f"{prefix}/DataBase.json"

class MainConfig:
    def __init__(self) -> None:

        self.prefix = os.getcwd()

        self.tk_config = Tk()
        self.tk_config.bind("<Escape>", exit)
        self.tk_config.configure(background="gray")
        self.tk_config.title("Intelligent System")

        about = About(self.tk_config)
        

        menuBar = Menu(self.tk_config)
        self.tk_config.config(menu=menuBar)

        fileMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="File", menu=fileMenu, font=mini_font)

        fileMenu.add_command(label="Refresh", font=mini_font, command=self.cameras_display)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=quit, font=mini_font)
    
        helpMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Help", menu=helpMenu, font=mini_font)
        helpMenu.add_command(label="About", command=about.about_function, font=mini_font)

        style = Style()
        style.theme_create( "MyStyle", parent="alt", settings={
                "TNotebook": {"configure": {"tabmargins": [0, 0, 2, 0] } },
                "TNotebook.Tab": {"configure": {"padding": [40, 20] },}})

        style.theme_use("MyStyle")

        notebook = Notebook(self.tk_config)
        tab1 = Frame(notebook)
        notebook.add(tab1, text = 'Camera preview')
        tab2 = Frame(notebook)
        notebook.add(tab2, text = 'Add camera')
        tab3 = Frame(notebook)
        notebook.add(tab3, text = 'Tab 3')
        notebook.pack(expand=True, fill=BOTH, padx=12, pady=12)

        #Camera preview tab

        self.mainFrame = LabelFrame(tab1, text="Cameras available: 7", font=small_font)
        self.mainFrame.grid(column=0, row=0, columnspan=3, sticky='W', padx=50, pady=30)

        self.my_canvas = Canvas(self.mainFrame, width=1800, height=800)
        self.my_canvas.pack(side=LEFT, fill=BOTH, expand=1, pady=(0,30))

        self.my_scrollbar = Scrollbar(self.mainFrame, orient=VERTICAL, command=self.my_canvas.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)

        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion= self.my_canvas.bbox("all")))

        self.camerasFrame = Frame(self.my_canvas)

        self.my_canvas.create_window((0,0), window=self.camerasFrame, anchor="nw")

        car_photo_ = PIL.Image.open(f"{prefix}/data/car.jpg")
        car_photo_ = car_photo_.resize((520,350))
        self.car_photo = PIL.ImageTk.PhotoImage(car_photo_)

        self.car_photo_t = self.car_photo
        self.images = []
        self.aLabel = None
        self.camera_1_button = None 

        self.cameras_display()

        camera_config = CameraConfig(self.tk_config, tab2)
        camera_config.main_config()

        self.tk_config.mainloop()

    
    def cameras_display(self):
        
        cc = 0
        cr = 0 
        _y = 20
        _x = 55
        c_height = 1

        self.images = []
        
        if self.aLabel != None:
            for widget in self.camerasFrame.grid_slaves():
                widget.grid_forget()
          

        with open(db, "r", encoding="utf-8") as file:
            data = json.load(file)
            images = data["db"]["cameras"]
        images_amount = len(images)

        self.mainFrame.config(text=f"Cameras available: {images_amount}")
        
        for i in range(1,images_amount+1):

            img_car_path = os.path.join("AIData", "test", f"Cars{images[i-1]}.png")
            car_photo_ = PIL.Image.open(img_car_path)
            car_photo_ = car_photo_.resize((520,350))
            self.car_photo_t = PIL.ImageTk.PhotoImage(car_photo_)
            self.images.append(self.car_photo_t)

        for i in range(1,images_amount+1):

            self.aLabel = Label(self.camerasFrame, text=f"camera {i} - {images[i-1]}", font=mini_font)
            self.aLabel.grid(column=cc, row=cr, padx=(55,55), pady=(_y, 5))

            self.camera_1_button = Button(self.camerasFrame, image=self.images[i-1], command=lambda:print(f"Camera {i}"), bd=1)
            self.camera_1_button.grid(column=cc, row=cr+1, padx=(_x,55), pady=(0,40))

            if i % 3 == 0:
                cr += 2
                cc = 0
                _y = 10
                _x = 55
                c_height += 1

                self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion=(0,0,1,c_height * 550)))
                self.my_canvas.create_window((0,0), window=self.camerasFrame, anchor="nw")

            else:
                cc += 1
                _x = 0
    


            

if __name__ == "__main__":
    config = MainConfig()


       

