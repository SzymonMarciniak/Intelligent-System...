from tkinter import messagebox
from tkinter.ttk import Notebook, Style
import PIL.Image, PIL.ImageTk
from tkinter import *
import json 
import os

from cv2 import CAP_PROP_XI_ACQ_TRANSPORT_BUFFER_COMMIT

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

        menuBar = Menu(self.tk_config)
        self.tk_config.config(menu=menuBar)

        fileMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="File", menu=fileMenu, font=mini_font)

        fileMenu.add_command(label="Refresh", font=mini_font, command=self.cameras_display)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=quit, font=mini_font)
    
        helpMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Help", menu=helpMenu, font=mini_font)
        helpMenu.add_command(label="About", command=lambda:print("dziala"), font=mini_font)

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

        # Add camera tab 

        self.AddMainFrame = LabelFrame(tab2, text="Add camera:", font=small_font)
        self.AddMainFrame.grid(column=0, row=0, columnspan=2, sticky='W', padx=(50,20), pady=20)

        self.aaLabel = Label(self.AddMainFrame, text=f"Camera ID:", font=mini_font)
        self.aaLabel.grid(column=0, row=0, padx=(55,20), pady=(15,3))

        self.AddID = StringVar()
        IDEntered = Entry(self.AddMainFrame, width=12, textvariable=self.AddID)
        IDEntered.grid(column=0, row=1, sticky=W, padx=(55,25))

        self.bbLabel = Label(self.AddMainFrame, text=f"Camera place:", font=mini_font)     
        self.bbLabel.grid(column=1, row=0, padx=(20,55), pady=(15,3))

        self.Addplace = StringVar()
        placeEntered = Entry(self.AddMainFrame, width=12, textvariable=self.Addplace)
        placeEntered.grid(column=1, row=1, sticky=W, padx=(25,55))

        self.AddButton = Button(self.AddMainFrame, text="Add camera", command=self.add_camera_function)
        self.AddButton.grid(column=0, row=2, columnspan=2, pady=30)



        self.ConfigMainFrame = LabelFrame(tab2, text="Configure:", font=small_font)
        self.ConfigMainFrame.grid(column=2, row=0, columnspan=2, sticky='W', padx=(50,20), pady=30)

        self.aaLabel = Label(self.ConfigMainFrame, text=f"Old camera ID:", font=mini_font)
        self.aaLabel.grid(column=0, row=0, padx=(55,20), pady=(15,3))

        self.OldConfID = StringVar()
        IDEntered = Entry(self.ConfigMainFrame, width=12, textvariable=self.OldConfID)
        IDEntered.grid(column=0, row=1, sticky=W, padx=(55,25))

        self.bbLabel = Label(self.ConfigMainFrame, text=f"Old camera place:", font=mini_font)
        self.bbLabel.grid(column=1, row=0, padx=(20,55), pady=(15,3))

        self.OldConfplace = StringVar()
        placeEntered = Entry(self.ConfigMainFrame, width=12, textvariable=self.OldConfplace)
        placeEntered.grid(column=1, row=1, sticky=W, padx=(25,55))

        self.aaLabel = Label(self.ConfigMainFrame, text=f"New camera ID:", font=mini_font)
        self.aaLabel.grid(column=0, row=2, padx=(55,20), pady=(15,3))

        self.NewConfID = StringVar()
        IDEntered = Entry(self.ConfigMainFrame, width=12, textvariable=self.NewConfID)
        IDEntered.grid(column=0, row=3, sticky=W, padx=(55,25))

        self.bbLabel = Label(self.ConfigMainFrame, text=f"New camera place:", font=mini_font)
        self.bbLabel.grid(column=1, row=2, padx=(20,55), pady=(15,3))

        self.NewConfplace = StringVar()
        placeEntered = Entry(self.ConfigMainFrame, width=12, textvariable=self.NewConfplace)
        placeEntered.grid(column=1, row=3, sticky=W, padx=(25,55))

        self.ConfigButton = Button(self.ConfigMainFrame, text="Configure", command=self.config_camera_function)
        self.ConfigButton.grid(column=0, row=4, columnspan=2, pady=30)



        self.DeleteMainFrame = LabelFrame(tab2, text="Delete camera:", font=small_font)
        self.DeleteMainFrame.grid(column=4, row=0, columnspan=2, sticky='W', padx=(50,50), pady=20)

        self.aaLabel = Label(self.DeleteMainFrame, text=f"Camera ID:", font=mini_font)
        self.aaLabel.grid(column=0, row=0, padx=(55,20), pady=(15,3))

        self.DelID = StringVar()
        IDEntered = Entry(self.DeleteMainFrame, width=12, textvariable=self.DelID)
        IDEntered.grid(column=0, row=1, sticky=W, padx=(55,25))

        self.bbLabel = Label(self.DeleteMainFrame, text=f"  or    ", font=mini_font)
        self.bbLabel.grid(column=1,row=0, padx=10, pady=(15,3))

        self.ccLabel = Label(self.DeleteMainFrame, text=f"Camera place:", font=mini_font)
        self.ccLabel.grid(column=2,row=0, padx=(10,20), pady=(15,3))

        self.Delplace = StringVar()
        placeEntered = Entry(self.DeleteMainFrame, width=12, textvariable=self.Delplace)
        placeEntered.grid(column=2, row=1, sticky=W, padx=(20,55))

        self.DeleteButton = Button(self.DeleteMainFrame, text="Delete camera", command=self.delete_camera_function)
        self.DeleteButton.grid(column=0, columnspan=3, row=2, pady=30)

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
    
    def add_camera_function(self):
        print("Adding....")
        camera_id = self.AddID.get()
        camera_place = self.Addplace.get()

        check = self.check_if_not_empty((camera_id, camera_place))
        
        if check:
            with open(db, "r", encoding="utf-8") as file:
                data = json.load(file)
                c_cameras = data["db"]["cameras"]
                c_cameras.append(camera_place)
                data["db"]["cameras"] = c_cameras #to do

            with open(db, "w") as file:
                json.dump(data, file, ensure_ascii=False, indent=4) 

    def config_camera_function(self):
        print("Configure....")
        old_camera_id = self.OldConfID.get()
        old_camera_place = self.OldConfplace.get()
        new_camera_id = self.NewConfID.get()
        new_camera_place = self.NewConfplace.get()

        check = self.check_if_not_empty((old_camera_id, old_camera_place, new_camera_id, new_camera_place))
    
        if check:
            with open(db, "r", encoding="utf-8") as file:
                data = json.load(file)
                c_cameras = data["db"]["cameras"]
                if old_camera_place in c_cameras:
                    idx = c_cameras.index(old_camera_place)
                    c_cameras[idx] = new_camera_place
                    data["db"]["cameras"] = c_cameras

                    with open(db, "w", encoding="utf-8") as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)
                else:
                    answer = messagebox.showinfo("Error", f"Cmaera {old_camera_place} not found")

    def delete_camera_function(self):
        print("Deleting....")

        camera_id = self.DelID.get()    
        camera_place = self.Delplace.get()

        if camera_place:
            with open(db, "r", encoding="utf-8") as file:
                data = json.load(file)
                c_cameras = data["db"]["cameras"]
                if camera_place in c_cameras:
                    c_cameras.remove(camera_place)

                with open(db, "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

        elif camera_id:
            with open(db, "r", encoding="utf-8") as file:
                data = json.load(file)
                c_cameras = data["db"]["cameras"]
                if camera_id in c_cameras: pass #To do 
        
        else:
            _ = self.check_if_not_empty((camera_id, camera_place))
        

    @staticmethod    
    def check_if_not_empty(values):
        for value in values:
            if value: pass 
            else:
                answer = messagebox.showinfo("Error", "Fields can't be empty")
                return False 
        return True 


            

if __name__ == "__main__":
    config = MainConfig()


       

