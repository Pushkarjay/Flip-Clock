import customtkinter as ctk
from tkinter import colorchooser, Menu, simpledialog
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
        settings_menu.add_command(label="Set Time Font Size", command=lambda: self.set_font_size("time"))
        settings_menu.add_command(label="Set Date Font Size", command=lambda: self.set_font_size("date"))
        settings_menu.add_command(label="Fit Window to Content", command=self.fit_window_to_content)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        # Theme Menu
        theme_menu = Menu(menu_bar, tearoff=0)
        theme_menu.add_command(label="Dark Theme", command=lambda: self.change_theme("dark"))
        theme_menu.add_command(label="Light Theme", command=lambda: self.change_theme("light"))
        menu_bar.add_cascade(label="Theme", menu=theme_menu)

        # Defaults Menu
        defaults_menu = Menu(menu_bar, tearoff=0)
        defaults_menu.add_command(label="Reset to Defaults", command=self.reset_to_defaults)
        menu_bar.add_cascade(label="Defaults", menu=defaults_menu)

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

    def set_font_size(self, label):
        font_size = simpledialog.askinteger("Set Font Size", f"Enter font size for {label}:")
        if font_size and font_size > 0:
            if label == "time":
                self.time_font_size = font_size
                self.time_label.configure(font=("Helvetica", self.time_font_size, "bold"))
            elif label == "date":
                self.date_font_size = font_size
                self.date_label.configure(font=("Helvetica", self.date_font_size))

    def fit_window_to_content(self):
        # Resize window to fit content dynamically
        self.root.update_idletasks()
        self.root.geometry(f"{self.time_font_size * 10}x{self.date_font_size * 10}")

    def change_theme(self, theme):
        self.theme = theme
        if theme == "dark":
            ctk.set_appearance_mode("dark")
            self.time_label.configure(text_color=self.time_color or "white")
            self.date_label.configure(text_color=self.date_color or "grey")
        elif theme == "light":
            ctk.set_appearance_mode("light")
            self.time_label.configure(text_color=self.time_color or "black")
            self.date_label.configure(text_color=self.date_color or "dimgray")

    def reset_to_defaults(self):
        # Reset all settings to defaults
        self.time_font_size = 80
        self.date_font_size = 20
        self.time_color = "white"
        self.date_color = "grey"
        self.theme = "dark"
        self.root.geometry("800x500")
        self.time_label.configure(font=("Helvetica", self.time_font_size, "bold"), text_color=self.time_color)
        self.date_label.configure(font=("Helvetica", self.date_font_size), text_color=self.date_color)
        self.change_theme("dark")

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
