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
        self.AddMainFrame.grid(column=0, row=0, columnspan=2, sticky='W',padx=(140,60))

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
        self.ConfigMainFrame.grid(column=2, row=0, columnspan=2, sticky='W', padx=(110,60), pady=30)

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
        self.DeleteMainFrame.grid(column=4, row=0, columnspan=2, sticky='W', padx=(150,130), pady=20)

        self.aaLabel = Label(self.DeleteMainFrame, text=f"Camera ID:", font=mini_font)
        self.aaLabel.grid(column=0, row=0, padx=(45,20), pady=(15,3))

        self.DelID = StringVar()
        IDEntered = Entry(self.DeleteMainFrame, width=12, textvariable=self.DelID)
        IDEntered.grid(column=0, row=1, sticky=W, padx=(55,25))

        self.DeleteButton = Button(self.DeleteMainFrame, text="Delete camera", command=self.delete_camera_function)
        self.DeleteButton.grid(column=0, columnspan=3, row=2, pady=30, padx=45)

        ccLabel = Label(self.DeleteMainFrame, text="", font=mini_font)
        ccLabel.grid(column=0, row=3, padx=(55,20), pady=(25,6))

        # Cameras data

        self.cameras_pack_function()
        self.cameras_autorefresh()

    def cameras_pack_function(self):
        self.dataCanvas = Canvas(self.tab2, bd=0)
        self.dataCanvas.grid(column=0, row=1,columnspan=30, sticky=W, padx=200, pady=40)

        self.dataFrame = LabelFrame(self.dataCanvas, bd=0)
        self.dataFrame.grid(column=0, row=0, columnspan=3, sticky=NW)

        cameras_text, cameras_text2, text_reg, text_reg2 = self.cameras_avaliable()

        self.aaLabel = Label(self.dataFrame, text=cameras_text, font=mini_font)
        self.aaLabel.grid(column=0, row=0, ipady=0, sticky=NW)

        self.aaLabel = Label(self.dataFrame, text=text_reg, font=mini_font)
        self.aaLabel.grid(column=1, row=0, ipady=0, ipadx=40, sticky=NW)

        if cameras_text2:
            self.aaLabel = Label(self.dataFrame, text=cameras_text2, font=mini_font)
            self.aaLabel.grid(column=2, row=0, sticky=NW)

            self.aaLabel = Label(self.dataFrame, text=text_reg2, font=mini_font)
            self.aaLabel.grid(column=3, row=0, ipadx=40, sticky=NW)
        

    def destroy_avaliable_cameras(self):
        for widget in self.dataFrame.grid_slaves():
            widget.config(text="")

    
    def cameras_avaliable(self):
        text = "Cameras avaliable:\n\n\n"
        text2 = "\n\n\n"
        text_reg ="\n\n\n"
        text_reg2 = "\n\n\n"

        with open(db,"r",encoding="utf-8") as file:
            data = json.load(file)
            cameras = data["db"]["cameras"]
            places = data["db"]["places"]
            registrations = data["db"]["cars"]["registrations"]
            car_camera = data["db"]["cars"]["camera"]
        
        cameras_and_places = []

        for camera_place in zip(places, cameras):
            cameras_and_places.append(camera_place)

        cameras_and_places.sort()

        for idx, camera_place in enumerate(cameras_and_places):
            cars_text = ""
            if camera_place[1] in car_camera:
                car_idxs = [i for i,x in enumerate(car_camera) if x == camera_place[1]]
                for car_idx in car_idxs:
                    cars_text = cars_text + f"[ {registrations[int(car_idx)]} ]"

            if idx <=10: 
                text = text + f"{camera_place[0]} - {camera_place[1]}:\n\n"
                text_reg = text_reg + f"{cars_text}\n\n"
            elif idx > 10 and idx <=19:
                text2 = text2 + f"{camera_place[0]} - {camera_place[1]}:\n\n" 
                text_reg2 = text_reg2 + f"{cars_text}\n\n"
            else: pass 
        return text, text2, text_reg, text_reg2


    def cameras_autorefresh(self):
        self.destroy_avaliable_cameras()
        self.cameras_pack_function()

        self.tk_config.after(10000, self.cameras_autorefresh)


    def add_camera_function(self):
        print("Adding....")
        camera_id = self.AddID.get()
        camera_place = self.Addplace.get()

        check = self.check_if_not_empty((camera_id, camera_place))
        
        if check:
            with open(db, "r", encoding="utf-8") as file:
                data = json.load(file)
                c_cameras = data["db"]["cameras"]
                c_cameras.append(camera_id)
                data["db"]["cameras"] = c_cameras #to do

                c_places = data["db"]["places"]
                c_places.append(camera_place)
                data["db"]["places"] = c_places

            with open(db, "w") as file:
                json.dump(data, file, ensure_ascii=False, indent=4) 

            self.destroy_avaliable_cameras()
            self.cameras_pack_function()

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
                c_places = data["db"]["places"]
                if old_camera_id in c_cameras:
                    idx = c_cameras.index(old_camera_id)

                    c_cameras[idx] = new_camera_id
                    data["db"]["cameras"] = c_cameras

                    c_places[idx] = new_camera_place
                    data["db"]["places"] = c_places

                    with open(db, "w", encoding="utf-8") as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)
                    
                    self.destroy_avaliable_cameras()
                    self.cameras_pack_function()

                else:
                    answer = messagebox.showinfo("Error", f"Camera {old_camera_id} not found")

    def delete_camera_function(self):
        print("Deleting....")

        camera_id = self.DelID.get()    

        check = self.check_if_not_empty(camera_id)
        if check:
            with open(db, "r", encoding="utf-8") as file:
                data = json.load(file)
                c_cameras = data["db"]["cameras"]
                c_places = data["db"]["places"]
                if camera_id in c_cameras:
                    idx = c_cameras.index(camera_id)
                    c_cameras.pop(idx)
                    c_places.pop(idx)

                with open(db, "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
            
            self.destroy_avaliable_cameras()
            self.cameras_pack_function()
        else:
            answer = messagebox,messagebox.showinfo("Error", f"Camera {camera_id} not found")

        

    @staticmethod    
    def check_if_not_empty(values):
        for value in values:
            if value: pass 
            else:
                answer = messagebox.showinfo("Error", "Fields can't be empty")
                return False 
        return True 