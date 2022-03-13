import json 
import os 
from tkinter import * 
from tkinter import messagebox

mini_font = ("Verdana", 15)                                                                                                                                                              
small_font = ('Verdana',20)

prefix = os.getcwd()
db = f"{prefix}/DataBase.json"

class CameraConfig:
    def __init__(self, tk_config, tab2) -> None:
        self.tk_config = tk_config
        self.tab2 = tab2 

    def main_config(self):

        #Add Frame

        self.AddMainFrame = LabelFrame(self.tab2, text="Add camera:", font=small_font)
        self.AddMainFrame.grid(column=0, row=0, columnspan=2, sticky='W',padx=(130,50))

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

        ccLabel = Label(self.AddMainFrame, text="", font=mini_font)
        ccLabel.grid(column=0, row=3, padx=(55,20), pady=(25,6))

        self.AddButton = Button(self.AddMainFrame, text="Add camera", command=self.add_camera_function)
        self.AddButton.grid(column=0, row=2, columnspan=2, pady=30)

        #Configure Frame

        self.ConfigMainFrame = LabelFrame(self.tab2, text="Configure:", font=small_font)
        self.ConfigMainFrame.grid(column=2, row=0, columnspan=2, sticky='W', padx=(100,50), pady=30)

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

        #Delete Frame

        self.DeleteMainFrame = LabelFrame(self.tab2, text="Delete camera:", font=small_font)
        self.DeleteMainFrame.grid(column=4, row=0, columnspan=2, sticky='W', padx=(100,120), pady=20)

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

        ccLabel = Label(self.DeleteMainFrame, text="", font=mini_font)
        ccLabel.grid(column=0, row=3, padx=(55,20), pady=(25,6))



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