import customtkinter as ctk
import tkinter as tk
from dataclasses import dataclass

from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.tools.buttons import Button
from Interface_Graphique.tools.button_quit import ButtonQuitter
from Interface_Graphique.tools.likerts import Likert
# from Interface_Graphique.var_fonc.variables_likert import *

from Interface_Graphique.tools.class_taches import BarreTache
from Interface_Graphique.tools.formats import FormatTitre, FormatQuestionCombobox
from Interface_Graphique.var_fonc.recolte_donnes import recolter_donnes_participant
from Interface_Graphique.var_fonc.variables_info import *

from Interface_Graphique.var_fonc.functions import passer, passer_definitif
from Interface_Graphique.var_fonc.variables_pages import pages



@dataclass
class PageParticipant:
    root: ctk.CTk

    page_participant = None
    bouton_quitter = None

    titre = None
    titre_informations_personnelles = None
    age = None
    genre = None
    titre_situation_personnelle = None
    sommeil = None
    troubles_sommeil = None
    stress = None
    cafeine = None
    quantite_cafeine = None
    nicotine = None
    quantite_nicotine = None

    button_suivant = None


    def __post_init__(self):
        self.create()

    def create(self):
        self.page_participant = Frame(master=self.root, border_width=0, expand=True, fill="both", px=20, py=20)

        self.bouton_quitter = ButtonQuitter(master=self.page_participant.frame, only_destroy=True, root=self.root)

        self.titre = FormatTitre(master=self.page_participant.frame, text="Merci de remplir ces informations anonymes :"
                                 , police=35, py=20)

        self.titre_informations_personnelles = FormatTitre(master=self.page_participant.frame,
                                                           text="Informations personnelles:", police=20)

        self.age = FormatQuestionCombobox(master=self.page_participant.frame, text=questions["age"],py=(0, 0),
                                          variable="age", values=[str(i) for i in range(18, 90)])
        # self.age.combobox.combobox._dropdown_menu._set

        self.genre = FormatQuestionCombobox(master=self.page_participant.frame, text=questions["genre"],py=(0, 0),
                                            variable="genre", values=values_genre)

        self.titre_situation_personnelle = FormatTitre(master=self.page_participant.frame,
                                                       text="Situation personnelle :", police=20)

        self.sommeil = FormatQuestionCombobox(master=self.page_participant.frame, text=questions["sommeil"],
                                              variable="sommeil", values=values_sommeil)

        self.troubles_sommeil = FormatQuestionCombobox(master=self.page_participant.frame,
                                                       text=questions["troubles_sommeil"], variable="troubles_sommeil",
                                                       values=values_oui_non)

        self.stress = Likert(master=self.page_participant.frame, dic=dic_stress, var=dic_informations['stress_general'],
                             text=dico_text["stress"])

        self.cafeine = FormatQuestionCombobox(master=self.page_participant.frame, text=questions["cafeine"],
                                              variable="cafeine", values=values_oui_non,
                                              py=(0, 0))

        self.quantite_cafeine = FormatQuestionCombobox(master=self.page_participant.frame, py=(0, 0),
                                                      text=questions["quantite_cafeine"], variable="quantite_cafeine",
                                                      values=values_quantite)

        self.nicotine = FormatQuestionCombobox(master=self.page_participant.frame, text=questions["nicotine"],
                                               variable="nicotine", values=values_oui_non,
                                               py=(20, 0))


        self.quantite_nicotine = FormatQuestionCombobox(master=self.page_participant.frame, py=(0, 20),
                                                        text=questions["quantite_nicotine"],
                                                        variable="quantite_nicotine", values=values_quantite)



        self.button_suivant = Button(master=self.page_participant.frame, text="Suivant", function=self.suivant,
                                    police=20, style="bold")

        self.titre.afficher()
        self.titre_informations_personnelles.afficher()
        self.age.afficher()
        self.genre.afficher()
        self.titre_situation_personnelle.afficher()
        self.sommeil.afficher()
        self.troubles_sommeil.afficher()
        self.stress.afficher()
        self.cafeine.afficher()
        self.quantite_cafeine.afficher()
        self.nicotine.afficher()
        self.quantite_nicotine.afficher()
        self.button_suivant.afficher()

        self.page_participant.frame.bind("<Enter>", lambda event: self.surveiller_cafe_nico())
        self.page_participant.frame.bind("<Leave>", lambda event: self.surveiller_cafe_nico())


    def surveiller_cafe_nico(self):
        if self.cafeine.combobox.combobox.get() == "Non":
            dic_informations["quantite_cafeine"] = 0
            self.quantite_cafeine.combobox.combobox.set("0")
            self.quantite_cafeine.combobox.combobox.configure(state="disabled")

        if self.nicotine.combobox.combobox.get() == "Non":
            dic_informations["quantite_nicotine"] = 0
            self.quantite_nicotine.combobox.combobox.set("0")
            self.quantite_nicotine.combobox.combobox.configure(state="disabled")

        if self.cafeine.combobox.combobox.get() == "Oui":
            self.quantite_cafeine.combobox.combobox.configure(state="readonly")

        if self.nicotine.combobox.combobox.get() == "Oui":
            self.quantite_nicotine.combobox.combobox.configure(state="readonly")

    def suivant(self):

        try:
            passer(self, pages["page_participant_2"])
        except KeyError:
            passer(self, pages["page_participant_2"])


    def afficher(self):
        self.page_participant.afficher()


    def cacher(self):
        self.page_participant.cacher()

    def destroy(self):
        self.page_participant.destroy()



