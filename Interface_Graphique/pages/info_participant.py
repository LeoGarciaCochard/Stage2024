import customtkinter as ctk
import tkinter as tk
from dataclasses import dataclass

from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.tools.buttons import Button
from Interface_Graphique.tools.button_quit import ButtonQuitter
from Interface_Graphique.tools.labels import Label

from Interface_Graphique.tools.formats import FormatTitre, FormatQuestionCombobox
from Interface_Graphique.var_fonc.variables_info import *


@dataclass
class PageParticipant:
    root: ctk.CTk

    page_participant = None

    def __post_init__(self):
        self.create()

    def create(self):
        self.page_participant = Frame(master=self.root, border_width=0, expand=True, fill="both", px=20, py=20)

        self.bouton_quitter = ButtonQuitter(master=self.page_participant.frame, only_destroy=True, root=self.root)

        self.titre = FormatTitre(master=self.page_participant.frame, text="Merci de remplir ces informations anonymes :"
                                 , police=35, py=20)

        self.titre_informations_personnelles = FormatTitre(master=self.page_participant.frame,
                                                           text="Informations personnelles:", police=20)

        self.genre = FormatQuestionCombobox(master=self.page_participant.frame, text=questions["genre"],
                                            variable=dic_informations["genre"], values=values_genre)


        self.button_suivant = Button(master=self.page_participant.frame, text="Suivant", command=self.suivant)

    def suivant(self):
        passer_page(self, Page)

    def afficher(self):
        self.page_participant.afficher()
        self.titre.afficher()
        self.titre_informations_personnelles.afficher()
        self.genre.afficher()

        self.button_suivant.afficher()