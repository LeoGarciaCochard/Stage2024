import customtkinter as ctk
from dataclasses import dataclass

from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.tools.button_quit import ButtonQuitter
from Interface_Graphique.tools.labels import Label
from Interface_Graphique.tools.class_taches import BarreTache
from Interface_Graphique.tools.buttons_alignement import BtnHelp
from Interface_Graphique.pages.recapitulatif import PageRecapitulatif
from Interface_Graphique.var_fonc.functions import stimulation, passer
from Interface_Graphique.var_fonc.variables_textes import dico_aide


@dataclass
class PagePrincipale:
    root: ctk.CTk

    page_principale = None
    bouton_quitter = None

    cadre_titre = None
    label_titre = None

    barre_taches = None
    renseigner = None
    forget = None
    recap = None

    def __post_init__(self):
        self.create()

    def create(self):
        """ Création de la page principale """

        page_recapitulatif = PageRecapitulatif(root=self.root)

        # Frame page d'acceuil
        self.page_principale = Frame(master=self.root, fg_color="#2b2b2b", border_width=2, ipy=10, ipx=100,
                                     fill='both', expand=True)

        # Bouton quitter
        self.bouton_quitter = ButtonQuitter(master=self.page_principale.frame, only_destroy=False, root=self.root)

        # Titre
        self.cadre_titre = Frame(self.page_principale.frame, border_width=3, corner_radius=100, ipx=20, py=(250, 60))

        self.label_titre = Label(master=self.cadre_titre.frame, text="Errare humanum est, et machinae".upper(),
                                 police=40, style="bold")

        # Barre Taches

        self.barre_taches = BarreTache(master=self.page_principale.frame, fg_color="#2b2b2b")

        # Boutons & aides

        self.renseigner = BtnHelp(master=self.page_principale.frame, text_button="Renseigner un incident négatif",
                                  text_help=dico_aide['Erreur'], function=lambda: stimulation(0),
                                  width=400, height=200, police=30, style="bold")

        self.forget = BtnHelp(master=self.page_principale.frame, width=300, height=50,
                              text_button="J'ai oublié de renseigner un incident négatif",
                              text_help=dico_aide['Forget'], function=self.derouler_forget)

        self.recap = BtnHelp(master=self.page_principale.frame, width=300, height=50,
                             text_button="Voir récapitulatif",
                             text_help=dico_aide['Recap'], function=lambda: passer(self, page_recapitulatif))

    def derouler_forget(self):
        """ Fonction de forget """
        pass

    def afficher(self):
        self.page_principale.afficher()
        self.cadre_titre.afficher()
        self.label_titre.afficher()
        self.barre_taches.afficher()
        self.renseigner.afficher()
        self.forget.afficher()
        self.recap.afficher()

    def cacher(self):
        self.page_principale.cacher()
        self.cadre_titre.cacher()
        self.label_titre.cacher()
        self.barre_taches.cacher()
        self.renseigner.cacher()
        self.forget.cacher()
        self.recap.cacher()

    def destroy(self):
        self.page_principale.destroy()
