import customtkinter as ctk
import tkinter as tk
from dataclasses import dataclass

from Interface_Graphique.pages.lettre_information import PageLettreInformation
from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.tools.buttons import Button
from Interface_Graphique.tools.button_quit import ButtonQuitter
from Interface_Graphique.tools.labels import Label
from Interface_Graphique.tools.entries import Entry
from Interface_Graphique.var_fonc.variables_info import dic_informations
from Interface_Graphique.tools.class_taches import BarreTache
from Interface_Graphique.var_fonc.functions import passer_definitif
from Interface_Graphique.pages.principal import PagePrincipale

@dataclass
class PageAcceuil:
    root: ctk.CTk

    page_acceuil = None
    bouton_quitter = None

    cadre_titre = None
    label_titre = None

    cadre_boutons = None
    bouton_participant_existant = None
    bouton_nouveau_participant = None

    cadre_existant = None
    entry_n_ano = None
    barre_taches = None
    bouton_valider_existant = None

    def __post_init__(self):
        self.create_acceuil()

    def create_acceuil(self):

        # Frame page d'acceuil
        self.page_acceuil = Frame(master=self.root, border_width=3, expand=True, fill="both", px=20, py=20)

        # Bouton quitter
        self.bouton_quitter = ButtonQuitter(master=self.page_acceuil.frame, only_destroy=True, root=self.root)

        # Titre
        self.cadre_titre = Frame(self.page_acceuil.frame, border_width=3, corner_radius=100, ipx=20, py=(250, 60))

        self.label_titre = Label(text="Options de lancement :", master=self.cadre_titre.frame, police=40, style="bold")

        # Cadre et boutons
        self.cadre_boutons = Frame(master=self.page_acceuil.frame)

        self.bouton_nouveau_participant = Button(master=self.cadre_boutons.frame, text="Générer un numéro d'anonymat",
                                                 function=self.nouveau, side=tk.LEFT,
                                                 width=300, height=40, police=20)
        self.bouton_participant_existant = Button(master=self.cadre_boutons.frame, text="Utiliser un numéro existant",
                                                  function=self.existant, side=tk.LEFT,
                                                 width=300, height=40, police=20)

        # Cadre existant :
        self.cadre_existant = Frame(master=self.page_acceuil.frame, fg_color="#242424")

        self.entry_n_ano = Entry(master=self.cadre_existant.frame, placeholder="N° Anonymat...",
                                 row=0, columnspan=3,column=0)

        self.barre_taches = BarreTache(master=self.cadre_existant.frame, column=1, row=1, choix='priorite')

        self.bouton_valider_existant = Button(master=self.cadre_existant.frame, text="Valider",
                                              function=self.verifier_existant, side=tk.LEFT,
                                              row=2, columnspan=3, column=0)

    def verifier_existant(self):
        try :
            n_anoymat = int(self.entry_n_ano.get())
            dic_informations['n_anonymat'] = n_anoymat
            if dic_informations['selected_var_tache'] is not None :
                page_principale = PagePrincipale(self.root)
                passer_definitif(self,page_principale)

        except ValueError:
            print("Erreur :" + " Le numéro d'anonymat doit être un entier, et la tâche doit être sélectionnée")


    def nouveau(self):
        page_lettre_information = PageLettreInformation(self.root)
        passer_definitif(self,page_lettre_information)

    def existant(self):
        self.cadre_existant.afficher()
        self.entry_n_ano.fixer()
        self.barre_taches.fixer()
        self.bouton_valider_existant.fixer()
        print("existant")

    def afficher_page_acceuil(self):
        self.page_acceuil.afficher()

        self.cadre_titre.afficher()
        self.label_titre.afficher()

        self.cadre_boutons.afficher()

        self.bouton_nouveau_participant.afficher()
        self.bouton_participant_existant.afficher()

        self.cadre_boutons.afficher()

    def destroy(self):
        self.page_acceuil.destroy()