@dataclass
class PageParticipant2:
    root: ctk.CTk

    page_participant_2 = None
    bouton_quitter = None

    titre = None
    titre_situation_professionnelle = None
    experience = None
    aisance_informatique = None
    passion = None

    titre_environnement = None
    bruit = None
    tache = None

    cadre_btn = None
    button_retour = None
    button_termine = None


    def __post_init__(self):
        self.create()

    def create(self):

        self.page_participant_2 = Frame(master=self.root, border_width=0, expand=True, fill="both", px=20, py=20)

        self.bouton_quitter = ButtonQuitter(master=self.page_participant_2.frame, only_destroy=True, root=self.root)

        self.titre = FormatTitre(master=self.page_participant_2.frame,
                                 text="Merci de remplir ces informations anonymes :", police=35, py=20)

        self.titre_situation_professionnelle = FormatTitre(master=self.page_participant_2.frame,
                                                           text="Situation professionnelle :", police=20)

        self.experience = FormatQuestionCombobox(master=self.page_participant_2.frame, text=questions["experience"],
                                                 variable="experience", values=values_an_exeperience)

        self.aisance_informatique = Likert(master= self.page_participant_2.frame, dic=dic_aisance_informatique,
                                             var=dic_informations['aisance_informatique'],
                                             text= dico_text["habilite_inf"], sliderwidth=600)

        self.passion = Likert(master= self.page_participant_2.frame, dic=dic_passion,
                              var=dic_informations['passion'], text= dico_text["passion"], sliderwidth=800)


        self.titre_environnement = FormatTitre(master=self.page_participant_2.frame,
                                               text="Environnement de travail :", police=20)

        self.bruit = Likert(master=self.page_participant_2.frame, dic=dic_bruit, var=dic_informations['bruit'],
                            text=dico_text["bruit"], sliderwidth=653.5)

        self.tache = BarreTache(master=self.page_participant_2.frame, choix="priorite", fg_color="#333333")

        self.cadre_btn = Frame(master=self.page_participant_2.frame, px=20, py=20)

        self.button_retour = Button(master=self.cadre_btn.frame, text="Retour", function=self.retour, side=tk.LEFT,
                                    police=20, style="bold")

        self.button_termine = Button(master=self.cadre_btn.frame, text="Terminé", function=self.termine, side=tk.LEFT,
                                     police=20, style="bold")

        self.titre.afficher()
        self.titre_situation_professionnelle.afficher()
        self.experience.afficher()
        self.aisance_informatique.afficher()
        self.passion.afficher()
        self.titre_environnement.afficher()
        self.bruit.afficher()
        self.tache.afficher()
        self.cadre_btn.afficher()
        self.button_retour.afficher()
        self.button_termine.afficher()

    def retour(self):
        passer(self, pages['page_participant'])

    def termine(self):

        if all(key == "n_anonymat" or value is not None for key, value in dic_informations.items()):
            generer_ano()
            recolter_donnes_participant()
            passer_definitif(self, pages["page_principale"])


    def afficher(self):
        self.page_participant_2.afficher()


    def cacher(self):
        self.page_participant_2.cacher()

    def destroy(self):
        pages["page_participant"].destroy()
        self.page_participant_2.destroy()