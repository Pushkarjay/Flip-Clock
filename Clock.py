import customtkinter as ctk
from tkinter import colorchooser, Menu, simpledialog, filedialog, messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk
from datetime import datetime


class FlipClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flip Clock")
        self.root.geometry("800x500")
        self.fullscreen = False

        # Default settings
        self.theme = "dark"
        self.time_color = "white"
        self.date_color = "grey"
        self.time_font_size = 300
        self.date_font_size = 20
        self.time_font = "Helvetica"
        self.date_font = "Helvetica"
        self.background_type = "solid"  # Options: solid, image
        self.background_color = "#000000"
        self.background_image = None
        self.display_time = True
        self.display_date = True
        self.time_format = "%H:%M:%S"
        self.date_format = "%A, %B %d, %Y"
        self.clock_style = "normal"  # Options: flip, normal, digital, analog
        self.sound_enabled = True

        ctk.set_appearance_mode("dark")

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

        # Developer label
        self.developer_label = ctk.CTkLabel(
            root,
            text="Developer: Pushkarjay Ajay",
            font=("Helvetica", 12),
            text_color="white",
        )
        self.developer_label.place(relx=0.95, rely=0.02, anchor="ne")
        self.developer_label.bind("<Button-1>", self.show_developer_info)

        # Add menu
        self.create_menu()

        # Update clock
        self.update_clock()

        # Bind the Esc key to exit fullscreen
        self.root.bind("<Escape>", self.exit_fullscreen)

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
        settings_menu.add_command(label="Set Time Font", command=lambda: self.set_font("time"))
        settings_menu.add_command(label="Set Date Font", command=lambda: self.set_font("date"))
        settings_menu.add_command(label="Set Time Font Size", command=lambda: self.set_font_size("time"))
        settings_menu.add_command(label="Set Date Font Size", command=lambda: self.set_font_size("date"))
        settings_menu.add_separator()
        settings_menu.add_command(label="Set Background Color", command=self.set_background_color)
        settings_menu.add_command(label="Set Background Image", command=self.set_background_image)
        settings_menu.add_command(label="Set Background Opacity", command=self.set_background_opacity)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        # Display Menu
        display_menu = Menu(menu_bar, tearoff=0)
        display_menu.add_command(label="Toggle Time Display", command=lambda: self.toggle_display("time"))
        display_menu.add_command(label="Toggle Date Display", command=lambda: self.toggle_display("date"))
        display_menu.add_separator()
        display_menu.add_command(label="Set Time Format", command=self.set_time_format)
        display_menu.add_command(label="Set Date Format", command=self.set_date_format)
        menu_bar.add_cascade(label="Display", menu=display_menu)

        # Theme Menu
        theme_menu = Menu(menu_bar, tearoff=0)
        theme_menu.add_command(label="Dark Theme", command=lambda: self.change_theme("dark"))
        theme_menu.add_command(label="Light Theme", command=lambda: self.change_theme("light"))
        theme_menu.add_command(label="Customize Theme", command=self.customize_theme)
        menu_bar.add_cascade(label="Theme", menu=theme_menu)

        # Clock Style Menu
        style_menu = Menu(menu_bar, tearoff=0)
        style_menu.add_command(label="Flip Style", command=lambda: self.set_clock_style("flip"))
        style_menu.add_command(label="Normal Style", command=lambda: self.set_clock_style("normal"))
        style_menu.add_command(label="Digital Style", command=lambda: self.set_clock_style("digital"))
        style_menu.add_command(label="Analog Style", command=lambda: self.set_clock_style("analog"))
        menu_bar.add_cascade(label="Clock Style", menu=style_menu)

        # Sound Menu
        sound_menu = Menu(menu_bar, tearoff=0)
        sound_menu.add_command(label="Enable Flip Sound", command=lambda: self.toggle_sound(True))
        sound_menu.add_command(label="Disable Flip Sound", command=lambda: self.toggle_sound(False))
        menu_bar.add_cascade(label="Sound", menu=sound_menu)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

        if self.fullscreen:
            self.developer_label.place_forget()  # Hide developer label
            self.root.config(menu=None)  # Hide menu
        else:
            self.developer_label.place(relx=0.95, rely=0.02, anchor="ne")  # Show developer label
            self.create_menu()  # Recreate menu

    def exit_fullscreen(self, event=None):
        if self.fullscreen:
            self.toggle_fullscreen()  # Toggle fullscreen off

    def show_developer_info(self, event):
        messagebox.showinfo("Developer Info", "Email: pushkarjay.ajay1@gmail.com\nLinkedIn: www.linkedin.com/in/pushkarjay")

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
                self.time_label.configure(font=(self.time_font, self.time_font_size, "bold"))
            elif label == "date":
                self.date_font_size = font_size
                self.date_label.configure(font=(self.date_font, self.date_font_size))

    def set_font(self, label):
        available_fonts = tkfont.families()
        font_choice = simpledialog.askstring("Set Font", f"Choose font for {label} from available options:\n{', '.join(available_fonts)}")
        if font_choice in available_fonts:
            if label == "time":
                self.time_font = font_choice
                self.time_label.configure(font=(self.time_font, self.time_font_size, "bold"))
            elif label == "date":
                self.date_font = font_choice
                self.date_label.configure(font=(self.date_font, self.date_font_size))

    def set_background_color(self):
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.background_type = "solid"
            self.background_color = color
            self.root.configure(bg=self.background_color)

    def set_background_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.gif")])
        if file_path:
            self.background_type = "image"
            image = Image.open(file_path).resize((self.root.winfo_width(), self.root.winfo_height()))
            self.background_image = ImageTk.PhotoImage(image)
            bg_label = ctk.CTkLabel(self.root, image=self.background_image)
            bg_label.place(relx=0.5, rely=0.5, anchor="center")

    def set_background_opacity(self):
        opacity = simpledialog.askfloat("Set Background Opacity", "Enter opacity (0.0 to 1.0):")
        if opacity is not None and 0.0 <= opacity <= 1.0:
            # Placeholder for actual opacity setting logic
            pass

    def customize_theme(self):
        options = [
            "Background Color",
            "Time Color",
            "Date Color",
        ]
        choice = simpledialog.askstring(
            "Customize Theme",
            f"Choose what to customize:\n{', '.join(options)}",
        )

        if choice == "Background Color":
            self.set_background_color()
        elif choice == "Time Color":
            self.change_time_color()
        elif choice == "Date Color":
            self.change_date_color()
        else:
            ctk.CTkMessageBox(title="Invalid Choice", message="Option not recognized.")

    def toggle_display(self, element):
        if element == "time":
            self.display_time = not self.display_time
            self.time_label.place_forget() if not self.display_time else self.time_label.place(relx=0.5, rely=0.4, anchor="center")
        elif element == "date":
            self.display_date = not self.display_date
            self.date_label.place_forget() if not self.display_date else self.date_label.place(relx=0.5, rely=0.6, anchor="center")

    def set_time_format(self):
        format_choice = simpledialog.askstring("Set Time Format", "Enter Python strftime format for time:")
        if format_choice:
            self.time_format = format_choice

    def set_date_format(self):
        format_choice = simpledialog.askstring("Set Date Format", "Enter Python strftime format for date:")
        if format_choice:
            self.date_format = format_choice

    def set_clock_style(self, style):
        self.clock_style = style
        # Placeholder for implementing different clock styles
        pass

    def toggle_sound(self, enable):
        self.sound_enabled = enable

    def update_clock(self):
        current_time = datetime.now().strftime(self.time_format)
        current_date = datetime.now().strftime(self.date_format)

        if self.display_time:
            self.time_label.configure(text=current_time)
        if self.display_date:
            self.date_label.configure(text=current_date)

        # Flip sound logic (placeholder)
        if self.sound_enabled and self.clock_style == "flip":
            pass  # Add flip sound logic here

        self.root.after(1000, self.update_clock)


# Run the app
app = ctk.CTk()
flip_clock = FlipClockApp(app)
app.mainloop()
