import tkinter
from dataclasses import dataclass
import customtkinter as ctk


@dataclass
class Affichage:
    method: str
    widget: ctk.CTkBaseClass

    px: int | tuple[int, int] = 10
    py: int | tuple[int, int] = 10
    ipx: int | tuple[int, int] = 0
    ipy: int | tuple[int, int] = 0
    side: str = tkinter.TOP

    row: int = 0
    column: int = 0
    columnspan: int = 1

    x: int = 0
    y: int = 0

    def __post_init__(self):
        self.afficher()

    def afficher(self):
        if self.method == "pack":
            self.widget.pack(ipadx=self.ipx,
                             ipady=self.ipy,
                             padx=self.px,
                             pady=self.py,
                             side=self.side)

        elif self.method == "grid":
            self.widget.grid(ipadx=self.ipx,
                             ipady=self.ipy,
                             padx=self.px,
                             pady=self.py,
                             row=self.row,
                             column=self.column,
                             columnspan=self.columnspan)

        elif self.method == "place":
            self.widget.grid(ipadx=self.ipx,
                             ipady=self.ipy,
                             x=self.x,
                             y=self.y)
