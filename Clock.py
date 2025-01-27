import customtkinter as ctk
import time
from datetime import datetime


class FlipClockApp:
    def __init__(self, root, time_font_size=60, date_font_size=16):
        self.root = root
        self.root.title("Flip Clock")
        self.root.geometry("600x400")  # Set initial size
        self.root.resizable(False, False)  # Disable resizing
        ctk.set_appearance_mode("dark")  # Dark mode

        # Fonts
        self.time_font = ("Helvetica", time_font_size, "bold")
        self.date_font = ("Helvetica", date_font_size)

        # Create UI
        self.time_label = ctk.CTkLabel(root, text="", font=self.time_font)
        self.time_label.place(relx=0.5, rely=0.4, anchor="center")  # Centered

        self.date_label = ctk.CTkLabel(root, text="", font=self.date_font)
        self.date_label.place(relx=0.5, rely=0.6, anchor="center")  # Below time

        # Update time every second
        self.update_clock()

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")  # Hour:Minute:Second
        current_date = datetime.now().strftime("%A, %B %d, %Y")  # Full date

        self.time_label.configure(text=current_time)
        self.date_label.configure(text=current_date)

        # Update every 1000ms (1 second)
        self.root.after(1000, self.update_clock)


# Customizable font sizes
TIME_FONT_SIZE = 80
DATE_FONT_SIZE = 20

# Create the app
app = ctk.CTk()
app.geometry("600x400")  # Window size
app.eval("tk::PlaceWindow . center")  # Center the window on the screen

flip_clock = FlipClockApp(app, time_font_size=TIME_FONT_SIZE, date_font_size=DATE_FONT_SIZE)
app.mainloop()
