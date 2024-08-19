import customtkinter as ctk
from dataclasses import dataclass
from tkinter import Event

from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.tools.buttons import Button
from Interface_Graphique.tools.labels import Label

from Interface_Graphique.var_fonc.functions import tout_complet



@dataclass
class ButtonQuitter:
    master: ctk.CTkFrame
    only_destroy: bool
    root: ctk.CTk

    placed: bool = True
    btn = None

    row: int = 0
    column: int = 0
    columnspan: int = 1

    def __post_init__(self):
        self.create()

    def arret_expe(self, event=None, only_destroy=False):
        """ Stop l'enregistrement et ferme l'application """
        if only_destroy:
            self.root.destroy()
        else:

            if tout_complet():
                #on vérifie que tout soit complet

                # arreterRecEEG() #TODO REMETTRE POUR REC INFO
                self.root.destroy()
            else:
                # Affiche une popup pour dire que tout n'est pas complet et propose de fermer quand même ou de compléter
                popup = PopUpIncomplet(event=event, root_app=self.root)
                popup.afficher()

    def on_enter(self):
        if self.only_destroy:
            self.btn.configure(text="❌ Fermer")
        else:
            self.btn.configure(text="❌ Fermer et sauvegarder")

    def on_leave(self):
        self.btn.configure(text="❌")

    def create(self):

        self.btn = ctk.CTkButton(master=self.master, text="❌", width=15,command=lambda: print('')) # Pas de fonction
        self.btn.bind("<Button-1>", lambda event: self.arret_expe(event=event, only_destroy=self.only_destroy))

        self.btn.configure(fg_color="red", hover_color="white", text_color="black")

        if self.placed :
            self.btn.place(x=10, y=10)

        self.btn.bind("<Enter>", lambda x: self.on_enter())
        self.btn.bind("<Leave>", lambda x: self.on_leave())

    def fixer(self):
        self.btn.grid(column=self.column, row=self.row, columnspan=self.columnspan)


@dataclass
class PopUpIncomplet:
    root_app: ctk.CTk
    event: Event

    root = None
    cadre = None
    label = None
    bouton_fermer = None
    bouton_completer = None

    def __post_init__(self):
        self.create_ajouter_tache()

    def create_ajouter_tache(self):

        x = self.event.x_root
        y = self.event.y_root

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.root = ctk.CTk()
        self.root.geometry(f'{455}x{110}+{x}+{y}')
        self.root.title("Important")

        self.cadre = Frame(master=self.root, fill='both', expand=True, px=0, py=0)

        self.label = Label(master=self.cadre.frame, police=15, row=0, columnspan=2, column=0,
                                 text="Tous les incidents n'ont pas été renseignés correctement")

        self.bouton_fermer = Button(master=self.cadre.frame, text="Fermer quand même",
                                    function=self.fermer, row=1, columnspan=1, column=0)

        self.bouton_completer = Button(master=self.cadre.frame, text="Compléter les renseignements",
                                       function=self.completer, row=1, columnspan=1, column=1)

    def fermer(self):
        """Ferme l'application"""
        self.root.destroy()
        self.root_app.destroy()

    def completer(self):
        """Ferme la fenêtre et ouvre la page_recapitulatif afin de compléter les infos"""
        print("completer")
        # passer(self, page_recapitulatif)


    def afficher(self):
        self.cadre.afficher()
        self.label.fixer()
        self.bouton_fermer.fixer()
        self.bouton_completer.fixer()

        self.root.mainloop()

