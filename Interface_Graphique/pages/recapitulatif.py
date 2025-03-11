import customtkinter as ctk
import pandas as pd
from dataclasses import dataclass

from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.tools.formats import FormatTitre
from Interface_Graphique.tools.buttons import Button
from Interface_Graphique.tools.labels import Label
from Interface_Graphique.tools.scrollable_frames import CadreTableauScrollable


from Interface_Graphique.var_fonc.functions import passer_definitif, resource_path
from Interface_Graphique.var_fonc.variables_likert import *
from Interface_Graphique.var_fonc.variables_pages import pages
from Interface_Graphique.var_fonc.variables_info import (directory_paths, columns_to_exclude_complete,
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

        df = pd.read_excel(resource_path(directory_paths["path_excel_beh"]))
        df = df[df['Parameter'] != 2]  # On supprime les lignes de signalement du moment de l'oubli
        df = df[df['Parameter'] != 4]  # On supprime les lignes de l'annulation du signalement

        df_filtered = df.drop(columns=columns_to_exclude_complete)

        # Créer une instance de la classe
        cadre_tableau = CadreTableauScrollable(master=cadre, bg_color='#333333', width=600, height=400)

        # Ajouter le cadre où vous allez ajouter du contenu
        scrollable_frame = cadre_tableau.get_frame()

        # En-tête de colonnes

        headers = ["Modifier"] + list(df_filtered.columns)

        for col_num, col_name in enumerate(headers):

            col_name_presentale = col_name.replace('_', ' ').title()

            header = Label(master=scrollable_frame, text=col_name_presentale, row=0, column=col_num, px=10, py=5,
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

    def create_tableau_incomplet(self, cadre):

        df = pd.read_excel(resource_path(directory_paths["path_excel_beh"]))
        df = df[df['Parameter'] != 2]  # On supprime les lignes de signalement du moment de l'oubli
        df = df[df['Parameter'] != 4] # On supprime les lignes de l'annulation du signalement

        # Retiré les paramètres annulés :


        # Créer une instance de la classe
        cadre_tableau = CadreTableauScrollable(master=cadre, bg_color='#333333', width=600, height=400)

        # Ajouter le cadre où vous allez ajouter du contenu
        scrollable_frame = cadre_tableau.get_frame()

        # En-tête de colonnes

        headers = ["Modifier"] + list(df[columns_to_keep_incomplete].columns)

        for col_num, col_name in enumerate(headers):

            col_name_presentale = col_name.replace('_', ' ').title()

            header = Label(master=scrollable_frame, text=col_name_presentale, row=0, column=col_num, px=10, py=5,
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
                        if str(value) == 'nan' or str(value) == ' ' or str(value) == "":
                            value = '--'
                        cell = Label(master=scrollable_frame, text=value, row=row_num+1, column=col_num+1,
                                     px=10, py=5, police=self.police)
                        cell.fixer()

    def modifier_ligne(self, row_id):

        df = pd.read_excel(resource_path(directory_paths["path_excel_beh"]))

        # Suppression des colonnes à exclure
        df = df.drop(columns=columns_to_exclude_complete)

        # Trouver l'indice de la ligne correspondant à l'ID spécifié
        row_modif = int(df.index[df['ID'] == row_id].tolist()[0])

        # Extraire la ligne correspondant à l'ID spécifié
        ligne = df.loc[df['ID'] == row_id]

        # Supprimer la colonne 'ID'
        # ligne = ligne.drop(columns=['ID'])

        # Convertir la ligne en dictionnaire {nom de colonne : valeur}
        ligne_dict = ligne.to_dict(orient='records')[0]

        #  # On modifie le type des valeurs pour les likerts qui nécessitent des int, la valeur associée au string] :

        # On crée une fonction intermédiare nécessaire pour la conversion
        def get_key_from_value(dic, value):
            """Récuperer la clef (int) associée à une valeur (str) dans un dictionnaire"""
            for key, val in dic.items():
                if val == value:
                    return key

        for key, value in ligne_dict.items():
            # pour tous les likerts échanger leurs valeurs
            if key in ['importance', 'concentration', 'fatigue']:  # TODO : Ajouter les autres likerts si ajout
                dic = globals().get(f"dic_{key}")
                if dic:
                    ligne_dict[key] = get_key_from_value(dic, value)
            if pd.isna(value):
                ligne_dict[key] = ''


        print("Ligne à modifier : ", ligne_dict)

        #Passer à la page questionnaire avec les valeurs de la ligne à modifier
        passer_definitif(self, pages["page_questionnaire1"])
        pages["page_questionnaire1"].set_values(ligne_dict)

    def verifier_page_1_questionnaire(self, row):
        """ Verifie si les information de la page 1 sont complétées"""


        type = str(row['nature_incident'])
        faute = str(row['responsabilite'])
        description = str(row['description_incident'])


        rep = (type != '' and faute != '' and description != "Description de l'incident...")
        rep_vide = (type != 'nan' and faute != 'nan' and description != "nan")

        return rep and rep_vide

    def afficher(self):
        self.create()
        self.page_recapitulatif.afficher()

    def destroy(self):
        self.page_recapitulatif.destroy()

    def toutes_infos_completes(self):
        df = pd.read_excel(resource_path(directory_paths["path_excel_beh"]))
        df = df[df['Parameter'] != 2]  # On supprimer les lignes de signalement du moment de l'oubli
        df = df[df['Parameter'] != 4]  # On supprimer les lignes de l'annulation du signalement

        for row_num, row in df.iterrows():
            if not self.verifier_page_1_questionnaire(row):
                return False

        return True



