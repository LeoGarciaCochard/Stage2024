from dataclasses import dataclass
import customtkinter as ctk


@dataclass
class Label:
    master: ctk.CTk
    text: str

    police: int = 15
    font: str = 'Helvetica'
    style: str = "normal"
    bg: str = "#2b2b2b"
    px: int | tuple[int, int] = 10
    py: int | tuple[int, int] = 10
    ipx: int | tuple[int, int] = 5
    ipy: int | tuple[int, int] = 5

    row: int = 0
    column: int = 0
    columnspan: int = 1

    label = None

    def __post_init__(self):
        self.create()

    def create(self):
        self.bg = self.master.cget('fg_color')
        self.label = ctk.CTkLabel(master=self.master,
                                  text=self.text,
                                  fg_color=self.bg,
                                  font=(self.font, self.police, self.style))

    def afficher(self):
        self.label.pack(ipadx=self.ipx,
                        ipady=self.ipy,
                        padx=self.px,
                        pady=self.py)

    def fixer(self):
        self.label.grid(ipadx=self.ipx,
                        ipady=self.ipy,
                        padx=self.px,
                        pady=self.py,
                        row=self.row,
                        column=self.column,
                        columnspan=self.columnspan)

    def cacher(self):
        self.label.pack_forget()
