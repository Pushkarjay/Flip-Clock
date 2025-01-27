import customtkinter as ctk
from tkinter import colorchooser, Menu
import time
from datetime import datetime


class FlipClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flip Clock")
        self.root.geometry("800x500")  # Initial window size
        self.fullscreen = False
        self.theme = "dark"  # Default theme
        self.time_color = "white"
        self.date_color = "grey"
        self.time_font_size = 80
        self.date_font_size = 20

        # Set appearance mode
        ctk.set_appearance_mode("dark")

        # Create labels
        self.time_label = ctk.CTkLabel(root, text="", font=("Helvetica", self.time_font_size, "bold"), text_color=self.time_color)
        self.time_label.place(relx=0.5, rely=0.4, anchor="center")

        self.date_label = ctk.CTkLabel(root, text="", font=("Helvetica", self.date_font_size), text_color=self.date_color)
        self.date_label.place(relx=0.5, rely=0.6, anchor="center")

        # Add menu
        self.create_menu()

        # Update clock
        self.update_clock()

    def create_menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        # Settings Menu
        settings_menu = Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="Toggle Fullscreen", command=self.toggle_fullscreen)
        settings_menu.add_separator()
        settings_menu.add_command(label="Change Time Color", command=self.change_time_color)
        settings_menu.add_command(label="Change Date Color", command=self.change_date_color)
        settings_menu.add_separator()
        settings_menu.add_command(label="Increase Time Font Size", command=lambda: self.adjust_font("time", "increase"))
        settings_menu.add_command(label="Decrease Time Font Size", command=lambda: self.adjust_font("time", "decrease"))
        settings_menu.add_command(label="Increase Date Font Size", command=lambda: self.adjust_font("date", "increase"))
        settings_menu.add_command(label="Decrease Date Font Size", command=lambda: self.adjust_font("date", "decrease"))
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        # Theme Menu
        theme_menu = Menu(menu_bar, tearoff=0)
        theme_menu.add_command(label="Dark Theme", command=lambda: self.change_theme("dark"))
        theme_menu.add_command(label="Light Theme", command=lambda: self.change_theme("light"))
        menu_bar.add_cascade(label="Theme", menu=theme_menu)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def change_time_color(self):
        color = colorchooser.askcolor(title="Choose Time Color")[1]
        if color:
            self.time_color = color
            self.time_label.configure(text_color=self.time_color)

    def change_date_color(self):
        color = colorchooser.askcolor(title="Choose Date Color")[1]
        if color:
            self.date_color = color
            self.date_label.configure(text_color=self.date_color)

    def adjust_font(self, label, action):
        if label == "time":
            if action == "increase":
                self.time_font_size += 5
            elif action == "decrease" and self.time_font_size > 20:
                self.time_font_size -= 5
            self.time_label.configure(font=("Helvetica", self.time_font_size, "bold"))
        elif label == "date":
            if action == "increase":
                self.date_font_size += 2
            elif action == "decrease" and self.date_font_size > 10:
                self.date_font_size -= 2
            self.date_label.configure(font=("Helvetica", self.date_font_size))

    def change_theme(self, theme):
        self.theme = theme
        if theme == "dark":
            ctk.set_appearance_mode("dark")
            self.time_label.configure(text_color=self.time_color or "white")
            self.date_label.configure(text_color=self.date_color or "grey")
        elif theme == "light":
            ctk.set_appearance_mode("light")
            self.time_label.configure(text_color=self.time_color or "black")
            self.date_label.configure(text_color=self.date_color or "black")

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")  # Hour:Minute:Second
        current_date = datetime.now().strftime("%A, %B %d, %Y")  # Full date

        self.time_label.configure(text=current_time)
        self.date_label.configure(text=current_date)

        # Update every 1000ms (1 second)
        self.root.after(1000, self.update_clock)


# Run the app
app = ctk.CTk()
flip_clock = FlipClockApp(app)
app.mainloop()
