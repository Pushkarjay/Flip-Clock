import customtkinter as ctk
from tkinter import colorchooser, Menu, simpledialog, filedialog, Toplevel
from tkinter import font as tkfont
from PIL import Image, ImageTk
import time
from datetime import datetime
import os


class FlipClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flip Clock")
        self.root.geometry("800x500")
        self.fullscreen = True

        # Default settings
        self.theme = "dark"
        self.time_color = "white"
        self.date_color = "grey"
        self.bg_color = "#000000"
        self.time_font_size = 300
        self.date_font_size = 20
        self.time_font = "Helvetica"
        self.date_font = "Helvetica"
        self.background_type = "solid"
        self.background_color = "#000001"
        self.background_image = None
        self.display_time = True
        self.display_date = True
        self.show_seconds = True
        self.time_format = "%H:%M:%S"
        self.date_format = "%A, %B %d, %Y"
        self.clock_style = "normal"
        self.sound_enabled = True
        self.tik_sound = False
        self.hourly_chime = False
        self.slogan = "Hello World"
        self.slogan_enabled = False
        self.prevent_sleep = True
        self.anti_burn_effect = True
        self.show_battery = True
        self.new_year_effect = False
        self.padding_hours = False

        ctk.set_appearance_mode(self.theme)

        # Create labels
        self.time_label = ctk.CTkLabel(
            root,
            text="",
            font=(self.time_font, self.time_font_size, "bold"),
            text_color=self.time_color,
        )
        self.time_label.place(relx=0.5, rely=0.4, anchor="center")

        self.date_label = ctk.CTkLabel(
            root,
            text="",
            font=(self.date_font, self.date_font_size),
            text_color=self.date_color,
        )
        self.date_label.place(relx=0.5, rely=0.6, anchor="center")

        self.slogan_label = ctk.CTkLabel(
            root,
            text=self.slogan,
            font=(self.time_font, 20),
            text_color=self.time_color,
        )
        self.slogan_label.place(relx=0.5, rely=0.8, anchor="center")
        self.slogan_label.place_forget()

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
        settings_menu.add_command(label="24-Hour Toggle", command=self.toggle_24_hour_format)
        settings_menu.add_command(label="Display Seconds Toggle", command=self.toggle_seconds)
        settings_menu.add_command(label="Padding 0 for Hours Toggle", command=self.toggle_padding_hours)
        settings_menu.add_separator()
        settings_menu.add_command(label="Anti-Screen Burn Effect", command=self.toggle_anti_burn)
        settings_menu.add_command(label="Prevent Screen Off & Sleep", command=self.toggle_prevent_sleep)
        settings_menu.add_command(label="Developer Info", command=self.show_contact_info)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        # Display Menu
        display_menu = Menu(menu_bar, tearoff=0)
        display_menu.add_command(label="Toggle Time Display", command=lambda: self.toggle_display("time"))
        display_menu.add_command(label="Toggle Date Display", command=lambda: self.toggle_display("date"))
        display_menu.add_command(label="Display Battery Status", command=self.toggle_battery_status)
        display_menu.add_separator()
        display_menu.add_command(label="Set Time Format", command=self.set_time_format)
        display_menu.add_command(label="Set Date Format", command=self.set_date_format)
        display_menu.add_separator()
        display_menu.add_command(label="New Year’s Fireworks Effect", command=self.toggle_new_year_effect)
        menu_bar.add_cascade(label="Display", menu=display_menu)

        # Font & Appearance Menu
        font_menu = Menu(menu_bar, tearoff=0)
        font_menu.add_command(label="Change Time Font Size", command=self.change_time_font_size)
        font_menu.add_command(label="Change Date Font Size", command=self.change_date_font_size)
        display_menu.add_separator()
        font_menu.add_command(label="Change Time Font Color", command=self.change_time_color)
        font_menu.add_command(label="Change Date Font Color", command=self.change_date_color)
        display_menu.add_separator()
        font_menu.add_command(label="Change Background Color", command=self.change_bg_color)
        font_menu.add_command(label="Set Background Image", command=self.set_bg_image)
        font_menu.add_command(label="Reset Background", command=self.reset_bg)
        menu_bar.add_cascade(label="Font & Appearance", menu=font_menu)

        # Sound Menu
        sound_menu = Menu(menu_bar, tearoff=0)
        sound_menu.add_command(label="Enable Tik Sound", command=self.toggle_tik_sound)
        sound_menu.add_command(label="Enable Hourly Voice Chime", command=self.toggle_hourly_chime)
        menu_bar.add_cascade(label="Sound", menu=sound_menu)

        # Slogan Menu
        slogan_menu = Menu(menu_bar, tearoff=0)
        slogan_menu.add_command(label="Toggle Slogan", command=self.toggle_slogan)
        slogan_menu.add_command(label="Set Custom Slogan", command=self.set_slogan)
        menu_bar.add_cascade(label="Slogan", menu=slogan_menu)

        # Theme Menu
        theme_menu = Menu(menu_bar, tearoff=0)
        theme_menu.add_command(label="Dark Theme", command=lambda: self.set_theme("dark"))
        theme_menu.add_command(label="Light Theme", command=lambda: self.set_theme("light"))
        menu_bar.add_cascade(label="Themes", menu=theme_menu)

    # Feature Toggles
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def toggle_24_hour_format(self):
        if "%I" in self.time_format:
            self.time_format = "%H:%M:%S" if self.show_seconds else "%H:%M"
        else:
            self.time_format = "%I:%M:%S %p" if self.show_seconds else "%I:%M %p"

    def toggle_seconds(self):
        self.show_seconds = not self.show_seconds
        self.time_format = (
            "%H:%M:%S" if self.show_seconds else "%H:%M"
        ) if "%H" in self.time_format else (
            "%I:%M:%S %p" if self.show_seconds else "%I:%M %p"
        )

    def toggle_padding_hours(self):
        self.padding_hours = not self.padding_hours

    def toggle_anti_burn(self):
        self.anti_burn_effect = not self.anti_burn_effect

    def toggle_prevent_sleep(self):
        self.prevent_sleep = not self.prevent_sleep
        if self.prevent_sleep:
            os.system("powercfg -change -monitor-timeout-ac 0")
        else:
            os.system("powercfg -change -monitor-timeout-ac 5")

    def toggle_battery_status(self):
        self.show_battery = not self.show_battery

    def toggle_new_year_effect(self):
        self.new_year_effect = not self.new_year_effect

    def toggle_tik_sound(self):
        self.tik_sound = not self.tik_sound

    def toggle_hourly_chime(self):
        self.hourly_chime = not self.hourly_chime

    def toggle_slogan(self):
        self.slogan_enabled = not self.slogan_enabled
        if self.slogan_enabled:
            self.slogan_label.place(relx=0.5, rely=0.8, anchor="center")
        else:
            self.slogan_label.place_forget()

    def set_slogan(self):
        slogan = simpledialog.askstring("Set Slogan", "Enter your custom slogan:")
        if slogan:
            self.slogan = slogan
            self.slogan_label.configure(text=self.slogan)

    # Font & Appearance Methods
    def change_time_font_size(self):
        size = simpledialog.askinteger("Time Font Size", "Enter font size for time:")
        if size:
            self.time_font_size = size
            self.time_label.configure(font=(self.time_font, self.time_font_size, "bold"))

    def change_date_font_size(self):
        size = simpledialog.askinteger("Date Font Size", "Enter font size for date:")
        if size:
            self.date_font_size = size
            self.date_label.configure(font=(self.date_font, self.date_font_size))

    def change_time_color(self):
        color = colorchooser.askcolor(title="Choose Time Font Color")[1]
        if color:
            self.time_color = color
            self.time_label.configure(text_color=color)

    def change_date_color(self):
        color = colorchooser.askcolor(title="Choose Date Font Color")[1]
        if color:
            self.date_color = color
            self.date_label.configure(text_color=color)

    def change_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.bg_color = color
            self.root.configure(bg=color)

    def set_bg_image(self):
        image_path = filedialog.askopenfilename(
            title="Select Background Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")],
        )
        if image_path:
            self.background_image = Image.open(image_path)
            self.background_image = ImageTk.PhotoImage(self.background_image)
            background_label = ctk.CTkLabel(self.root, image=self.background_image)
            background_label.place(relx=0.5, rely=0.5, anchor="center")

    def reset_bg(self):
        self.background_image = None
        self.root.configure(bg=self.bg_color)

    def set_time_format(self):
        format_choice = simpledialog.askstring("Set Time Format", "Enter Python strftime format for time:")
        if format_choice:
            self.time_format = format_choice

    def set_date_format(self):
        format_choice = simpledialog.askstring("Set Date Format", "Enter Python strftime format for date:")
        if format_choice:
            self.date_format = format_choice

    def set_theme(self, theme):
        self.theme = theme
        ctk.set_appearance_mode(theme)

    def show_contact_info(self):
        contact_popup = Toplevel(self.root)
        contact_popup.title("Contact Information")
        contact_popup.geometry("300x150")

        ctk.CTkLabel(
            contact_popup,
            text="Developer: Pushkarjay Ajay",
            font=("Helvetica", 14),
        ).pack(pady=10)

        ctk.CTkLabel(
            contact_popup,
            text="Email: pushkarjay.ajay1@gmail.com",
            font=("Helvetica", 12),
        ).pack(pady=5)

        ctk.CTkLabel(
            contact_popup,
            text="LinkedIn: linkedin.com/in/pushkarjay",
            font=("Helvetica", 12),
        ).pack(pady=5)

        close_button = ctk.CTkButton(contact_popup, text="Close", command=contact_popup.destroy)
        close_button.pack(pady=10)

    def toggle_display(self, element):
        if element == "time":
            self.display_time = not self.display_time
            self.time_label.place_forget() if not self.display_time else self.time_label.place(relx=0.5, rely=0.4, anchor="center")
        elif element == "date":
            self.display_date = not self.display_date
            self.date_label.place_forget() if not self.display_date else self.date_label.place(relx=0.5, rely=0.6, anchor="center")

    def update_clock(self):
        current_time = datetime.now().strftime(self.time_format)
        current_date = datetime.now().strftime(self.date_format)

        if self.display_time:
            self.time_label.configure(text=current_time.zfill(8 if self.padding_hours else 0))
        if self.display_date:
            self.date_label.configure(text=current_date)

        self.root.after(1000, self.update_clock)


# Run the app
app = ctk.CTk()
flip_clock = FlipClockApp(app)
app.mainloop()
