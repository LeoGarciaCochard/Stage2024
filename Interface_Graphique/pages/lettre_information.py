import customtkinter as ctk
from dataclasses import dataclass

from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.tools.buttons import Button
from Interface_Graphique.tools.button_quit import ButtonQuitter
from Interface_Graphique.tools.labels import Label

from Interface_Graphique.pages.questionnaire_participant import PageParticipant
from Interface_Graphique.var_fonc.variables_textes import texte_lettre_information
from Interface_Graphique.var_fonc.functions import passer_definitif
from Interface_Graphique.var_fonc.variables_pages import pages


@dataclass
class PageLettreInformation:
    root: ctk.CTk

    page_lettre_information = None
    bouton_quitter = None


    def __post_init__(self):
        self.create()

    def create(self):

        self.page_lettre_information = Frame(master=self.root, border_width=0, expand=True, fill="both", px=20, py=5,
                                             ipy=20)

        self.bouton_quitter = ButtonQuitter(master=self.page_lettre_information.frame, only_destroy=True,
                                            root=self.root)
        self.lettre_information = Frame(master=self.page_lettre_information.frame, border_width=3, corner_radius=75,
                                        expand=True, py=0, ipx=30, ipy=30)

        self.titre = Label(master=self.lettre_information.frame, text=texte_lettre_information["texte_titre"],
                           police=30, style="bold", py=(20, 0))

        self.p1 = Label(master=self.lettre_information.frame, text=texte_lettre_information["texte_p1"],
                        police=20, justify="left")

        self.p2 = Label(master=self.lettre_information.frame, text=texte_lettre_information["texte_p2"],
                        police= 20, justify="left")

        self.sTitre2 = Label(master=self.lettre_information.frame, text=texte_lettre_information["texte_sTitre2"],
                             police=25)

        self.texte_liste = Label(master=self.lettre_information.frame, text=texte_lettre_information["texte_liste"],
                                    police=20)

        self.texte_thanks = Label(master=self.lettre_information.frame, text=texte_lettre_information["texte_thanks"],
                                  police=18, style="italic")

        self.bouton = Button(master=self.page_lettre_information.frame, text="Compris", width=250, height=50, police=30,
                             function=self.passer, style="bold", py=(0,90))

    def passer(self):
        print("Dic : ",pages)
        passer_definitif(self, pages["page_participant"])

    def afficher(self):
        self.page_lettre_information.afficher()
        self.lettre_information.afficher()
        self.titre.afficher()
        self.p1.afficher()
        self.p2.afficher()
        self.sTitre2.afficher()
        self.texte_liste.afficher()
        self.texte_thanks.afficher()
        self.bouton.afficher()

    def destroy(self):
        self.page_lettre_information.destroy()