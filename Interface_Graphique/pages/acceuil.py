import customtkinter as ctk
import tkinter as tk
from dataclasses import dataclass

from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.tools.buttons import Button, ButtonQuitter, ButtonImage
from Interface_Graphique.tools.labels import Label
from Interface_Graphique.tools.entries import Entry
from Interface_Graphique.tools.comboboxes import Combobox
import Interface_Graphique.var_fonc.variables_path as paths
import Interface_Graphique.var_fonc.functions as functions
import Interface_Graphique.var_fonc.variables_taches as variables_taches


@dataclass
class PageAcceuil:
    root: ctk.CTk

    bouton_nouveau_participant = None
    label_titre = None
    bouton_quitter = None
    bouton_participant_existant = None
    cadre_existant = None
    cadre_titre = None
    page_acceuil = None
    cadre_boutons = None
    bouton_valider_existant = None

    button_rajouter_tache = None
    label_tache = None
    entry_n_ano = None

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
                                                 function=self.nouveau, side=tk.LEFT)
        self.bouton_participant_existant = Button(master=self.cadre_boutons.frame, text="Utiliser un numéro existant",
                                                  function=self.existant, side=tk.LEFT)

        # Cadre existant :
        self.cadre_existant = Frame(master=self.page_acceuil.frame)

        self.entry_n_ano = Entry(master=self.cadre_existant.frame, placeholder="N° Anonymat...",
                                 row=0, columnspan=3,column=0)

        self.label_tache = Label(master=self.cadre_existant.frame, column=0, row=1,
                                 text="Quelle est la tâche que vous allez effectuer en priorité ?")

        self.combobox_tache = Combobox(master=self.cadre_existant.frame, values=variables_taches.taches,
                                     variable_name="selected_var_tache", row=1, column=1, columnspan=1)

        self.button_rajouter_tache = ButtonImage(master = self.cadre_existant.frame,
                                                 column=2, row=1, tooltip=True,
                                                 text_tooltip="Si la tâche que vous effectuez n'apparaît pas dans la "
                                                              + "liste,\n Cliquez pour rajouter une nouvelle tâche",
                                                 path_hover=paths.img_btn_hover, path=paths.img_btn,
                                                 function=functions.ajouter_tache)

        self.bouton_valider_existant = Button(master=self.cadre_existant.frame, text="Valider",
                                              function=self.verifier_existant, side=tk.LEFT,
                                              row=2, columnspan=3, column=0)

    def verifier_existant(self):
        pass

    def nouveau(self):
        self.page_acceuil.frame.destroy()

    def existant(self):
        self.cadre_existant.afficher()
        self.entry_n_ano.fixer()
        self.label_tache.fixer()
        self.combobox_tache.fixer()
        self.button_rajouter_tache.fixer()
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



# btn_valider = ctk.CTkButton(notif_exi,text="Valider",command=validation ,font=('Helvetica',15))
#
#
# def modifier_tache(rep):
#     """ Modifie la tâche de la ligne"""
#     global tache_modif
#     tache_modif = rep
#

# def change_tache(rep):
#     global selected_var_tache
#     selected_var_tache = rep
#     combobox_tache2.set(selected_var_tache)
#
# frame_tache0 = ctk.CTkFrame(master=notif_exi, fg_color="#242424")
#
# label_tache0 = ctk.CTkLabel(master=frame_tache0, text="Quelle est la tâche que vous allez effectuer en priorité ?\n(Vous pourrez modifier la tâche en cours)",font=('Helvetica',15))
# label_tache0.grid(row=1,column=0, ipadx=15, ipady=5)
#
# combobox_tache0 = ctk.CTkComboBox(master=frame_tache0, values=taches, state="readonly", command= lambda x : change_tache(x))
# combobox_tache0.grid(row=1,column=1)
