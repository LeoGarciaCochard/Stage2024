import customtkinter as ctk
from dataclasses import dataclass

from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.tools.labels import Label
from Interface_Graphique.tools.entries import Entry
from Interface_Graphique.tools.buttons import Button, ButtonImage
import Interface_Graphique.var_fonc.variables_path as paths
from Interface_Graphique.var_fonc.variables_pages import pages
from Interface_Graphique.var_fonc.variables_textes import dico_aide
from Interface_Graphique.var_fonc.functions import passer
from Interface_Graphique.var_fonc.recolte_donnes import stimulation

@dataclass
class BtnHelp:
    master: ctk.CTkFrame
    text_button: str
    text_help: str
    function: callable

    text_label_deroulement: str = "Entrez le texte à ajouter :"
    text_button_deroulement: str = "Valider"
    placeholder: str = "Entrez le texte ici"
    entry_height: int = 30

    width: int = 200
    height: int = 30
    fg_color: str = "#2b2b2b"

    police: int = 15
    font: str = 'Helvetica'
    style: str = "normal"

    px: int | tuple[int, int] = 0
    py: int | tuple[int, int] = 0
    ipx: int | tuple[int, int] = 0
    ipy: int | tuple[int, int] = 0

    cadre = None
    button = None
    button_help = None

    cadre_deroulement = None
    label_deroulement = None
    entry_deroulement = None
    button_valider = None

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

        # Deroulement
        self.cadre_deroulement = Frame(master=self.cadre.frame, ipx=0, ipy=0, column=0, row=0,
                                       px=self.px, py=self.py, fg_color="#242424")

        self.label_deroulement = Label(master=self.cadre_deroulement.frame, police=15, ipx=5, ipy=5, px=5, py=5,
                                       text=self.text_label_deroulement,
                                       row=0, column=0)

        self.button_valider = Button(master=self.cadre_deroulement.frame, text=self.text_button_deroulement, police=15,
                                     row=2, column=0, ipx=3, ipy=3, function=self.valider)

        self.label_deroulement.fixer()
        self.button_valider.fixer()

    def valider(self):
        """ Si ajout rapide, on stimule(3), puis on ajoute la description rapide entry.get() .
            Si forget,on stimule(1, entry.get()) (dans le temps) et stimule(2) (moment de la déclaration)
        Puis on retire le deroulement
        """

        if self.text_help == dico_aide['Rapide']:
            print(" --> Simulation3")
            stimulation(3, description = self.entry_deroulement.get())
            print(self.entry_deroulement.get())

            self.retirer_deroulement()

        elif self.text_help == dico_aide['Forget']:
            try:
                minutes = int(self.entry_deroulement.get())
                stimulation(2)
                stimulation(1, minutes )
                print(minutes)
                passer(pages["page_principale"], pages['page_questionnaire1'])

                self.retirer_deroulement()

            except ValueError:
                pass


    def afficher_deroulement(self):

        self.button.unfix()

        self.entry_deroulement = Entry(master=self.cadre_deroulement.frame, width=200, height=self.entry_height, row=1, column=0,
                                       placeholder=self.placeholder, ipx=3, ipy=3, px=5, py=5)

        self.entry_deroulement.fixer()

        self.cadre_deroulement.fixer()

        self.entry_deroulement.entry.focus_set()

        self.entry_deroulement.entry.bind("<Return>", lambda event: self.valider())

    def retirer_deroulement(self):
        self.entry_deroulement.destroy()
        self.cadre_deroulement.unfix()
        self.button.fixer()

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
