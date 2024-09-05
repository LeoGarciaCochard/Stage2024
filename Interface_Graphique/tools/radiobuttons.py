import tkinter as tk

import customtkinter as ctk
from dataclasses import dataclass

@dataclass
class RadioButton:

        master: ctk.CTkFrame
        text: str
        variable: tk.StringVar
        value: str | int

        px: int | tuple[int, int] = 10
        py: int | tuple[int, int] = 10
        ipx: int | tuple[int, int] = 0
        ipy: int | tuple[int, int] = 0
        side: str = tk.TOP
        police: int = 15
        font: str = 'Helvetica'
        style: str = "normal"

        row: int = 0
        column: int = 0
        columnspan: int = 1

        x: int = 0
        y: int = 0

        radio_button = None

        def __post_init__(self):
            self.create()

        def create(self):
            self.radio_button = ctk.CTkRadioButton(master=self.master, variable=self.variable, value=self.value,
                                                    text=self.text, font=(self.font, self.police, self.style))

        def afficher(self):
            self.radio_button.pack(ipadx=self.ipx,
                                   ipady=self.ipy,
                                   padx=self.px,
                                   pady=self.py,
                                   side=self.side)

        def cacher(self):
            self.radio_button.pack_forget()

        def fixer(self):
            self.radio_button.grid(ipadx=self.ipx,
                                   ipady=self.ipy,
                                   padx=self.px,
                                   pady=self.py,
                                   row=self.row,
                                   column=self.column,
                                   columnspan=self.columnspan)

        def unfix(self):
            self.radio_button.grid_forget()
