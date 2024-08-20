import customtkinter as ctk
from dataclasses import dataclass
import tkinter as tk

from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.tools.button_quit import ButtonQuitter
from Interface_Graphique.tools.labels import Label
from Interface_Graphique.tools.class_taches import BarreTache
from Interface_Graphique.tools.buttons_alignement import BtnHelp, AjoutRapide
from Interface_Graphique.pages.recapitulatif import PageRecapitulatif
from Interface_Graphique.var_fonc.functions import stimulation, passer
from Interface_Graphique.var_fonc.variables_textes import dico_aide
from Interface_Graphique.var_fonc.variables_info import dic_informations


@dataclass
class PagePrincipale:
    root: ctk.CTk

    page_principale = None

    cadre_quit_anonymat = None
    bouton_quitter = None
    cadre_ano = None
    label_n_ano = None

    cadre_titre = None
    label_titre = None

    barre_taches = None
    renseigner = None
    forget = None
    recap = None
    ajout_rapide = None

    def __post_init__(self):
        self.create()

        self.root.after(100,lambda: self.label_n_ano.label.configure(text=f"N° Anonymat : \n{dic_informations['n_anonymat']}"))

    def create(self):
        """ Création de la page principale """

        page_recapitulatif = PageRecapitulatif(root=self.root)

        # Frame page d'acceuil
        self.page_principale = Frame(master=self.root, fg_color="#2b2b2b", border_width=2, ipy=10, ipx=100,
                                     fill='both', expand=True)

        # Bouton quitter & N° Anonymat

        self.cadre_quit_anonymat = Frame(master=self.page_principale.frame, fg_color="#2b2b2b")

        self.bouton_quitter = ButtonQuitter(master=self.cadre_quit_anonymat.frame, only_destroy=False, root=self.root,
                                            placed=False)
        self.cadre_ano = Frame(master=self.cadre_quit_anonymat.frame, corner_radius=5, fg_color="#2b2b2b",
                               border_color="#106a43", border_width=2, row=0, column=1, ipx=0, ipy=0, px=10, py=10)

        self.label_n_ano = Label(master=self.cadre_ano.frame, text='N° Anonymat : \n...', police=13,
                                 ipx=3, ipy=3, px=5, py=5)

        # Titre

        self.cadre_titre = Frame(self.page_principale.frame, border_width=3, corner_radius=100, ipx=20, py=(150, 60))

        self.label_titre = Label(master=self.cadre_titre.frame, text="Errare humanum est, et machinae".upper(),
                                 police=40, style="bold")

        # Barre Taches

        self.barre_taches = BarreTache(master=self.page_principale.frame, fg_color="#2b2b2b", police=17, py=0 )

        # Boutons & aides

        self.renseigner = BtnHelp(master=self.page_principale.frame, text_button="Renseigner un incident négatif",
                                  text_help=dico_aide['Erreur'], function=lambda: stimulation(0),
                                  width=400, height=200, police=30, style="bold", py=0)

        self.forget = BtnHelp(master=self.page_principale.frame, width=300, height=50,
                              text_button="J'ai oublié de renseigner un incident négatif",
                              text_help=dico_aide['Forget'], function=self.derouler_forget)

        self.recap = BtnHelp(master=self.page_principale.frame, width=300, height=50, text_button="Voir récapitulatif",
                             text_help=dico_aide['Recap'], function=lambda: passer(self, page_recapitulatif))

        self.ajout_rapide = AjoutRapide(master=self.page_principale.frame, width=400, height=50,
                                        text_button=" Ajout Rapide ", text_help=dico_aide['Rapide'],
                                        function=self.derouler_ajout_rapide, img_width=55, img_height=55)


    def derouler_forget(self):
        """ Fonction de forget """
        pass

    def derouler_ajout_rapide(self):
        """ Fonction de ajout rapide """
        pass

    def afficher(self):
        self.page_principale.afficher()
        self.cadre_titre.afficher()
        self.label_titre.afficher()
        self.barre_taches.afficher()
        self.renseigner.afficher()
        self.forget.afficher()
        self.recap.afficher()
        self.ajout_rapide.afficher()
        self.bouton_quitter.fixer()
        self.label_n_ano.afficher()
        self.cadre_ano.fixer()
        self.cadre_quit_anonymat.frame.place(x=10, y=5)

    def cacher(self):
        self.page_principale.cacher()
        self.cadre_titre.cacher()
        self.label_titre.cacher()
        self.barre_taches.cacher()
        self.renseigner.cacher()
        self.forget.cacher()
        self.recap.cacher()
        self.ajout_rapide.cacher()

    def destroy(self):
        self.page_principale.destroy()
