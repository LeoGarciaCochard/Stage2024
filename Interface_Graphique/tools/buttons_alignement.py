import customtkinter as ctk
from dataclasses import dataclass

from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.tools.buttons import Button, ButtonImage
import Interface_Graphique.var_fonc.variables_path as paths


@dataclass
class BtnHelp:
    master: ctk.CTkFrame
    text_button: str
    text_help: str
    function: callable

    width: int = 200
    height: int = 30
    fg_color: str = "#2b2b2b"

    police: int = 15
    font: str = 'Helvetica'
    style: str = "normal"

    px= 0
    py= 0
    ipx = 0
    ipy= 0

    cadre = None
    button = None
    button_help = None

    def __post_init__(self):
        self.create()

        self.button.fixer()
        self.button_help.fixer()

    def create(self):

        self.cadre = Frame(master=self.master, fg_color=self.fg_color, ipx=self.ipx, ipy=self.ipy,
                           px=self.px, py=self.py)

        self.button = Button(master=self.cadre.frame, text=self.text_button, width=self.width, height=self.height,
                             function=self.function, police=self.police, font=self.font, style=self.style,
                             column=0, row=0)

        self.button_help = ButtonImage(master=self.cadre.frame, path=paths.img_aide, path_hover=paths.img_aide_hover,
                                       text_tooltip=self.text_help, column=1, row=0, tooltip=True,
                                       function=lambda: print(''))  # Pas de fonction
    def afficher(self):
        self.cadre.afficher()

    def cacher(self):
        self.cadre.cacher()


@dataclass
class AjoutRapide(BtnHelp):
    img_width: int = 55
    img_height: int = 55
    compound: str = "left"
    btn_ipx = 50
    def create(self):
        super().create()

        self.button = ButtonImage(master=self.cadre.frame, path=paths.img_btn, path_hover=paths.img_btn_hover,
                                  text_tooltip=self.text_help, column=0, row=0, tooltip=False, ipx=self.btn_ipx,
                                  function=self.function, text=self.text_button, compound= self.compound,
                                  width=self.img_width, height=self.img_height)

