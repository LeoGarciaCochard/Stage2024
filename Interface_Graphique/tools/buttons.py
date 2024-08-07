from dataclasses import dataclass
import customtkinter as ctk
import tkinter as tk
from PIL import Image

from Interface_Graphique.tools.tooltips import Tooltip


@dataclass
class Button:

    master: ctk.CTkFrame
    text: str
    function: callable

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

    btn = None
    button = None

    def __post_init__(self):
        self.create()

    def create(self):
        self.button = ctk.CTkButton(master=self.master, text=self.text, command=self.function, width=self.width,
                                    height=self.height, font=(self.font, self.police, self.style))

    def afficher(self):
        self.button.pack(ipadx=self.ipx,
                         ipady=self.ipy,
                         padx=self.px,
                         pady=self.py,
                         side=self.side)

    def fixer(self):
        self.button.grid(ipadx=self.ipx,
                        ipady=self.ipy,
                        padx=self.px,
                        pady=self.py,
                        row=self.row,
                        column=self.column,
                        columnspan=self.columnspan)


    def cacher(self):
        self.button.pack_forget()


@dataclass
class ButtonQuitter:
    master: ctk.CTkFrame
    only_destroy: bool
    root: ctk.CTk

    btn = None

    def __post_init__(self):
        self.create()

    def arret_expe(self, acc=False):
        """
        Stop l'enregistrement et ferme l'application
        """
        if acc:
            self.root.destroy()
        else:

            if tout_complet():
                # arreterRecEEG() #TODO REMETTRE POUR REC INFO
                self.root.destroy()
            else:
                affiche_message_incomplet()

    def on_enter(self):
        if self.only_destroy:
            self.btn.configure(text="❌ Fermer")
        else:
            self.btn.configure(text="❌ Fermer et sauvegarder")

    def on_leave(self):
        self.btn.configure(text="❌")

    def create(self):

        self.btn = ctk.CTkButton(master=self.master, text="❌", width=15,
                                 command=lambda: self.arret_expe(self.only_destroy))
        self.btn.configure(fg_color="red", hover_color="white", text_color="black")
        self.btn.place(x=10, y=10)

        self.btn.bind("<Enter>", lambda x: self.on_enter())
        self.btn.bind("<Leave>", lambda x: self.on_leave())

@dataclass
class ButtonImage:
    master: ctk.CTkFrame
    path: str
    path_hover: str
    function: callable

    width: int = 25
    height: int = 25

    tooltip: bool = False
    text_tooltip: str = ''

    image = None
    image_resized = None
    photo = None
    image_hover = None
    image_hover_resized = None
    photo_hover = None
    button = None

    px: int | tuple[int, int] = 10
    py: int | tuple[int, int] = 10
    ipx: int | tuple[int, int] = 0
    ipy: int | tuple[int, int] = 0
    side: str = tk.TOP

    row: int = 0
    column: int = 0
    columnspan: int = 1

    def __post_init__(self):
        self.create()

    def create(self):
        self.image = Image.open(self.path)
        self.image_resized = self.image.resize((100, 100), Image.LANCZOS)
        self.photo = ctk.CTkImage(light_image=self.image_resized, dark_image=self.image_resized, size=(self.width, self.height))

        self.image_hover = Image.open(self.path_hover)
        self.image_hover_resized = self.image_hover.resize((100, 100), Image.LANCZOS)
        self.photo_hover = ctk.CTkImage(light_image=self.image_hover_resized, dark_image=self.image_hover_resized,
                                        size=(self.width, self.height))

        self.button = ctk.CTkLabel(master=self.master, image=self.photo, text=' ', cursor="hand2")

        self.button.bind("<Button-1>", self.function)
        self.button.bind("<Enter>", self.enter)
        self.button.bind("<Leave>", self.leave)

        if self.tooltip :
            Tooltip(self.button, self.text_tooltip)

    def enter(self, event):
        self.button.configure(image=self.photo)

    def leave(self, event):
        self.button.configure(image=self.photo_hover)

    def afficher(self):
        self.button.pack(ipadx=self.ipx,
                         ipady=self.ipy,
                         padx=self.px,
                         pady=self.py,
                         side=self.side)

    def fixer(self):
        self.button.grid(ipadx=self.ipx,
                         ipady=self.ipy,
                         padx=self.px,
                         pady=self.py,
                         row=self.row,
                         column=self.column,
                         columnspan=self.columnspan)


    def cacher(self):
        self.button.pack_forget()

