from tkinter import Toplevel
import customtkinter as ctk


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.screen_width = widget.winfo_screenwidth()
        self.wraplength = 750

        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.widget.bind("<Motion>", self.move_tooltip)

    def show_tooltip(self, event):
        if self.tooltip_window:
            return
        x, y = event.widget.winfo_pointerxy()
        self.tooltip_window = Toplevel(event.widget)
        self.tooltip_window.wm_overrideredirect(True)

        frame = ctk.CTkFrame(self.tooltip_window, fg_color=None)
        frame.pack()
        label = ctk.CTkLabel(frame, text=self.text, text_color="white", fg_color="black", wraplength=self.wraplength)
        label.pack(ipady=5, ipadx=5)

        self.tooltip_window.update_idletasks()
        tooltip_width = self.tooltip_window.winfo_width()

        if x < self.screen_width / 2:
            self.tooltip_window.wm_geometry(f"+{x + 20}+{y + 20}")
        else:
            self.tooltip_window.wm_geometry(f"+{x - tooltip_width - 20}+{y + 20}")

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def move_tooltip(self, event):
        if self.tooltip_window:
            x, y = event.widget.winfo_pointerxy()
            tooltip_width = self.tooltip_window.winfo_width()

            if x <= self.screen_width // 2:
                self.tooltip_window.wm_geometry(f"+{x + 20}+{y + 20}")
            else:
                self.tooltip_window.wm_geometry(f"+{x - tooltip_width - 20}+{y + 20}")
