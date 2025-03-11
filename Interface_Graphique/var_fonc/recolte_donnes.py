import subprocess
import shutil
import pandas as pd
import os
import time

from Interface_Graphique.var_fonc.functions import resource_path
from Interface_Graphique.var_fonc.variables_info import (dic_informations, directory_paths, dic_donnes_questionnaire,
                                                         columns_excel_initialisation, time_code_start_recording,
                                                         dic_informations_incident, process)

from Interface_Graphique.var_fonc.variables_path import openvibe_executable, scenario_file_Stim, path_recordStim_edf

from Interface_Graphique.var_fonc.variables_pages import pages

def format_n_anonymat():
    n_anonymat = dic_informations['n_anonymat']

    if n_anonymat in list(range(1, 10)):
        n_anonymat = f"0{n_anonymat}"

    return n_anonymat

def creer_repertoire_subject():
    """ Crée un répertoire pour un sujet """

    n_anonymat = format_n_anonymat()

    # Création des chemins pour sub-XX, sub-XX/eeg et sub-XX/beh
    path_sub = resource_path(f"../Database/sub-{n_anonymat}")
    path_eeg = os.path.join(path_sub, "eeg")
    path_beh = os.path.join(path_sub, "beh")
    path_audio = os.path.join(path_sub, "audio")

    path_excel_beh = os.path.join(path_beh, f"sub-{n_anonymat}_task-work_questionnaire_beh.xlsx")
    path_time_codes = resource_path('../OpenVibe/enregistrement_en_cours/timecodes.csv')


    os.makedirs(path_sub, exist_ok=True)
    os.makedirs(path_eeg, exist_ok=True)
    os.makedirs(path_beh, exist_ok=True)
    os.makedirs(path_audio, exist_ok=True)

        # Créer le fichier excel vide s'il n'existe pas déjà
    if not os.path.exists(path_excel_beh):
        df = pd.DataFrame(columns=columns_excel_initialisation)
        df.set_index('ID', inplace=True)
        df.to_excel(path_excel_beh)

    os.path.exists(path_time_codes)
    df = pd.DataFrame(columns=["ID", "Timecode", "Parameter"])
    df.set_index('ID', inplace=True)
    df.to_csv(path_time_codes)

    # On ajoute les chemins au dictionnaire
    directory_paths["path_sub"] = path_sub
    directory_paths["path_eeg"] = path_eeg
    directory_paths["path_beh"] = path_beh
    directory_paths["path_audio"] = path_audio
    directory_paths["path_excel_beh"] = path_excel_beh
    directory_paths["path_time_codes"] = path_time_codes


def recolter_donnes_participant():
    """ Récupère les informations du participant et les met dans le fichier excel ../Database/participants.xlsx """

    # On transforme le dictionnaire en DataFrame
    df = pd.DataFrame([dic_informations])
    df.set_index('n_anonymat', inplace=True)

    # Vérifier si le fichier existe
    path_participants = resource_path('../Database/participants.xlsx')
    directory_paths["path_participants"] = path_participants

    if os.path.exists(path_participants):
        # Si le fichier existe, charger le fichier existant
        existing_df = pd.read_excel(path_participants, index_col=0)
        # Ajouter la nouvelle ligne
        updated_df = pd.concat([existing_df, df])
    else:
        # Si le fichier n'existe pas, le DataFrame est le seul contenu
        updated_df = df

    # Sauvegarder le fichier Excel
    updated_df.to_excel(path_participants)

def recolter_questionnaire(num_dict):
    """
    Récupère les informations du questionnaire dans dic_questionnaire et les met dans le fichier excel
    ../Database/sub-XX/beh/sub-XX_task_questionnaire_beh.xlsx
    Soit directory_paths["path_beh"] + /sub-XX_task_questionnaire_beh.xlsx
    """
    global dic_donnes_questionnaire

    # On transforme le dictionnaire en DataFrame

    print(f"\n\n\nOn arrive dans recolter_questionnaire avec num_dict = {num_dict}\nEt dic_donnes_questionnaire =")
    for dic in dic_donnes_questionnaire:
        print(dic)

    if num_dict != -1 :
        print("\nComme num_dict est différent de -1, on va chercher le dictionnaire correspondant car il faut le modifier")
    # On récupère le dic dont la clé est l'ID de l'incident
        for dico in dic_donnes_questionnaire:
            print(f"\nOn regarde le dico :\n{dico}")
            print(f"dico['ID'] == num_dict : {dico['ID'] == num_dict}")
            if dico["ID"] == num_dict:
                dic_pour_enregistrement = dico
                break
    else:
        dic_pour_enregistrement = dic_donnes_questionnaire[-1]

    print(f"\nLe dictionnaire à modifier est donc : \n{dic_pour_enregistrement}") # Pourquoi forcément modifier ??

    df = pd.DataFrame(dic_pour_enregistrement, index=[0])

    print(f"\n\nOn crée un DataFrame avec ce dictionnaire : \n{df}")
    df.set_index('ID', inplace=True)

    if os.path.exists(directory_paths["path_excel_beh"]):
        # Si le fichier existe, charger le fichier existant
        existing_df = pd.read_excel( directory_paths["path_excel_beh"], index_col=0)
        # Récupérer l'ID à mettre à jour ou à ajouter
        id_to_update = df.index[0]
        # Vérifier si l'ID existe déjà
        if id_to_update in list(existing_df.index):
            # Mettre à jour la ligne existante
            existing_df.loc[id_to_update] = df.iloc[0]
        else:
            # Ajouter une nouvelle ligne
            existing_df = pd.concat([existing_df, df])
    else:
        # Créer un nouveau DataFrame
        existing_df = df

        # Enregistrer le DataFrame mis à jour

    print("Nouveau fichier :{existing_df} ")

    existing_df.to_excel(directory_paths["path_excel_beh"])

