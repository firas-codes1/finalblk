import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
#from blockchain import Blockchain
#from car_sharing import Owner, Car, Customer
from customer_ui import CustomerUI
from owner_ui import OwnerUI
from car_data import CarData
from deploycontract import deploy_contract
from makecar import makeCar

class CarSharingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Car Sharing")
        deploy_contract()
        makeCar(price=4)
        #self.blockchain = Blockchain()
        #self.customer = Customer(500)
        #s#elf.owner = Owner(500)

        self.car_data = CarData()
        self.customer_ui = CustomerUI(self.root, self.car_data)
        self.owner_ui = OwnerUI(self.root, self.car_data)

        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.add_background_image()
        self.create_widgets()

    def add_background_image(self):
        import os
        cwd = os.getcwd()
        image = Image.open(cwd+"/img_1.png")
        image = image.resize((800, 600))
        self.bg_image = ImageTk.PhotoImage(image)
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_widgets(self):
        overlay = tk.Frame(self.root, bg='white')
        overlay.place(relx=0.5, rely=0.5, anchor='center', width=500, height=400)

        title_label = tk.Label(
            overlay,
            text="Car Sharing on Blockchain",
            font=('Helvetica', 20, 'bold'),
            bg='white',
            fg='#333'
        )
        title_label.pack(pady=(30, 40))

        button_frame = tk.Frame(overlay, bg='white')
        button_frame.pack()

        customer_button = tk.Button(
            button_frame,
            text="Customer",
            command=self.customer_interface,
            width=20,
            height=2,
            font=('Helvetica', 14),
            bg='#007acc',
            fg='white',
            bd=0,
            activebackground='#005f99'
        )
        customer_button.pack(pady=15)

        owner_button = tk.Button(
            button_frame,
            text="Owner",
            command=self.owner_interface,
            width=20,
            height=2,
            font=('Helvetica', 14),
            bg='#007acc',
            fg='white',
            bd=0,
            activebackground='#005f99'
        )
        owner_button.pack(pady=15)

    def customer_interface(self):
        self.customer_ui.show_car_listings()

    def owner_interface(self):
        self.owner_ui.show_car_editor()

if __name__ == "__main__":
    root = tk.Tk()
    app = CarSharingApp(root)
    root.mainloop()
