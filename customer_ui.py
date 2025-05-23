import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
from ownercode import CustomerAgree

class CustomerUI:
    def __init__(self, root, car_data):
        self.root = root
        self.car_data = car_data
        self.car_window = None

    def show_car_listings(self, refresh=False):
        def rent_car(car_id, car_name):
            date_window = tk.Toplevel(self.root)
            date_window.title("Select Rental Dates")
            date_window.geometry("400x600")
            date_window.grab_set()

            tk.Label(date_window, text=f"Rent: {car_name}", font=('Arial', 12, 'bold')).pack(pady=10)
            tk.Label(date_window, text="Start Date:").pack()
            start_cal = Calendar(date_window, date_pattern='yyyy-mm-dd')
            start_cal.pack(pady=5)

            tk.Label(date_window, text="End Date:").pack()
            end_cal = Calendar(date_window, date_pattern='yyyy-mm-dd')
            end_cal.pack(pady=5)

            def confirm_dates():
                start_date = start_cal.get_date()
                end_date = end_cal.get_date()

                try:
                    fmt = "%Y-%m-%d"
                    start = datetime.strptime(start_date, fmt)
                    end = datetime.strptime(end_date, fmt)

                    if start > end:
                        messagebox.showwarning("Date Error", "End date must be after start date.")
                        return

                    total_days = (end - start).days
                    self.car_data.set_booking(car_id, start_date, end_date)

                    CustomerAgree(int(car_id), start_date, end_date)

                    messagebox.showinfo("Booking Confirmed", f"You booked {car_name} for {total_days} days.")
                    date_window.destroy()

                except ValueError:
                    messagebox.showerror("Format Error", "Invalid date format.")

            tk.Button(date_window, text="Confirm", command=confirm_dates, bg="#007acc", fg="white").pack(pady=10)

        if self.car_window and self.car_window.winfo_exists():
            self.car_window.destroy()

        self.car_window = tk.Toplevel(self.root)
        self.car_window.title("Car Detail Page")
        self.car_window.geometry("600x600")
        self.car_window.configure(bg='#f0f4f7')

        header = tk.Label(
            self.car_window,
            text="Available Car Listings",
            font=('Helvetica', 18, 'bold'),
            fg='#0a3d62',
            bg='#f0f4f7'
        )
        header.pack(pady=10)

        outer_frame = tk.Frame(self.car_window)
        outer_frame.pack(fill='both', expand=True, padx=10, pady=5)

        canvas = tk.Canvas(outer_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scroll_frame = tk.Frame(canvas, bg='white')

        def resize_scroll_frame(event):
            canvas.itemconfig("window_frame", width=event.width)

        window_frame = canvas.create_window((0, 0), window=scroll_frame, anchor="nw", tags="window_frame")
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", resize_scroll_frame)

        for widget in scroll_frame.winfo_children():
            widget.destroy()

        for car in self.car_data.get_cars():
            is_available = car['Availability'] == 'Available'
            bg_color = '#dff9fb' if is_available else '#f8d7da'
            text_color = '#27ae60' if is_available else '#c0392b'

            car_frame = tk.Frame(scroll_frame, bg=bg_color, bd=1, relief='ridge')
            car_frame.pack(fill='x', padx=20, pady=10)

            booking = car.get("Booking")
            booking_text = f"\nBooked: {booking['Start']} → {booking['End']}" if booking else ""

            car_info = (
                f"Car ID: {car['ID']}\n"
                f"Model: {car['Name']}\n"
                f"Price: {car['Price']}\n"
                f"Status: {car['Availability']}" + booking_text
            )

            label = tk.Label(
                car_frame,
                text=car_info,
                font=('Arial', 12),
                bg=bg_color,
                fg=text_color,
                justify='left',
                anchor='w'
            )
            label.pack(fill='x', padx=15, pady=(10, 5))

            if is_available:
                rent_button = tk.Button(
                    car_frame,
                    text="Rent",
                    bg='#2980b9',
                    fg='white',
                    font=('Arial', 11, 'bold'),
                    width=10,
                    command=lambda c=car: rent_car(c['ID'], c['Name'])
                )
                rent_button.pack(anchor='w', padx=15, pady=(0, 10))

        # Refresh and Close buttons
        refresh_button = tk.Button(
            self.car_window,
            text="Refresh",
            command=lambda: self.show_car_listings(refresh=True),
            bg='#3498db',
            fg='white',
            font=('Arial', 12, 'bold'),
            width=10
        )
        refresh_button.pack(pady=5)

        close_button = tk.Button(
            self.car_window,
            text="Close",
            command=self.car_window.destroy,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 12, 'bold'),
            width=10
        )
        close_button.pack(pady=5)
