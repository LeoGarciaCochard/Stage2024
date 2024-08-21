import tkinter
from dataclasses import dataclass
import customtkinter as ctk


@dataclass
class Entry:
    master: ctk.CTk

    placeholder: str = ''
    police: int = 15
    font: str = 'Helvetica'
    style: str = "normal"
    bg: str = "#2b2b2b"
    px: int | tuple[int, int] = 10
    py: int | tuple[int, int] = 10
    ipx: int | tuple[int, int] = 0
    ipy: int | tuple[int, int] = 0
    width: int = 150
    height: int = 30
    side: str = tkinter.TOP

    row: int = 0
    column: int = 0
    columnspan: int = 1

    entry = None

    def __post_init__(self):
        self.create()

    def create(self):
        self.entry = ctk.CTkEntry(master=self.master,
                                  placeholder_text=self.placeholder,
                                  width=self.width,
                                  height=self.height,
                                  font=(self.font, self.police, self.style))

    def get(self):
        return self.entry.get()

    def afficher(self):
        self.entry.pack(ipadx=self.ipx,
                        ipady=self.ipy,
                        padx=self.px,
                        pady=self.py,
                        side=self.side)
    def fixer(self):
        self.entry.grid(ipadx=self.ipx,
                        ipady=self.ipy,
                        padx=self.px,
                        pady=self.py,
                        row=self.row,
                        column=self.column,
                        columnspan=self.columnspan)

    def cacher(self):
        self.entry.pack_forget()

    def destroy(self):
        self.entry.destroy()
