import customtkinter as ctk
import pandas as pd
from dataclasses import dataclass

from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.tools.formats import FormatTitre
from Interface_Graphique.tools.buttons import Button
from Interface_Graphique.tools.labels import Label
from Interface_Graphique.tools.scrollable_frames import CadreTableauScrollable


from Interface_Graphique.var_fonc.functions import passer_definitif

from Interface_Graphique.var_fonc.variables_pages import pages
from Interface_Graphique.var_fonc.variables_info import (excel_path, columns_to_exclude_complete,
                                                         columns_to_keep_incomplete)

@dataclass
class PageRecapitulatif:

    root: ctk.CTk

    page_recapitulatif = None

    police = 13

    def __post_init__(self):
        pass


    def create(self):

        self.page_recapitulatif = Frame(master=self.root, border_width=0, ipy=10, ipx=100, fill='both', expand=True)

        self.titre = FormatTitre(master=self.page_recapitulatif.frame, text="Récapitulatif des incidents négatifs",
                                 police=40, py=20)

        self.button_retour_page_principale = Button(master=self.page_recapitulatif.frame, text="Retour",
                                                    function=lambda: passer_definitif(self, pages["page_principale"]),
                                                    x=10, y=10)

        ############################################################################################################
        # Renseignements complétés

        self.cadre_complet = Frame(master=self.page_recapitulatif.frame,  border_width=2, ipy=10,
                                   fill='both', expand=True)

        self.titre_complet = FormatTitre(master=self.cadre_complet.frame, text="Renseignements complétés", police=20)



        ############################################################################################################
        # Renseignements incomplets

        self.cadre_incomplet = Frame(master=self.page_recapitulatif.frame, border_width=2, ipy=10,
                                   fill='both', expand=True)

        self.titre_incomplet = FormatTitre(master=self.cadre_incomplet.frame, text="Renseignements à compléter",
                                           police=20)

        ############################################################################################################
        # Affichage

        self.titre.afficher()
        self.button_retour_page_principale.placed()

        self.cadre_complet.afficher()
        self.titre_complet.afficher()
        self.create_tableau_complet(self.cadre_complet.frame)

        self.cadre_incomplet.afficher()
        self.titre_incomplet.afficher()
        self.create_tableau_incomplet(self.cadre_incomplet.frame)


    def create_tableau_complet(self, cadre):

        df = pd.read_excel(excel_path)

        df_filtered = df.drop(columns=columns_to_exclude_complete)

        # Créer une instance de la classe
        cadre_tableau = CadreTableauScrollable(master=cadre, bg_color='#333333', width=600, height=400)

        # Ajouter le cadre où vous allez ajouter du contenu
        scrollable_frame = cadre_tableau.get_frame()

        # En-tête de colonnes

        headers = ["Modifier"] + list(df_filtered.columns)

        for col_num, col_name in enumerate(headers):
            header = Label(master=scrollable_frame, text=col_name, row=0, column=col_num, px=10, py=5,
                           police=self.police)
            header.fixer()

            #Inserer les données et les boutons de modification

            for row_num, row in df_filtered.iterrows() :

                if self.verifier_page_1_questionnaire(row) :
                    row_id = row["ID"]

                    # Ajouter le bouton modifier

                    button_modifier = Button(master=scrollable_frame, text="Modifier", width=50,
                                             function=lambda row=row_id: self.modifier_ligne(row),
                                             row=row_num+1, column=0, px=10, py=5)
                    button_modifier.fixer()

                    # Ajouter les autres cellules

                    for col_num, value in enumerate(row) :
                        if str(value) == 'nan' or str(value) == ' ': # TODO : Vérifier si c'est la bonne condition
                            value = '--'
                        cell = Label(master=scrollable_frame, text=value, row=row_num+1, column=col_num+1,
                                     px=10, py=5, police=self.police)
                        cell.fixer()

    def create_tableau_incomplet(self,cadre):

        df = pd.read_excel(excel_path)
        df = df[df['Parameter'] != 2]  # On supprimer les lignes de signalement du moment de l'oubli

        # Créer une instance de la classe
        cadre_tableau = CadreTableauScrollable(master=cadre, bg_color='#333333', width=600, height=400)

        # Ajouter le cadre où vous allez ajouter du contenu
        scrollable_frame = cadre_tableau.get_frame()

        # En-tête de colonnes

        headers = ["Modifier"] + list(df[columns_to_keep_incomplete].columns)

        for col_num, col_name in enumerate(headers):
            header = Label(master=scrollable_frame, text=col_name, row=0, column=col_num, px=10, py=5,
                           police=self.police)
            header.fixer()

            #Inserer les données et les boutons de modification

            for row_num, row in df.iterrows() :

                if not self.verifier_page_1_questionnaire(row) :
                    row_id = row["ID"]

                    # Ajouter le bouton modifier

                    button_modifier = Button(master=scrollable_frame, text="Modifier", width=50,
                                             function=lambda row=row_id: self.modifier_ligne(row),
                                             row=row_num+1, column=0, px=10, py=5)
                    button_modifier.fixer()

                    # Ajouter les autres cellules

                    filtered_row = row[columns_to_keep_incomplete]
                    for col_num, value in enumerate(filtered_row) :
                        if str(value) == 'nan' or str(value) == ' ': # TODO : Vérifier si c'est la bonne condition
                            value = '--'
                        cell = Label(master=scrollable_frame, text=value, row=row_num+1, column=col_num+1,
                                     px=10, py=5, police=self.police)
                        cell.fixer()

    def modifier_ligne(self, row_id):
        print("Id de la ligne à modifier : ", row_id)

    def verifier_page_1_questionnaire(self, row):
        """ Verifie si les information de la page 1 sont complétées"""

        type = str(row['Type'])
        faute = str(row['Faute'])
        description = str(row['Description'])

        rep = (type != '' and faute != '' and description != "Description de l'incident négatif...")
        rep_vide = (type != 'nan' and faute != 'nan' and description != "nan")

        return rep and rep_vide

    def afficher(self):
        self.create()
        self.page_recapitulatif.afficher()

    def destroy(self):
        self.page_recapitulatif.destroy()


