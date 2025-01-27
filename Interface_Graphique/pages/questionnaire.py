import tkinter as tk

import customtkinter as ctk
from dataclasses import dataclass
import tkinter as tk

from Interface_Graphique.tools.formats import (FormatTitre, FormatChoix2RadioBox, FormatRadiosButtons,
                                               FormatChoix2RadioBoxDeroulement, FormatGridButtons, FormatTextBox)

from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.tools.buttons import Button
from Interface_Graphique.tools.likerts import Likert
from Interface_Graphique.tools.class_taches import BarreTache

from Interface_Graphique.var_fonc.variables_pages import pages
from Interface_Graphique.var_fonc.functions import passer_definitif
from Interface_Graphique.var_fonc.variables_info import (dic_informations, dic_questionnaire, dic_donnes_questionnaire ,
                                                         types_options, types_descriptions, types_exemples,
                                                         dic_importance, dic_concentration, dic_fatigue,
                                                         values_difficulte, dico_text, dic_informations_incident)
from Interface_Graphique.var_fonc.recolte_donnes import stimulation
import Interface_Graphique.var_fonc.variables_info as variables_info

from Interface_Graphique.var_fonc.recolte_donnes import recolter_questionnaire

@dataclass
class PageQuestionnaire:
    root: ctk.CTk

    place_holder_description = "Description de l'incident négatif..."

    modifier = False
    num_dic: int = -1

    page_questionnaire1 = None
    page_questionnaire2 = None
    bouton_annuler = None
    titre = None

    def __post_init__(self):
        self.reset_vars()
        self.create_page1()
        self.create_page2()

    def create_page1(self):

        self.page_questionnaire1 = Frame(master=self.root, border_width=0, ipx=100, py=15,
                                         fill='both', expand=True)

        self.bouton_annuler = Button(master=self.page_questionnaire1.frame, text="Annuler", function=self.annuler,
                                     x=10, y=10)

        self.titre = FormatTitre(master=self.page_questionnaire1.frame, text="Questionnaire sur l'incident négatif",
                                 police=30, style="bold", text_ipy=10, text_ipx=10)

        ############################################################################################################

        self.cadre_nature = Frame(master=self.page_questionnaire1.frame, border_width=2, px=50, py=5,
                                  fill='both', expand=True)

        self.nature_incident = FormatGridButtons(master=self.cadre_nature.frame,
                                                 text="Veuillez renseigner la nature de l'incident négatif",
                                                 options=types_options, descriptions=types_descriptions,
                                                 exemples=types_exemples)

        # Récupération de la nature de l'incident avec self.nature_incident.dic_button_states

        self.responsabilite = FormatChoix2RadioBox(master=self.cadre_nature.frame, text="Selon vous, qui est "
                                                                                        "responsable de l'incident ?",
                                                   choix1="Utilisateur (Moi)", choix2="Système (Machine)",
                                                   variable=self.selected_var_responsabilite, fg_color="#2b2b2b")

        self.barre_tache = BarreTache(master=self.cadre_nature.frame, choix="questionnaire", fg_color="#333333")

        ############################################################################################################

        self.cadre_description = Frame(master=self.page_questionnaire1.frame, border_width=2, px=50, py=5,
                                  fill='both', expand=True)

        self.importance = Likert(master=self.cadre_description.frame, dic=dic_importance, expand=False, py=5,
                                 var= dic_questionnaire['importance'], text= dico_text["importance"], sliderwidth=600)

        self.description = FormatTextBox(master=self.cadre_description.frame, text="Décrivez l'incident négatif :",
                                         placeholder=self.place_holder_description, textbox_height=80, py=0)

        ############################################################################################################

        self.bouton_suivant = Button(master=self.page_questionnaire1.frame, text="Suivant", function=self.suivant1)

        self.bouton_envoyer_etat = Button(master=self.page_questionnaire1.frame, text="Envoyer en l'état",
                                          function=self.envoyer_etat)


        self.bouton_annuler.placed()
        self.titre.afficher()

        self.cadre_nature.afficher()
        self.nature_incident.afficher()
        self.responsabilite.afficher()
        self.barre_tache.afficher()

        self.cadre_description.afficher()
        self.importance.afficher()
        self.description.afficher()

        self.bouton_suivant.afficher()
        self.bouton_envoyer_etat.afficher()



    def create_page2(self):

        self.page_questionnaire2 = Frame(master=self.root, border_width=0, ipx=100, py=15,
                                         fill='both', expand=True)

        self.bouton_annuler2 = Button(master=self.page_questionnaire2.frame, text="Annuler", function=self.annuler,
                                      x=10, y=10)

        self.titre2 = FormatTitre(master=self.page_questionnaire2.frame, text="Questionnaire sur l'incident négatif",
                                 police=30, style="bold", text_ipy=10, text_ipx=10)

        self.bouton_retour1 = Button(master=self.page_questionnaire2.frame, text="Retour", function=self.retour1, py=15)

        ############################################################################################################

        self.cadre_concentration = Frame(master=self.page_questionnaire2.frame, border_width=2, px=50, py=5,
                                  fill='both', expand=True)

        self.concentration = Likert(master=self.cadre_concentration.frame, dic=dic_concentration,
                                    var=dic_questionnaire['concentration'], text=dico_text["concentration"],
                                    sliderwidth=500, expand=True)

        self.distraction = FormatChoix2RadioBoxDeroulement(master=self.cadre_concentration.frame, choix1="Oui",
                                                           choix2="Non",
                                                           text="Étiez-vous distrait(e) par quelque chose au moment où "
                                                                "l'incident négatif s'est produit ?",
                                                           variable=self.selected_var_distraction, fg_color="#2b2b2b",
                                                           text_deroulement="Si oui, par quoi étiez-vous distrait(e) ?",
                                                           placeholder_deroulement="Décrire la distraction...",
                                                           py=5)

        self.fatigue = Likert(master=self.cadre_concentration.frame, dic=dic_fatigue, expand=True,
                                 var=dic_questionnaire['fatigue'], text=dico_text["fatigue"], sliderwidth=500)

        ############################################################################################################

        self.cadre_difficulte = Frame(master=self.page_questionnaire2.frame, border_width=2, px=50, py=5,
                                      fill='both')

        self.difficulte = FormatRadiosButtons(master=self.cadre_difficulte.frame,
                                              text="Comment qualifieriez-vous la difficulté de la tâche au moment de "
                                                   "l'incident négatif ?", variable=self.selected_var_difficulte,
                                              choix=values_difficulte)

        ############################################################################################################

        self.bouton_envoyer_complet = Button(master=self.page_questionnaire2.frame,
                                             text="Envoyer le questionnaire complet",
                                             function=self.envoyer_complet)

        self.bouton_envoyer_etat2 = Button(master=self.page_questionnaire2.frame, text="Envoyer en l'état",
                                          function=self.envoyer_etat)


        self.bouton_annuler2.placed()
        self.titre2.afficher()
        self.bouton_retour1.afficher()

        self.cadre_concentration.afficher()
        self.concentration.afficher()
        self.distraction.afficher()
        self.fatigue.afficher()

        self.cadre_difficulte.afficher()
        self.difficulte.afficher()

        self.bouton_envoyer_complet.afficher()
        self.bouton_envoyer_etat2.afficher()

    def annuler(self):
        """Annule le renseignement, donc stimule(4) pour signaler l'annulation, puis retourne à la page principale"""
        if not self.modifier :
            stimulation(4)
            print(f"\n\n\n J'annule e, stimulant, {self.modifier} \n\n\n")

            self.modifier = False

        print(f"\n\n\n J'annule sans stimuler, {self.modifier} \n\n\n")
        passer_definitif(self, pages["page_principale"])

    def envoyer_etat(self):
        """Envoie les informations en l'état"""

        #TODO : envoyer les informations en l'état

        print("_______________________________\n\nDébut de envoyer_etat : \n"
              "On récupère les réponses\n\n")
        self.get_answers()

        print(f"de base voici le dic_donnes_questionnaire :")
        for dic in dic_donnes_questionnaire:
            print(dic)


        print(f"\nModifier = {self.modifier} donc \n")
        # On copie le dictionnaire des informations de l'incident pour créer le df avec le reste des informations
        if not self.modifier:
            dic_donnes_questionnaire.append(dic_informations_incident.copy())
            print(f"On rajoute les information dans un nouveau dic de dic_donnes_questionnaire :")
            for dic in dic_donnes_questionnaire:
                print(dic)

        # On attribue à index_dic l'index de la liste dic_donnes_questionnaire qui correspond au numéro du dic dont l'index = num_dic

        index_dic = -1
        for i in range(len(dic_donnes_questionnaire)):
            print(f"\nOn regarde le dico :\n{dic_donnes_questionnaire[i]}")
            print(f"['ID'] == num_dict : {dic_donnes_questionnaire[i]['ID'] == self.num_dic}")
            if dic_donnes_questionnaire[i]['ID'] == self.num_dic:
                index_dic = i
                break

        print(f"\nOn met à jour l'élément {index_dic} de dic_donnes_questionnaire avec les informations du questionnaire :")
        dic_donnes_questionnaire[index_dic].update(dic_questionnaire) # TODO PAS LE DERNIER MAIS LE NUM_DIC
        print(dic_donnes_questionnaire[index_dic])



        # Les likerts sont des listes, on prend le premier élément
        for key, value in dic_donnes_questionnaire[index_dic].items():
            if isinstance(value, list):
                try:
                    dic_donnes_questionnaire[index_dic][key] = value[0]
                except IndexError:
                    pass

        print(f"\nNum_dic = {self.num_dic} et on passe à récolter questionnaire\n__________________________")

        if self.modifier:
            recolter_questionnaire(self.num_dic)
        else :
            recolter_questionnaire(self.num_dic)

        passer_definitif(self, pages["page_principale"])

        self.modifier = False
        self.num_dic = -1

        print("Et on réinitialise les variables : mofiier = False et num_dic = -1\n\n_______________________________\n\n")

    def envoyer_complet(self):
        """Envoie les informations si le questionnaire est complet"""

        #TODO : envoyer les informations si le questionnaire est complet

        self.get_answers()

        if self.est_complet():
            self.envoyer_etat()

    def afficher(self):

        self.afficher_page_1()

    def afficher_page_1(self):
        self.create_page1()
        self.create_page2()
        self.page_questionnaire1.afficher()

    def cacher_page_1(self):
        self.page_questionnaire1.cacher()

    def afficher_page_2(self):
        self.create_page2()
        self.page_questionnaire2.afficher()

    def cacher_page_2(self):
        self.page_questionnaire2.cacher()

    def suivant1(self):
        self.page_questionnaire1.frame.pack_forget()
        self.page_questionnaire2.afficher()

    def retour1(self):
        self.page_questionnaire2.frame.pack_forget()
        self.page_questionnaire1.afficher()

    def destroy(self):
        self.page_questionnaire1.destroy()
        self.page_questionnaire2.destroy()
        self.reset_vars()

    def reset_vars(self):

        self.selected_var_responsabilite  = tk.StringVar(master=self.root)
        self.selected_var_distraction  = tk.StringVar(master=self.root)
        self.selected_var_difficulte = tk.StringVar(master=self.root)

    def get_answers(self):
        """
        Récupère les réponses du questionnaire et les stocke dans dic_questionnaire
        Incorporer ici les spécificités de chaque reponse (ex: si place_holder, alors vide)
        Mais pas spécialement besoin de mettre toutes les réponses en str, on peut les laisser en listes car dans
        la fonction envoyer_complet, on les transforme en str si besoin
        """

        # On récupère le type de l'incident sous la forme d'une liste[str][0] donc un str
        nature_incident = self.nature_incident.get_selected()
        if nature_incident is not None:
            dic_questionnaire["nature_incident"] = self.nature_incident.get_selected()[0]  # Type List[str]
        else:
            dic_questionnaire["nature_incident"] = ''

        # On récupère la responsabilité sous la forme d'un str
        dic_questionnaire["responsabilite"] = self.selected_var_responsabilite.get()  # Type str

        # On récupère la tâche sous la forme d'un str
        dic_questionnaire["tache"] = self.barre_tache.get_selected()  # Type str

        # l'importance est déjà obtenue avec le Likert
        # Type List[str]

        # On récupère la description de l'incident sous la forme d'un str
        nouvelle_valeur_description = self.description.get_text()
        if nouvelle_valeur_description == self.place_holder_description:
            nouvelle_valeur_description = ''
        dic_questionnaire["description_incident"] = nouvelle_valeur_description  # Type str

        # la concentration est déjà obtenue avec le Likert
        # Type List[str]

        # On récupère la distraction sous la forme d'un str
        dic_questionnaire["distraction"] = self.selected_var_distraction.get() # Type str

        # On récupère la nature de la distraction sous la forme d'un str
        if dic_questionnaire["distraction"] == "Non":
            nature_distraction = 'Pas de distraction'
        elif dic_questionnaire["distraction"] == "Oui":
            nature_distraction = self.distraction.get_entry_deroulement() # Type str
        else :
            nature_distraction = ''
        dic_questionnaire["nature_distraction"] = nature_distraction  # Type str

        # la fatigue est déjà obtenue avec le Likert
        # Type List[str]

        # On récupère la difficulté sous la forme d'un str
        dic_questionnaire["difficulte"] = self.selected_var_difficulte.get() # Type str

        for key, value in dic_questionnaire.items() : #TODO : A enlever
            print(key, " : ", value)

    def est_complet(self):
        """ regarde dans dic_questionnaire si toutes les valeurs sont remplies :

        """
        return all([dic_questionnaire["nature_incident"] != '',
                   dic_questionnaire["responsabilite"] != '',
                   dic_questionnaire["description_incident"] != '',
                   dic_questionnaire["distraction"] != '',
                   dic_questionnaire["nature_distraction"] != '' or dic_questionnaire["distraction"] == 'Non',
                   dic_questionnaire["difficulte"] != ''])

    def set_values(self, dic_values):

        self.modifier = True
        self.num_dic = dic_values["ID"]

        self.nature_incident.set(dic_values["nature_incident"])
        self.selected_var_responsabilite.set(dic_values["responsabilite"])
        self.barre_tache.set(dic_values["tache"])
        self.importance.set(dic_values["importance"])
        self.description.set(dic_values["description_incident"])
        self.concentration.set(dic_values["concentration"])
        self.selected_var_distraction.set(dic_values["distraction"])
        self.distraction.set(choix=dic_values["distraction"], valeur=dic_values["nature_distraction"])
        self.fatigue.set(dic_values["fatigue"])
        self.selected_var_difficulte.set(dic_values["difficulte"])


