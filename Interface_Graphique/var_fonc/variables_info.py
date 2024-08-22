from Interface_Graphique.var_fonc.functions import resource_path
from Interface_Graphique.var_fonc.variables_likert import *
from Interface_Graphique.var_fonc.variables_path import fichier_types_err
import pandas as pd

def actualise_taches() :
    """ Lis le fichier excel des tâches et les met dans la liste taches """
    df_taches = pd.read_excel(resource_path("../Sources/taches.xlsx"))
    global taches
    taches =list(df_taches['Tâches'])

def actualise_instance_tache(instance) :
    """ On actualise l'instance de la combobox de BarreTache à tâche """
    instance.combobox_tache.combobox.set(dic_informations['selected_var_tache'])

#Anonymat
def generer_ano() :
    """ Génère un numéro d'anonymat qui suit le dernier"""
    df_anonymat = pd.read_excel(resource_path("../Sources/info_participants.xlsx"))

    #On récupère la dernière ligne de la colonne "N_ano" et ajoute 1 pour le nouveau numéro d'ano
    n_anonymat = int(df_anonymat["N_Ano"].iloc[-1]) + 1 if not df_anonymat.empty else 1
    dic_informations['n_anonymat'] = n_anonymat

    #Ajoute le n_anonymat à la fin du tableau
    nouvelle_ligne = pd.DataFrame({"N_Ano": [n_anonymat]})
    df_anonymat = pd.concat([df_anonymat, nouvelle_ligne], ignore_index=False)

    df_anonymat.to_excel(resource_path("../Sources/info_participants.xlsx"), index=False)

directory_paths = {}

excel_path = r"C:\Users\milio\PycharmProjects\Stage2024\DATA\2\Detail_Stim_n-2__2024-08-22_14h00m54s.xlsx"
columns_to_exclude_complete = ["Path","ID Cible" ,"Timecode", "Parameter"]
columns_to_keep_incomplete = ["ID","Description"]


dic_informations = {'n_anonymat' : None,
                    'genre' : None,
                    'age' : None,
                    'sommeil' : None,
                    'troubles_sommeil' : None,
                    'stress_general' : [dic_stress[48.5]],
                    'cafeine' : None,
                    'quantite_cafeine' : 0,
                    'nicotine' : None,
                    'quantite_nicotine' : 0,
                    'experience' : None,
                    'aisance_informatique' : [dic_aisance_informatique[53]],
                    'passion' : [dic_passion[50]],
                    'bruit' : [dic_bruit[53.5]],
                    'selected_var_tache' : None}

dic_questionnaire = {"nature_incident" : None,
                     "responsabilite" : None,
                     "tache" : None,
                     "importance" : [dic_importance[50]],
                     "description_incident" : None,
                     "concentration" : [dic_concentration[50]],
                     "distraction" : None,
                     "nature_distraction" : None,
                     "fatigue" : [dic_fatigue[50]],
                     "difficulte" : None}

questions = {"age": "Quel est votre âge ?",
             "genre": "Veillez indiquer votre genre",
             "sommeil": "Combien d'heures de sommeil avez-vous eu la nuit dernière ?",
             "troubles_sommeil": "Avez-vous des troubles du sommeil ?",
             "stress_general": "De manière générale, comment décrivez-vous votre état de stress ?",
             "cafeine": "Avez-vous consommé de la caféine aujourd'hui ?",
             "quantite_cafeine": "Combien de tasses de café avez-vous bu aujourd'hui ?",
             "nicotine": "Avez-vous consommé de la nicotine aujourd'hui ?",
             "quantite_nicotine": "Combien de cigarettes avez-vous fumé aujourd'hui ?",
             "experience": "Combien de temps d'expérience avez-vous dans votre domaine ?",
             "aisance_informatique": "À quel point êtes vous à l'aise avec les outils informatiques ?",
             "passion": "À quel point aimez-vous ce travail ?",
             "bruit": "Le niveau de bruit dans votre environnement de travail est :",
             }

values_difficulte = [
    "Très Simple",
    "Simple",
    "Moyenne",
    "Difficile",
    "Très Difficile"
]

df_types = pd.read_excel(fichier_types_err)

types_options = list(df_types['Types'])
types_descriptions = list(df_types['Description'])
types_exemples = list(df_types['Exemple'])


taches = []
values_genre = ["Femme","Homme","Autre"]
values_sommeil = ["Nuit blanche","Moins de 3h","4h","5h","6h","7h","8h","Plus de 9h"]
values_oui_non = ["Oui","Non"]
values_quantite = ["0","1","2","3","4","Plus de 5"]
values_an_exeperience = ["Moins d'un an", "2 ans", "3 ans"," 4 ans", "plus de 5 ans", "plus de 10 ans"]


actualise_taches()