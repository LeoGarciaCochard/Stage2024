import customtkinter as ctk
import pandas as pd
from dataclasses import dataclass
from typing import Literal
from tkinter import Event

from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.tools.buttons import Button, ButtonImage
from Interface_Graphique.tools.labels import Label
from Interface_Graphique.tools.entries import Entry
from Interface_Graphique.tools.comboboxes import Combobox

from Interface_Graphique.var_fonc.variables_info import taches, dic_informations
import Interface_Graphique.var_fonc.variables_path as paths

from Interface_Graphique.var_fonc.functions import resource_path

@dataclass
class PopUpAjouterTache:
    event: Event
    combobox: Combobox

    root = None
    cadre_ajouter_tache = None
    label_tache = None
    entry_tache = None
    bouton_valider = None

    def __post_init__(self):
        self.create_ajouter_tache()

    def create_ajouter_tache(self):
        x = self.event.x_root
        y = self.event.y_root

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.root = ctk.CTk()
        self.root.geometry(f'{320}x{110}+{x}+{y}')
        self.root.title("Ajout d'une tâche")

        self.cadre_ajouter_tache = Frame(master=self.root, fill='both', expand=True, px=0, py=0)

        self.label_tache = Label(master=self.cadre_ajouter_tache.frame, text="Nom de la tâche :", police=15)

        self.entry_tache = Entry(master=self.cadre_ajouter_tache.frame, placeholder="Nom de la tâche...", row=0, column=1)

        self.bouton_valider = Button(master=self.cadre_ajouter_tache.frame, text="Valider", function=self.valider, row=1, columnspan=2)

    def valider(self):
        # On rajoute la tache au fichier excel
        df_taches = pd.read_excel(resource_path("../Sources/taches.xlsx"))
        rep = self.entry_tache.entry.get()
        ligne = pd.DataFrame({"Tâches": [rep]})

        df_taches = pd.concat([df_taches, ligne], ignore_index=True)

        df_taches.to_excel(resource_path("../Sources/taches.xlsx"), index=False)

        # On actualise taches ainsi que les options dans la combobox
        taches = list(df_taches['Tâches'])

        self.combobox.combobox.configure(values=taches)
        self.combobox.combobox.set(rep)

        dic_informations['selected_var_tache'] = rep
        # On retire la frame
        self.root.after(100, self.root.destroy)



    def afficher(self):
        self.cadre_ajouter_tache.afficher()
        self.label_tache.fixer()
        self.entry_tache.fixer()
        self.bouton_valider.fixer()

        self.root.mainloop()


@dataclass
class BarreTache:
    master: ctk.CTkFrame | ctk.CTk

    choix:Literal['priorite','erreur',''] = ''

    row: int = 0
    column: int = 0
    columnspan: int = 1

    px: int | tuple[int, int] = 10
    py: int | tuple[int, int] = 10
    ipx: int | tuple[int, int] = 10
    ipy: int | tuple[int, int] = 10

    fg_color:str = "#242424"
    police: int = 15

    cadre_tache = None
    label_tache = None
    combobox_tache = None
    button_rajouter_tache = None

    def __post_init__(self):
        self.create()

        self.label_tache.fixer()
        self.combobox_tache.fixer()
        self.button_rajouter_tache.fixer()


    def create(self):
        self.cadre_tache = Frame(master=self.master, columnspan=self.columnspan, column=self.column, row=self.row,
                                 fg_color=self.fg_color, ipx=10, ipy=10, px=10, py=10)

        self.label_tache = Label(master=self.cadre_tache.frame, column=0, row=0, text='',police=self.police)

        if self.choix == 'priorite':
            self.label_tache.label.configure(text="Quelle est la tâche que vous allez effectuer en priorité ? \n "
                                                  "(Vous pourrez modifier la tâche pars la suite)")
        elif self.choix == 'erreur':
            self.label_tache.label.configure(text="Quelle était la tâche lors de l'incident ?")
        else:
            self.label_tache.label.configure(text="Quelle est la tâche que vous effetuez actuellement ?")

        self.combobox_tache = Combobox(master=self.cadre_tache.frame, values=taches,
                                       variable_name="selected_var_tache", row=0, column=1)

        self.button_rajouter_tache = ButtonImage(master=self.cadre_tache.frame,
                                                 column=2, row=0, tooltip=True,
                                                 text_tooltip="Si la tâche que vous effectuez n'apparaît pas dans la "
                                                              + "liste,\n Cliquez pour rajouter une nouvelle tâche",
                                                 path_hover=paths.img_btn_hover, path=paths.img_btn,
                                                 function=lambda x : self.ajouter_tache(x))
    def ajouter_tache(self, event):
        popup = PopUpAjouterTache(event, self.combobox_tache)
        popup.afficher()

    def afficher(self):
        if dic_informations['selected_var_tache'] is not None:
            self.combobox_tache.combobox.set(dic_informations['selected_var_tache'])
            print("tache : ", dic_informations['selected_var_tache'])

        self.cadre_tache.afficher()

    def fixer(self):
        self.cadre_tache.fixer()

    def cacher(self):
        self.cadre_tache.cacher()
