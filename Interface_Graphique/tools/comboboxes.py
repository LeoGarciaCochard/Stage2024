from dataclasses import dataclass
import customtkinter as ctk
import tkinter as tk
from typing import List
from Interface_Graphique.var_fonc.variables_info import *


@dataclass
class Combobox:

    master: ctk.CTkFrame
    values: List[str]
    variable_name: str

    state: str = "readonly"

    width: int = 200
    height: int = 30
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

    combobox = None



    def __post_init__(self):
        self.create()

    def actualiser(self, choix):

        dic_informations[self.variable_name] = choix

        self.combobox.set(choix)

    def create(self):
        self.combobox = ctk.CTkComboBox(master=self.master, state=self.state, values=self.values,
                                        command=self.actualiser, width=self.width, height=self.height,
                                        font=(self.font, self.police, self.style), cursor='hand2')

    def afficher(self):
        self.combobox.pack(ipadx=self.ipx,
                           ipady=self.ipy,
                           padx=self.px,
                           pady=self.py,
                           side=self.side)

    def fixer(self):
        self.combobox.grid(ipadx=self.ipx,
                           ipady=self.ipy,
                           padx=self.px,
                           pady=self.py,
                           row=self.row,
                           column=self.column,
                           columnspan=self.columnspan)

    def cacher(self):
        self.combobox.pack_forget()
