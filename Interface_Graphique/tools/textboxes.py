import customtkinter as ctk
import tkinter as tk
from dataclasses import dataclass

@dataclass
class TextBox:
    master: ctk.CTkFrame
    placeholder: str |None = None

    width: int = 400
    height: int = 200

    border_spacing: int = 3
    corner_radius: int | None = None
    border_width: int | None = None

    scrollbar_button_color: str | tuple[str, str] | None = None
    scrollbar_button_hover_color: str | tuple[str, str] | None = None

    activate_scrollbars: bool = True

    police: int = 15
    font: str = 'Helvetica'
    style: str = "normal"

    fg_color: str | None = None
    bg_color: str = "transparent"

    px: int = 10
    py: int = 5
    ipx: int = 0
    ipy: int = 0
    side: str = tk.TOP

    row: int = 0
    column: int = 0
    columnspan: int = 1

    x: int = 0
    y: int = 0

    textbox = None

    def __post_init__(self):
        self.create()
        if self.placeholder != None:
            self.add_placeholder()

    def create(self):
        self.textbox = ctk.CTkTextbox(master=self.master, width=self.width, height=self.height,
                                      border_spacing=self.border_spacing, corner_radius=self.corner_radius, border_width=self.border_width,
                                      scrollbar_button_color=self.scrollbar_button_color, scrollbar_button_hover_color=self.scrollbar_button_hover_color,
                                      activate_scrollbars=self.activate_scrollbars, font=(self.font, self.police, self.style),
                                      fg_color=self.fg_color, bg_color=self.bg_color)

        if self.placeholder != None:
            self.textbox.bind("<FocusIn>", self.remove_placeholder)
            self.textbox.bind("<FocusOut>", self.add_placeholder)

    def add_placeholder(self,event=None):
        if self.textbox.get("1.0", "end-1c") == "":
            self.textbox.insert("1.0", self.placeholder)

    # Fonction pour retirer le placeholder
    def remove_placeholder(self, event=None):
        if self.textbox.get("1.0", "end-1c") == self.placeholder:
            self.textbox.delete("1.0", "end")

    def get_text(self):
        return self.textbox.get("1.0", "end-1c")

    def afficher(self):
        self.textbox.pack(ipadx=self.ipx,
                          ipady=self.ipy,
                          padx=self.px,
                          pady=self.py,
                          side=self.side)

