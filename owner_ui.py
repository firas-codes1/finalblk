import tkinter as tk
from tkinter import messagebox
from ownercode import OwnerAgree, CustomerPay
from datetime import datetime

class OwnerUI:
    def __init__(self, root, car_data):
        self.root = root
        self.car_data = car_data
        self.entries = []
        self.editor_window = None

    def show_car_editor(self):
        if self.editor_window and self.editor_window.winfo_exists():
            self.editor_window.destroy()

        self.entries.clear()
        cars = self.car_data.get_cars()

        self.editor_window = tk.Toplevel(self.root)
        self.editor_window.title("Manage Car Listings")
        self.editor_window.geometry("800x500")
        self.editor_window.configure(bg="#f9f9f9")
        self.editor_window.protocol("WM_DELETE_WINDOW", self.on_close_editor)

        header = tk.Label(self.editor_window, text="Edit Car Listings", font=('Helvetica', 18, 'bold'),fg='#2c3e50', bg="#f9f9f9")
        header.pack(pady=20)

        container = tk.Frame(self.editor_window, bg="#f9f9f9")
        container.pack(padx=20, fill="both", expand=True)

        tk.Label(container, text="ID", font=('Arial', 12, 'bold'), bg="#f9f9f9").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(container, text="Model", font=('Arial', 12, 'bold'), bg="#f9f9f9").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(container, text="Price", font=('Arial', 12, 'bold'), bg="#f9f9f9").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(container, text="Availability", font=('Arial', 12, 'bold'), bg="#f9f9f9").grid(row=0, column=3, padx=5, pady=5)
        tk.Label(container, text="Booking", font=('Arial', 12, 'bold'), bg="#f9f9f9").grid(row=0, column=4, padx=5, pady=5)

        for i, car in enumerate(cars):
            row = i + 1
            print(car)
            tk.Label(container, text=car["ID"], bg="#f9f9f9").grid(row=row, column=0, padx=5, pady=5)

            name_entry = tk.Label(container, text=car["Name"])
            #name_entry.insert(0, car["Name"])
            name_entry.grid(row=row, column=1, padx=5, pady=5)

            price_entry = tk.Label(container,text=car["Price"])
            #price_entry.insert(0, car["Price"])
            price_entry.grid(row=row, column=2, padx=5, pady=5)

            availability_var = tk.StringVar()
            availability_var.set(car["Availability"])
            tk.OptionMenu(container, availability_var, "Available", "Not Available").grid(row=row, column=3, padx=5, pady=5)

            booking = car.get("Booking")
            if booking:
                text = f"{booking['Start']} → {booking['End']}"
            else:
                text = "—"
            tk.Label(container, text=text, bg="#f9f9f9", fg="#c0392b").grid(row=row, column=4, padx=5, pady=5)



            try:
                def rentCar(car):
                    booking = car.get("Booking")
                    carid=car["ID"]
                    OwnerAgree(int(carid), booking["Start"], booking["End"])
                    fmt = "%Y-%m-%d"
                    start = datetime.strptime(booking["Start"], fmt)
                    end = datetime.strptime(booking["End"], fmt)
                    tdays=(end - start).days
                    amount=int(car["Price"])*int(tdays)
                    CustomerPay(amount)
                    print(("Payment done (UI) ", amount,))


                file=open("ownerrequest.txt","r")
                text=file.readlines()
                addr="Customer: "+text[0]
                total="Days to rent: "+text[1]
                tk.Label(container, text=addr, bg="#f9f9f9", fg="#c0392b").grid(row=row+1, column=1, padx=5, pady=5)
                tk.Label(container, text=total, bg="#f9f9f9", fg="#c0392b").grid(row=row+1, column=4, padx=5, pady=5)
                rent_btn = tk.Button(container, text="Rent!", bg="#27ae60", fg="white",
                font=('Arial', 12, 'bold'), command=lambda: rentCar(car) ).grid(row=row+1, column=5, padx=5, pady=5)                
            except:
                text="No bookings"


            self.entries.append({
                "ID": car["ID"],
                "Name": name_entry,
                "Price": price_entry,
                "Availability": availability_var
            })

        button_frame = tk.Frame(self.editor_window, bg="#f9f9f9")
        button_frame.pack(pady=15)

        save_btn = tk.Button(
            button_frame, text="Save Changes", bg="#27ae60", fg="white",
            font=('Arial', 12, 'bold'), command=self.save_changes
        )
        save_btn.grid(row=0, column=0, padx=10)

        refresh_btn = tk.Button(
            button_frame, text="Refresh", bg="#3498db", fg="white",
            font=('Arial', 12, 'bold'), command=self.show_car_editor
        )
        refresh_btn.grid(row=0, column=1, padx=10)

    def save_changes(self):
        updated_data = []
        for car_entry in self.entries:
            car_id = car_entry["ID"]
            availability = car_entry["Availability"].get()

            existing_car = next((c for c in self.car_data.get_cars() if c["ID"] == car_id), None)
            booking = existing_car.get("Booking") if existing_car else None

            if availability == "Available":
                booking = None

            updated_data.append({
                "ID": car_id,
                "Name": car_entry["Name"].get(),
                "Price": car_entry["Price"].get(),
                "Availability": availability,
                "Booking": booking
            })

        self.car_data.update_cars(updated_data)
        messagebox.showinfo("Success", "Car details updated successfully!")

    def on_close_editor(self):
        if self.editor_window:
            self.editor_window.destroy()
            self.editor_window = None
