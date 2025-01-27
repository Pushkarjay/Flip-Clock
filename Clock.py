import customtkinter as ctk
import time
from datetime import datetime


class FlipClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flip Clock")
        self.root.geometry("400x300")
        ctk.set_appearance_mode("dark")  # Dark mode

        # Fonts
        self.time_font = ("Helvetica", 48, "bold")
        self.date_font = ("Helvetica", 14)

        # Create UI
        self.time_label = ctk.CTkLabel(root, text="", font=self.time_font)
        self.time_label.pack(pady=20)

        self.date_label = ctk.CTkLabel(root, text="", font=self.date_font)
        self.date_label.pack()

        # Update time every second
        self.update_clock()

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")  # Hour:Minute:Second
        current_date = datetime.now().strftime("%A, %B %d, %Y")  # Full date

        self.time_label.configure(text=current_time)
        self.date_label.configure(text=current_date)

        # Update every 1000ms (1 second)
        self.root.after(1000, self.update_clock)


# Create the app
app = ctk.CTk()
flip_clock = FlipClockApp(app)
app.mainloop()
