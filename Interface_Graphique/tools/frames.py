import tkinter as tk
from dataclasses import dataclass

import customtkinter as ctk


@dataclass
class Frame:
    master: ctk.CTk
    fill: str | None = None
    expand: bool = False
    px: int | tuple[int, int] = 10
    py: int | tuple[int, int] = 10
    ipx: int | tuple[int, int] = 10
    ipy: int | tuple[int, int] = 10
    border_width: int = 0
    corner_radius: int = 5
    border_color: str = "#106a43"

    row: int = 0
    column: int = 0
    columnspan: int = 1

    frame = None

    def __post_init__(self):
        self.create()

    def create(self):
        self.frame = ctk.CTkFrame(master=self.master, border_width=self.border_width, corner_radius=self.corner_radius,
                                  border_color=self.border_color)

    def afficher(self):
        self.frame.pack(ipadx=self.ipx, ipady=self.ipy, padx=self.px, pady=self.py, expand=self.expand, fill=self.fill)

    def cacher(self):
        self.frame.pack_forget()

    def fixer(self):
        self.entry.grid(ipadx=self.ipx,
                        ipady=self.ipy,
                        padx=self.px,
                        pady=self.py,
                        row=self.row,
                        column=self.column,
                        columnspan=self.columnspan)

    def destroy(self):
        self.frame.destroy()