def stimulation(n,minutes=0, description='') :
    """ Fonction de stimulation :

    Paramètre : 0 si l'erreur est déclarée sur le moment
                1 si l'erreur est déclarée à posteriori
                2 le moment ou l'erreur est déclarée à posteriori
                3 Ajout rapide
                4 Anulation d'une erreur
                5 Ajout d'une erreur vocale
    """

    #       Temps actuel - temps passé depuis l'erreur - du lancement du record
    #     t = 0 si sur le moment t = minutes rentrées par l'utilisateur en cas d'oubli

    temps_stim = int(time.time() - (minutes * 60) - time_code_start_recording[0])
    dernier_id = recupere_dernier_id()

    run_n = format_count_edf_files(1 + len([f for f in os.listdir(directory_paths["path_eeg"]) if f.endswith('.edf')]))

    dic_informations_incident["ID"] = dernier_id + 1
    dic_informations_incident["Path"] = f"run-{run_n}"
    dic_informations_incident["Parameter"] = n
    dic_informations_incident["ID Cible"] = '--'
    dic_informations_incident["Timecode"] = temps_stim

    if n == 2 :
        dic_informations_incident["ID Cible"] = dernier_id +2

    elif n == 3 :

        dic_donnes_questionnaire.append(dic_informations_incident.copy())

    elif n == 4 :
        dic_informations_incident["ID Cible"] = dernier_id


### Ajouter les informations dans le fichier time_codes pour open Vibe

    df = pd.read_csv(directory_paths["path_time_codes"], sep=',') # Ouvre le Excel et récupère les infos
    # print(df)

    # Ajouter à df la ligne contenant les colonnes ID, Timecode, Parameter:
    nouvelle_ligne = pd.DataFrame([dic_informations_incident]) # Création d'un nouveau DF à concatener
    nouvelle_ligne = nouvelle_ligne[["ID", "Timecode", "Parameter"]] # On garde que les colonnes ID, Timecode, Parameter

    # print(f"nouvelle ligne : \n{nouvelle_ligne}")


    df = pd.concat([df, nouvelle_ligne], ignore_index=True) # Concatenation
    df.to_csv(directory_paths["path_time_codes"], index=False) # Enregistrement

    # print(df)

#### Fichier Excel

    #TODO :
    # ID cible
    # Description rapide


    df = pd.read_excel(directory_paths["path_excel_beh"])  # Ouvre le Excel et récupère les infos
    nouvelle_ligne = pd.DataFrame([dic_informations_incident])  # Création d'un nouveau DF à concatener


    if n == 3 : # ajout de la description rapide
        nouvelle_ligne["description_incident"] = description


    # print(f"df :\n{df}\n\nligne à rajouter : \n{nouvelle_ligne}")
    df = pd.concat([df, nouvelle_ligne], ignore_index=True)  # Concatenation
    df.to_excel(directory_paths["path_excel_beh"], index=False)  # Enregistrement

def recupere_dernier_id() :
    """ Récupère le dernier ID dans le fichier excel """
    path_participants = directory_paths["path_excel_beh"]

    if os.path.exists(path_participants):
        df = pd.read_excel(path_participants)
        ids = list(df['ID'])

        if ids != [] :
            return ids[-1]
        else :
            return 0

def stop_recording():
    """ Arrête l'enregistrement EEG"""

    if process[0]:
        process[0].terminate()
        process[0] = None

    ajouter_stimulations()

def ajouter_stimulations():
    """ A la fin de l'enregistrement du rec, prends le fichier .ov et y rajoute les stimulation aux timecodes indiqués
    en differenciant les certains et les oubliés"""

    try:
        command = [openvibe_executable, "--no-gui", "--play-fast", scenario_file_Stim]
        subprocess.run(command)

        ranger_edf()  # Doit attendre que le subprocess soit terminé, mais le subprocess est à temps variable et
        # peut-être long, il faut donc qu'il s'execute uniquement une fois que la fenêtre de openvibe est partie

    except FileNotFoundError:
        print("Erreur : fichier exécutable OpenViBE introuvable.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande : {e}")

def ranger_edf():
    """ Déplace le fichier .edf dans le dossier sub-XX/eeg et le renomme
        Regarde dans le dossier directory_paths["path_eeg"], compte le nombre de fichiers .edf pour nommer le nouveau
        fichier : sub-{format_n_anonymat()}_task-work_run-{nombre_de_fichier_plus_1}_eeg.edf"
        """

    count_edf_files = len([f for f in os.listdir(directory_paths["path_eeg"]) if f.endswith('.edf')])

    path_edf_eeg = os.path.join(directory_paths["path_eeg"],
                                f"sub-{format_n_anonymat()}_task-work_run-"
                                f"{format_count_edf_files(count_edf_files + 1)}_eeg.edf")

    directory_paths["path_edf_eeg"] = path_edf_eeg


    try:
        shutil.move(path_recordStim_edf, directory_paths["path_edf_eeg"])
        print(f"Fichier déplacé et renommé avec succès à : {path_edf_eeg}")
    except FileNotFoundError:
        print("Erreur : Le fichier source n'existe pas.")
    except Exception as e:
        print(f"Erreur lors du déplacement et du renommage du fichier : {e}")

def format_count_edf_files(n):
    if n in list(range(1, 10)):
        n_formate = f"0{n}"
    else:
        n_formate = n

    return n_formate


