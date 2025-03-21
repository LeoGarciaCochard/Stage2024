import subprocess
import threading
import time
import customtkinter as ctk
from dataclasses import dataclass
import tkinter as tk

from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.tools.button_quit import ButtonQuitter
from Interface_Graphique.tools.labels import Label
from Interface_Graphique.tools.class_taches import BarreTache
from Interface_Graphique.tools.buttons_alignement import BtnHelp, AjoutRapide
from Interface_Graphique.tools.voice_recorder import VoiceRecorder

from Interface_Graphique.var_fonc.functions import passer
from Interface_Graphique.var_fonc.variables_textes import dico_aide
from Interface_Graphique.var_fonc.variables_info import dic_informations, time_code_start_recording
from Interface_Graphique.var_fonc.variables_pages import pages
from Interface_Graphique.var_fonc.recolte_donnes import stimulation

from Interface_Graphique.var_fonc.variables_path import openvibe_executable, scenario_file_Ecriture
from Interface_Graphique.var_fonc.variables_info import process
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

    def create(self):
        """ Création de la page principale """

        ############################################################################################################
        # Frame page d'acceuil
        self.page_principale = Frame(master=self.root, fg_color="#2b2b2b", border_width=2, ipy=10, ipx=100,
                                     fill='both', expand=True)

        ############################################################################################################
        # Bouton quitter & N° Anonymat

        self.cadre_quit_anonymat = Frame(master=self.page_principale.frame, fg_color="#2b2b2b")

        self.bouton_quitter = ButtonQuitter(master=self.cadre_quit_anonymat.frame, only_destroy=False, root=self.root,
                                            placed=False)
        self.cadre_ano = Frame(master=self.cadre_quit_anonymat.frame, corner_radius=5, fg_color="#2b2b2b",
                               border_color="#106a43", border_width=2, row=0, column=1, ipx=0, ipy=0, px=10, py=10)

        self.label_n_ano = Label(master=self.cadre_ano.frame, text='N° Anonymat : \n...', police=13,
                                 ipx=3, ipy=3, px=5, py=5)

        ############################################################################################################
        # Titre

        self.cadre_titre = Frame(self.page_principale.frame, border_width=3, corner_radius=100, ipx=20, py=(150, 60))

        self.label_titre = Label(master=self.cadre_titre.frame, text="Errare humanum est, et machinae".upper(),
                                 police=40, style="bold")

        ############################################################################################################
        # Barre Taches

        self.barre_taches = BarreTache(master=self.page_principale.frame, fg_color="#2b2b2b", police=17, py=0 )

        ############################################################################################################
        # Boutons & aides

        self.cadre_rec = Frame(master=self.page_principale.frame, fg_color="#2b2b2b", ipx=0, ipy=0, px=0, py=0)
        self.renseigner = BtnHelp(master=self.cadre_rec.frame, text_button="Renseigner un incident négatif",
                                  row=0, column=1, ipx=0, ipy=0,
                                  text_help=dico_aide['Erreur'], function=self.renseigner0,
                                  width=400, height=200, police=30, style="bold", py=0)

        self.voice = VoiceRecorder(self.cadre_rec.frame, row=0, column=0) # Bouton pour enregistrer la voix

        self.forget = BtnHelp(master=self.page_principale.frame, width=300, height=50,
                              text_button="J'ai oublié de renseigner un incident négatif",
                              text_help=dico_aide['Forget'], function=self.derouler_forget,
                              text_label_deroulement="Combien de temps s'est-il écoulé depuis l'incident ? \n "
                                                     "(En minutes)",
                              placeholder="Temps en minutes...")

        self.recap = BtnHelp(master=self.page_principale.frame, width=300, height=50, text_button="Voir récapitulatif",
                             text_help=dico_aide['Recap'], function=lambda: passer(self, pages["page_recapitulatif"]))

        self.ajout_rapide = AjoutRapide(master=self.page_principale.frame, width=400, height=50,
                                        text_button="  Ajout Rapide ", text_help=dico_aide['Rapide'],
                                        function=self.derouler_ajout_rapide, img_width=55, img_height=55,
                                        text_label_deroulement="Vous pouvez renseigner une brève description "
                                                               "(Facultatif)", entry_height=50,
                                        text_button_deroulement="Valider ou ignorer",
                                        placeholder="Rapide description...")

        ############################################################################################################

    def renseigner0(self):
        """ Stimule(0) car sur le moment et passe à la page questionnaire"""
        stimulation(0)
        passer(self, pages["page_questionnaire1"])

    def recapitulatif(self):
        """ Affiche le récapitulatif """
        passer(self, pages["page_recapitulatif"])

    def derouler_forget(self , event=None):
        """ Fonction qui affiche les nouveaux éléments pour le forget """
        try:
            self.ajout_rapide.retirer_deroulement()
        except AttributeError:
            pass

        self.forget.afficher_deroulement()

    def derouler_ajout_rapide(self, event=None):
        """ Fonction qui affiche les nouveaux éléments pour l'ajout rapide """
        try:
            self.forget.retirer_deroulement()
        except AttributeError:
            pass

        self.ajout_rapide.afficher_deroulement()


    def afficher(self):
        """ Affiche la page principale en retirant les possibles déroulants de forget et ajout_rapide"""
        try:
            self.forget.retirer_deroulement()
        except AttributeError:
            pass

        try:
            self.ajout_rapide.retirer_deroulement()
        except AttributeError:
            pass

        self.root.after(100, lambda: self.label_n_ano.label.configure(
            text=f"N° Anonymat : \n{dic_informations['n_anonymat']}"))

        self.page_principale.afficher()
        self.cadre_titre.afficher()
        self.label_titre.afficher()
        self.barre_taches.afficher()
        self.cadre_rec.afficher()
        self.renseigner.fixer() # TODO: Fix this
        self.voice.fixer() # TODO: Fix this
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
        self.cadre_rec.cacher()
        self.forget.cacher()
        self.recap.cacher()
        self.ajout_rapide.cacher()

    def destroy(self):
        self.page_principale.destroy()


    def lancer_enregistrement_eeg(self):
        """Lance la fonction lancerRecEEG() dans un thread séparé pour ne pas bloquer l'interface graphique"""

        threading.Thread(target=self.lancerRecEEG).start()

    def lancerRecEEG(self):
        """Lance le rec"""

        time_code_start_recording.append(time.time())

        try:
            command = [openvibe_executable, "--no-gui", "--play", scenario_file_Ecriture]
            process[0] = subprocess.Popen(command)
        except FileNotFoundError:
            print("Erreur : fichier exécutable OpenViBE introuvable.")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution de la commande : {e}")

