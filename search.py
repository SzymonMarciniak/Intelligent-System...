from tkinter import *
import PIL.Image, PIL.ImageTk
import os

from AImain import detect_plate, get_registration_numbers

blue_color = "#4da6ff"
small_font = ('Verdana bold',28)
large_font = ('Verdana bold',35)
extralarge_font = ('Verdana bold',100)
class Search:
    def __init__(self, tk: LabelFrame, cancel_icon: PhotoImage) -> None:
        self.tk = tk
        self.cancel_icon = cancel_icon
       
    
    def exit_search(self):
        self.searchFrame.place_forget()
        self.tk.SearchIsOpen = False

    def main(self, car_registration, language, car_image, found_car_image):

        self.car_registration = car_registration
        self.found_car_image = found_car_image

        self.searchFrame = LabelFrame(self.tk, bd=5, bg="white", width=1300, height=650, highlightbackground=blue_color, background=blue_color)
        self.searchFrame.place(relx=0.5, rely=0.5, anchor=CENTER) 

        cancel_button = Button(self.searchFrame, image=self.cancel_icon, borderwidth=0, bg=blue_color, bd=0, highlightthickness=0, \
            activebackground=blue_color, command=self.exit_search)
        cancel_button.place(relx=0.95, rely=0)
        cancel_button.image = self.cancel_icon

        self.textLabel = Label(self.searchFrame, text=f"Searching: {car_registration}", bg=blue_color, font=large_font)
        self.textLabel.place(relx=0.35, rely=0.1)

        self.car_image_label = Label(self.searchFrame, image=car_image, borderwidth=0, bg="gray", bd=0)
        self.car_image_label.place(relx=0.05, rely=0.23)

        self.car_location_text = Label(self.searchFrame, text="Your car location: ", bg=blue_color, font=large_font)
        self.car_location_text.place(relx=0.62, rely=0.23)

        self.car_location = Label(self.searchFrame, text="B3", bg=blue_color, font=extralarge_font, fg="green")
        self.car_location.place(relx=0.73, rely=0.37)

        self.confirm_button = Button(self.searchFrame, text="Thanks", borderwidth=2, bg="green", font=small_font, bd=2, highlightthickness=2, \
            activebackground="green", width=10, pady=11, command=self.exit_search)
        self.confirm_button.place(relx=0.7, rely=0.83)

        self.registration_checking(car_registration)

        if language == "en":
            self.english_language() 
        elif language == "pl":
            self.polish_language()
    
    def english_language(self):
        self.textLabel.config(text=f"Searching: {self.car_registration}")
        self.car_location_text.config(text="Your car location: ")
        self.car_location_text.place(relx=0.62, rely=0.23)
        self.confirm_button.config(text="Thanks")

    def polish_language(self):
        self.textLabel.config(text=f"Wyszukiwanie: {self.car_registration}") 
        self.car_location_text.config(text="Położenie Twojego auta:")
        self.car_location_text.place(relx=0.57, rely=0.23)
        self.confirm_button.config(text="Dziękuję")

    def registration_checking(self, car_registration):

        detection_threshold = 0.4
        region_treshold = 0.6
        text_threshold = 0.7

        images = ["402", "400", "412"]

        for car_nr in images:
            image_np_with_detections, detections, _ = detect_plate(car_number=car_nr)
            image = image_np_with_detections
            text, _ = get_registration_numbers(image, detections, detection_threshold, region_treshold, text_threshold)
            text = text[0].upper()
            if text == car_registration:
                break
            else:
                text=None

    
        if text:
            # from main import Main
            # main = Main(self.tk)

            print(f"Registration: {text} - SUCCESS")
            #image = main.car_image_search(car_nr)
          
            self.car_image_label.config(image=self.found_car_image)
        else:
            print(f"Registration {car_registration} no found")

