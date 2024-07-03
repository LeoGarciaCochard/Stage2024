
## Interface Graphique pour récupérations de données EEG sur l'ErrP

#TODO ID float dans ajout rapide

#TODO Type de travail : CODER/Ecrire/Lire..

########################################################################### Imports

import tkinter as tk
import customtkinter as ctk
import os
import shutil
import pandas as pd
import subprocess
import threading
from datetime import datetime
import time
from PIL import Image, ImageTk
from tkinter import Toplevel


########################################################################### Variables Globales

screen_width = 3072
width = 400                        #Taille de la fenêtre
height = 800                       #Taille de la fenêtre
time_start = None
temps_stim = None
id_time_code = 0
path_time_code = None
path_time_code_BackUp = None
dernier_id = None
dernier_time_code = None
dernier_parametre = None
background_color = "#2b2b2b"
row_modif = None
description_rapide = None
n_anonymat = None


dic_likert_Importance = { 0: "Insignifiante",
                         16: "Peu Importante",
                         33: "Pas Très Importante",
                         50: "Neutre",
                         66: "Assez Importante",
                         83: "Importante",
                         100: "Très Importante"}

dic_likert_Concentration ={0: "Très Faible",
                         16: "Faible",
                         33: "Plutôt Faible",
                         50.1 : ' ',
                         50: "Neutre",
                         66: "Plutôt élevé",
                         83: "Elevé",
                         100: "Très élevé"}


dic_likert_Fatigue =    { 0: "Pas fatigué",
                         16: "Très peu fatigué",
                         33: "Peu fatigué",
                         50.1 : ' ',
                         50: "Neutre",
                         66: "Plutôt fatigué",
                         83: "Fatigué",
                         100: "Vraiment fatigué"}

path_img_btn = "../Sources/btn.png"
path_img_btnf = "../Sources/btn_f.png"

path_img_aide = "../Sources/aide.png"
path_img_aidef = "../Sources/aide_f.png"
########################################################################### Lancement de l'interface

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.geometry(str(width)+'x'+str(height))
root.title("Interface Graphique ErrP")


def toggle_fullscreen(event=None):
    global fullscreen
    fullscreen = not fullscreen
    root.attributes("-fullscreen", fullscreen)
    return "break"

def end_fullscreen(event=None):
    global fullscreen
    fullscreen = False
    root.attributes("-fullscreen", False)
    return "break"

fullscreen = False
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", end_fullscreen)


########################################################################### Path

# openvibe_executable = r"C:\Program Files\openvibe-3.6.0-64bit\bin\openvibe-designer.exe"
#
# scenario_file_Ecriture = r"C:\Users\milio\PycharmProjects\Stage\OpenVibe\Scenario\EcritureEEG.xml"
# scenario_file_Stim = r"C:\Users\milio\PycharmProjects\Stage\OpenVibe\Scenario\placementStimulation.xml"
#
# record_ov = r"C:/Users/milio/PycharmProjects/Stage/OpenVibe/enregistrement_en_cours/record.ov"
#
# path_recordStim_edf = r"C:/Users/milio/PycharmProjects/Stage/OpenVibe/enregistrements_avec_stim/recordStim.edf"
# path_recordStim_ov = r"C:/Users/milio/PycharmProjects/Stage/OpenVibe/enregistrements_avec_stim/recordStim.ov"

#TODO Retirer POUR REC INFO

openvibe_executable = r""
scenario_file_Ecriture = r""
scenario_file_Stim = r""
record_ov = r""
path_recordStim_edf =r""
path_recordStim_ov = r""


########################################################################### TOOLTIP



dico_aide = {
    "Erreur" : "En cliquant sur ce bouton, vous signalez un incident. Un questionnaire s'ouvrira. \nMerci de remplir au moins la première page. Si vous avez le temps, complétez le reste. Sinon, \ncliquez sur 'Envoyer en l'état'. Vous pourrez toujours le compléter plus tard en \ncliquant sur 'Voir Récapitulatif'.",
    "Forget" : "En cliquant sur ce bouton, vous signalez un incident a posteriori, c'est-à-dire que \nvous aviez oublié de le signaler en temps voulu. Vous devez indiquer un nombre \napproximatif de minutes depuis la survenue de l'erreur. Ensuite, le questionnaire s'ouvrira \navec les mêmes instructions que pour un signalement normal.",
    "Recap"  : "En cliquant sur ce bouton, vous pourrez voir un récapitulatif des incidents déjà \nsignalés. Vous aurez la possibilité de modifier vos réponses en cliquant sur 'Modifier' \nà la ligne correspondante. Deux tableaux sont disponibles : \n--Le premier, 'Informations complétées', indique les incidents pour lesquels au moins la \npremière page est renseignée. \n--Le second, 'Informations à compléter', indique ceux qu'il vous reste à compléter, \npar exemple ceux renseignés via 'Ajout Rapide'.",
    "Rapide" : "En cliquant sur ce bouton, vous pouvez signaler un incident de manière rapide. Vous \npouvez, si vous le souhaitez, fournir une brève description (facultatif) pour vous aider à le \ncompléter plus tard. Cet incident sera placé dans le tableau 'Informations à compléter' \nsur la page du récapitulatif."
}


# Initialisation de la variable globale
tooltip_window = None


def show_tooltip(event, text):
    global tooltip_window
    if tooltip_window:
        return
    x, y = event.widget.winfo_pointerxy()
    screen_width = event.widget.winfo_screenwidth()
    tooltip_window = Toplevel(event.widget)
    tooltip_window.wm_overrideredirect(True)

    frame = ctk.CTkFrame(tooltip_window, fg_color=None)
    frame.pack()
    label = ctk.CTkLabel(frame, text=text, text_color="white", fg_color="black")
    label.pack(ipady=5, ipadx=5)

    # Obtenir la largeur de la bulle d'information
    tooltip_window.update_idletasks()
    tooltip_width = tooltip_window.winfo_width()

    # Positionner la bulle à droite ou à gauche du curseur selon la position du curseur par rapport à l'écran
    if x < screen_width / 2:
        # Positionner à droite du curseur
        tooltip_window.wm_geometry(f"+{x + 20}+{y + 20}")
    else:
        # Positionner à gauche du curseur
        tooltip_window.wm_geometry(f"+{x - tooltip_width - 20}+{y + 20}")


# Fonction pour cacher la bulle d'info lorsque la souris quitte le bouton
def hide_tooltip(event):
    global tooltip_window
    if tooltip_window:
        tooltip_window.destroy()
        tooltip_window = None



def move_tooltip(event):
    global tooltip_window
    if tooltip_window:
        x, y = event.widget.winfo_pointerxy()
        global screen_width
        tooltip_width = tooltip_window.winfo_width()

        if x <= screen_width // 2:
            # Positionner à droite du curseur
            tooltip_window.wm_geometry(f"+{x + 20}+{y + 20}")
        else:
            # Positionner à gauche du curseur
            tooltip_window.wm_geometry(f"+{x - tooltip_width - 20}+{y + 20}")


########################################################################### Logique EEG

process = None

def ranger_edf() :
    """
    récupère recordStim.edf et recordStim.ov de path_recordStim_ov et path_recordStim_edf
    les réname avec l'horodatage donné dans lancerRecEEG()
    sous le nom "Record_[NumAnonymat]_[horodatage]"
    """


    path_actuel_edf = "../OpenVibe/enregistrements_avec_stim/recordStim.edf"
    path_actuel_ov = "../OpenVibe/enregistrements_avec_stim/recordStim.ov"

    nouveau_path_edf = f"../Data/{n_anonymat}/Record_{n_anonymat}_{horodatage_start}.edf"
    nouveau_path_ov = f"../Data/{n_anonymat}/Record_{n_anonymat}_{horodatage_start}.ov"

    try:
        shutil.move(path_actuel_edf, nouveau_path_edf)
        print(f"Fichier déplacé et renommé avec succès à : {nouveau_path_edf}")
    except FileNotFoundError:
        print("Erreur : Le fichier source n'existe pas.")
    except Exception as e:
        print(f"Erreur lors du déplacement et du renommage du fichier : {e}")

    try:
        shutil.move(path_actuel_ov, nouveau_path_ov)
        print(f"Fichier déplacé et renommé avec succès à : {nouveau_path_ov}")
    except FileNotFoundError:
        print("Erreur : Le fichier source n'existe pas.")
    except Exception as e:
        print(f"Erreur lors du déplacement et du renommage du fichier : {e}")



def ajouterStim() :
    """
    A la fin de l'enregistrement du rec, prends le fichier .ov et y rajoute les stimulation aux timecodes indiqués en differenciant les certains et les oubliés
    """
    try:
        command = [openvibe_executable, "--no-gui", "--play-fast", scenario_file_Stim]
        subprocess.run(command)


        ranger_edf() #Doit attendre que le subprocess soit terminé, mais le subprocess est à temps variable et peut-être long, il faut donc qu'il s'execute uniquement une fois que la fenêtre de openvibe est partie

    except FileNotFoundError:
        print("Erreur : fichier exécutable OpenViBE introuvable.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande : {e}")



def lancerRecEEG() : #TODO lancerRecEEG
    """
        Lance l'enregistrement des signaux EEG + crée un fichier timecodes de l'enregistrement pour y spécifier les stimulations
    """
    global horodatage_start


    global time_start
    time_start = time.time()

    #Création du fichier CSV contenant les times codes qui sera lu par le code LUA pour ajouter les stimulation
    df = pd.DataFrame(columns=['id', 'timecode', 'parameter'])
    global path_time_code
    global path_time_code_BackUp

    path_time_code  = '../OpenVibe/enregistrement_en_cours/timecodes.csv'
    path_time_code_BackUp = f'../Data/{str(n_anonymat)}/timecodes_BackUp{str(n_anonymat)}_{horodatage_start}.csv'

    df.to_csv(path_time_code, index=False)
    df.to_csv(path_time_code_BackUp, index=False)


    global process
    try:
        command = [openvibe_executable, "--no-gui", "--play", scenario_file_Ecriture]
        process = subprocess.Popen(command)
    except FileNotFoundError:
        print("Erreur : fichier exécutable OpenViBE introuvable.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande : {e}")


def arreterRecEEG():
    """
    Arrête l'enregistrement des signaux EEG
    """
    global process
    if process:
        process.terminate()
        process = None
    ajouterStim()

def start_recording_thread():
    """
    Lance la fonction lancerRecEEG() dans un thread séparé
    """
    threading.Thread(target=lancerRecEEG).start()


def stimulation(parametre ,t = 0) :
    """
    Paramètre : 0 si l'erreur est déclarée sur le moment
                1 si l'erreur est déclarée à posteriori
                2 le moment ou l'erreur est déclarée à posteriori
                3 Ajout rapide
                4 Anulation, avec id cible

    t :  t = 0 si sur le moment t = minutes rentrées par l'utilisateur en cas d'oubli

    Ajoute le time code de l'erreur dans le but d'ajouter une stimulation post enregistrement
    """

    global id_time_code

    df = pd.read_csv(path_time_code)

    #       Temps actuel - temps passé depuis l'erreur - du lancement du record
    #     t = 0 si sur le moment t = minutes rentrées par l'utilisateur en cas d'oubli
    temps_stim = int(time.time() - (t*60) - time_start)



    nouvelle_ligne = pd.DataFrame({"id" : [id_time_code] , "timecode" : [temps_stim] , "parameter" : [parametre] })
    df = pd.concat([df, nouvelle_ligne], ignore_index=True)

    df.to_csv(path_time_code, index=False)
    df.to_csv(path_time_code_BackUp, index=False)

    global dernier_id
    global dernier_time_code
    global dernier_parametre
    dernier_id = id_time_code
    dernier_time_code = temps_stim
    dernier_parametre = parametre

    if parametre == 2:
        nouvelle_ligne2 = pd.DataFrame({
            "ID": [dernier_id],
            "Path": [f"../Data/{n_anonymat}/Record_{n_anonymat}_{horodatage_start}.edf"],
            "Timecode": [dernier_time_code],
            "Parameter": [dernier_parametre],
            "ID Cible" : [int(dernier_id-1)]})
        df = pd.read_excel(excel_path)
        df = pd.concat([df, nouvelle_ligne2])
        df.to_excel(excel_path, index=False)

    if parametre == 3 :

        global description_rapide

        nouvelle_ligne2 = pd.DataFrame({
            "ID": [id_time_code],
            "Path": [f"../Data/{n_anonymat}/Record_{n_anonymat}_{horodatage_start}.edf"],
            "Timecode": [dernier_time_code],
            "Parameter": [dernier_parametre],
            "Description": [description_rapide]})
        df = pd.read_excel(excel_path)
        df = pd.concat([df, nouvelle_ligne2])
        df.to_excel(excel_path, index=False)

    else :
        versQuestionnaire()

    id_time_code += 1

    print("stimulé !")




def arretExpe(acc=False) :
    """Stop l'enregistrement et ferme l'application"""
    if acc :
        root.destroy()
    else :
        # arreterRecEEG() #TODO REMETTRE POUR REC INFO
        root.destroy()


def creer_repertoire(n) :
    """
    ouvre le dossier ../Data verifie s'il existe un répertoire ../DATA/n, si oui : est-ce qu'il existe ../Data/n/n.xlsx, si oui : ne rien faire (=réouverture du dossier, en cas de crash par exemple)
                                                                        , Si non : le creer, et creer le dossier ../Data/n/n.xlsx
    :param n int: Numéro d'anonymat
    """

    global horodatage_start
    horodatage_start = datetime.now().strftime("_%Y-%m-%d_%Hh%Mm%Ss")

    path_directory = "../DATA/" + str(n)
    os.makedirs(path_directory, exist_ok=True)                                                                          #Creation du fichier n s'il n'existe pas

    global excel_path
    excel_path = os.path.join(path_directory, f"Detail_Stim_n-{n}_{horodatage_start}.xlsx")                                                              #Path du fichier excel

                    #Création du fichier Excel s'il n'existe pas déjà

    if not os.path.exists(excel_path):                  #On veérifie que le fichier n'existe pas
        colonnes = ["ID", "Path", "Timecode", "Parameter","ID Cible" , "Type","Faute", "Importance","Description",
                    "Concentration","Distrait","NatureDistraction", "Fatigue", "Difficulte"]
        df = pd.DataFrame(columns=colonnes)
        df.to_excel(excel_path, index=False)                                                                    #S'il n'éxiste pas on enregistre le fichier Excel


#Anonymat

def generer_ano() :
    df_anonymat = pd.read_excel("../Sources/info_participants.xlsx")

    #On récupère la dernière ligne de la colonne "N_ano" et ajoute 1 pour le nouveau numéro d'ano
    global n_anonymat
    n_anonymat = int(df_anonymat["N_Ano"].iloc[-1]) + 1 if not df_anonymat.empty else 1

    #Ajoute le n_anonymat à la fin du tableau

    nouvelle_ligne = pd.DataFrame({"N_Ano": [n_anonymat]})
    df_anonymat = pd.concat([df_anonymat, nouvelle_ligne], ignore_index=False)



    df_anonymat.to_excel("../Sources/info_participants.xlsx", index=False)




########################################################################### Frame 1 : Informations


def versParticipant() :

    frame_info.pack_forget()
    frame_participant.pack(pady=15, padx=30, fill="both", expand=True)





frame_info = ctk.CTkFrame(master=root)
frame_info.pack(pady=15, padx=30, fill="both", expand=True)
image_path = "../Sources/Information_R.png"
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)

#Afficher l'image dans le label
label_image = tk.Label(master=frame_info, image=photo)
label_image.pack(pady=(100,20), padx=10)

button_versB = ctk.CTkButton(master = frame_info, text="Compris !", width= 250, height=60, command=versParticipant)
button_versB.configure(font=("Helvetica", 30, "bold"))
button_versB.pack(pady=10, padx=10)

def on_enter2(event):
    button_acc_f4.configure(text="❌ Fermer")
def on_leave2(event):
    button_acc_f4.configure(text="❌")

button_acc_f4 = ctk.CTkButton(master = frame_info, text="❌", width=15, command=lambda : arretExpe(True))
button_acc_f4.configure(fg_color="red", hover_color="white", text_color="black")
button_acc_f4.pack()
button_acc_f4.place(x=5,y=5)

button_acc_f4.bind("<Enter>", on_enter2)
button_acc_f4.bind("<Leave>", on_leave2)

########################################################################### Frame 2 : Questionnaire de participant

frame_participant = ctk.CTkFrame(master=root)
# frame_participant.pack(pady=20, padx=20, fill="both", expand=True)

frame_quest_participant = ctk.CTkFrame(master=frame_participant)
frame_quest_participant.pack(pady=20, padx=20, fill="both", expand=True)

########## Dictionnaires :

dic_stress= {
    0: "Sans stress",  # 11 caractères
    16: "Pas trop stressé(e)",  # 12 caractères
    33: "Légèrement stressé(e)",  # 20 caractères
    48.5: "Neutre",  # 6 caractères
    66: "Assez stressé(e)",  # 13 caractères
    83: "Très stressé(e)",  # 12 caractères
    100: "Extrêmement stressé(e)"
}

dic_Hability_inf = {
    0: "Aucunes compétences",        # 19 caractères
    16: "Très peu compétent",          # 18 caractères
    39: "Peu compétent",        # 21 caractères
    53: "Moyen",          # 18 caractères
    66: "Compétent",                   # 9 caractères
    83: "Très compétent",              # 15 caractères
    100: "Extrêmement compétent"       # 22 caractères
}

dic_Passion = {
    0: "Pas du tout passionné(e)",        # 20 caractères
    16: "Très peu passionné(e)",          # 18 caractères
    33: "Peu passionné(e)",        # 21 caractères
    50: "Passion neutre(e)",              # 14 caractères
    66: "Légèrement passionné(e)",                   # 9 caractères
    83: "Très passionné(e)",              # 15 caractères
    100: "Extrêmement passionné(e)"       # 22 caractères
}


dic_Bruit = {
    0: "Pas du tout bruyant",          # 19 caractères
    16: "Très peu bruyant",            # 16 caractères
    33: "Légèrement bruyant",          # 20 caractères
    53.5: "Normal",                # 12 caractères
    66: "Assez bruyant",               # 13 caractères
    83: "Très bruyant",                # 12 caractères
    100: "Extrêmement bruyant"         # 21 caractères
}

########## Variables :

selected_var_heure = datetime.now().strftime("%Hh%M")

##Informations personnelles :

selected_var_age = tk.StringVar()
selected_var_genre = tk.StringVar()

##Informations de contexte :

selected_var_sommeil = tk.StringVar()
selected_var_trouble_sommeil = tk.StringVar()
selected_var_stress = dic_stress[48.5]

selected_var_cafeine = tk.StringVar()
selected_var_quantite_cafeine = 0

selected_var_nicotine = tk.StringVar()
selected_var_quantite_nicotine = 0

##Travail :

selected_var_Hability_inf = dic_Hability_inf[53]
selected_var_experience = tk.StringVar()
selected_var_Passion = dic_Passion[50]

# selected_var_distractions_travail = tk.StringVar()
selected_var_Bruit = dic_Bruit[53.5]


####################################### TODO A SUPRUMER

selected_var_age = 22
selected_var_genre = "Homme"

##Informations de contexte :

selected_var_sommeil = 7
selected_var_trouble_sommeil = "Non"
selected_var_stress = dic_stress[48.5]

selected_var_cafeine = "Oui"
selected_var_quantite_cafeine = 10

selected_var_nicotine = "Non"
selected_var_quantite_nicotine = 0

##Travail :

selected_var_Hability_inf = dic_Hability_inf[53]
selected_var_experience = "+de 10"
selected_var_Passion = dic_Passion[50]

selected_var_Bruit = dic_Bruit[53.5]



########## Titre :

cadre_participantTitre = ctk.CTkFrame(master=frame_quest_participant)
cadre_participantTitre.pack(pady=25, padx=50)

label_participantTitre = ctk.CTkLabel(master= cadre_participantTitre, text="Merci de remplir ces informations anonymes")
label_participantTitre.pack(pady=10, padx=50)
label_participantTitre.configure(font=("Helvetica", 35,"bold"))


########## Titre IP (Info Perso) :

cadre_participantIP = ctk.CTkFrame(master=frame_quest_participant)
cadre_participantIP.pack(pady=10, padx=50)

label_participantIP = ctk.CTkLabel(master= cadre_participantIP, text="Informations personelles :")
label_participantIP.pack(pady=5, padx=50)
label_participantIP.configure(font=("Helvetica", 15))

########## Age :

def on_enter_label(label):
    label.configure(fg_color="#474545")

def on_exit_label(label):
    label.configure(fg_color="#242424")

def ouvrir_menu_age() :
    """
    Crée une nouvelle fenêtre et ouvrer un menu déroulant
    """
    global selected_var_age

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    menu = ctk.CTk()
    menu.title("Exemple avec CTk")
    menu.geometry("100x300")

    scrollable_frame = ctk.CTkScrollableFrame(master=menu)
    scrollable_frame.pack(fill="both", expand=True)

    for n in range(18, 100):
        label_age = ctk.CTkLabel(master=scrollable_frame, text=str(n), cursor="hand2", fg_color="#242424",
                                 corner_radius=10)
        label_age.pack(pady=3, padx=3, fill="both")

        label_age.bind("<Enter>", lambda event, label=label_age: on_enter_label(label))
        label_age.bind("<Leave>", lambda event, label=label_age: on_exit_label(label))
        label_age.bind("<Button-1>", lambda event, age=n: (set_selected_age(age), menu.destroy()))

    menu.mainloop()

def set_selected_age(age):
    global selected_var_age
    selected_var_age = age
    label_box_age.configure(text=f"Veuillez cliquer ici pour renseigner votre âge :   {str(selected_var_age)}")

frame_age= ctk.CTkFrame(master=frame_quest_participant)
frame_age.pack(padx= 50, pady=10, fill="both")

label_box_age = ctk.CTkLabel(master=frame_age, text="Veuillez cliquer ici pour renseigner votre âge :   ...", cursor="hand2")
label_box_age.grid(row=0,column=0, ipadx=5, ipady=5)
label_box_age.bind("<Button-1>", command=lambda x: ouvrir_menu_age())


########## Genre :

def change_genre(genre):
    global selected_var_genre
    selected_var_genre = genre

frame_genre = ctk.CTkFrame(master=frame_quest_participant)
frame_genre.pack(padx= 50, pady=10, fill="both")

label_genre = ctk.CTkLabel(master=frame_genre, text="Veuillez renseigner votre genre : ")
label_genre.grid(row=0,column=0, ipadx=5, ipady=5)

combobox_genre = ctk.CTkComboBox(master=frame_genre, values=["Femme","Homme","Autre"], state="readonly", command= lambda x : change_genre(x))
combobox_genre.grid(row=0,column=1)

########## Situation personelle :

########## Titre SP (Situation personelle) :

cadre_participantSP = ctk.CTkFrame(master=frame_quest_participant)
cadre_participantSP.pack(pady=10, padx=50)

label_participantSP = ctk.CTkLabel(master= cadre_participantSP, text="Situation personelle :")
label_participantSP.pack(pady=5, padx=50)
label_participantSP.configure(font=("Helvetica", 15))

########## Sommeil :

frame_sommeil = ctk.CTkFrame(master=frame_quest_participant)
frame_sommeil.pack(padx= 50, pady=10, fill="both")

## Temps de sommeil :

def change_sommeil(heure):
    global selected_var_sommeil
    selected_var_sommeil = heure

label_sommeil = ctk.CTkLabel(master=frame_sommeil, text="Combien d'heures avez-vous dormis cette nuit : ")
label_sommeil.grid(row=0,column=0, ipadx=5, ipady=5)

combobox_genre = ctk.CTkComboBox(master=frame_sommeil, values=["Nuit blanche","Moins de 3h","4h","5h","6h","7h","8h","Plus de 9h"], state="readonly", command= lambda x : change_sommeil(x))
combobox_genre.grid(row=0,column=1)

## Troubles du sommeil :

def change_troubles_sommeil(rep):
    global selected_var_trouble_sommeil
    selected_var_trouble_sommeil = rep

label_sommeil = ctk.CTkLabel(master=frame_sommeil, text="Souffrez vous de troubles du sommeil : ")
label_sommeil.grid(row=1,column=0, ipadx=5, ipady=5)

combobox_sommeil = ctk.CTkComboBox(master=frame_sommeil, values=["Oui","Non"], state="readonly", command= lambda x : change_troubles_sommeil(x))
combobox_sommeil.grid(row=1,column=1)

########## Stress :

def magnet_likert_Stress(valeur_actuelle) :
    """Magnetise la valeur à la plus proche sur l'echelle de likert """
    liste = [0, 16 , 33 , 48.5, 66, 83, 100]

    nouvelle_val = min(liste, key=lambda val: abs(val - valeur_actuelle))
    sliderStress.set(nouvelle_val)
    global selected_var_stress
    selected_var_stress= dic_stress[nouvelle_val]


frame_Stress = ctk.CTkFrame(master=frame_quest_participant)
frame_Stress.pack(pady=10, padx=50, fill="both")

label_Stress = ctk.CTkLabel(master = frame_Stress,text="De manière générale, comment décrivez vous votre état de stress")
label_Stress.pack(pady=10)
label_Stress.configure(font=("Helvetica", 15))

###Slider

cadreStress = ctk.CTkFrame(master=frame_Stress)
cadreStress.pack(anchor=tk.CENTER, pady=10)


label_Stress_0 = ctk.CTkLabel(master = cadreStress,text=dic_stress[0])
label_Stress_0.grid(row=0, column=0, padx=10)
label_Stress_0.configure(font=("Helvetica",13),text_color='green')

label_Stress_1 = ctk.CTkLabel(master = cadreStress,text=dic_stress[16])
label_Stress_1.grid(row=0, column=1, padx=10)
label_Stress_1.configure(font=("Helvetica",13),text_color='green')

label_Stress_2 = ctk.CTkLabel(master = cadreStress,text=dic_stress[33])
label_Stress_2.grid(row=0, column=2, padx=10)
label_Stress_2.configure(font=("Helvetica",13),text_color='green')

label_Stress_3 = ctk.CTkLabel(master = cadreStress,text=dic_stress[48.5])
label_Stress_3.grid(row=0, column=3, padx=10)
label_Stress_3.configure(font=("Helvetica",13),text_color='white')


label_Stress_4 = ctk.CTkLabel(master = cadreStress,text=dic_stress[66])
label_Stress_4.grid(row=0, column=4, padx=10)
label_Stress_4.configure(font=("Helvetica",13),text_color='red')

label_Stress_5 = ctk.CTkLabel(master = cadreStress,text=dic_stress[83])
label_Stress_5.grid(row=0, column=5, padx=10)
label_Stress_5.configure(font=("Helvetica",13),text_color='red')

label_Stress_6 = ctk.CTkLabel(master = cadreStress,text=dic_stress[100])
label_Stress_6.grid(row=0, column=6, padx=10)
label_Stress_6.configure(font=("Helvetica",13),text_color='red')

sliderStress = ctk.CTkSlider(master = frame_Stress, from_=0, to=100, width=700, command=magnet_likert_Stress)
sliderStress.pack()
sliderStress.set(48.5)

######### Caféine

frame_cafeine = ctk.CTkFrame(master=frame_quest_participant)
frame_cafeine.pack(padx= 50, pady=10, fill="both")
def change_cafeine(rep):
    global selected_var_cafeine
    selected_var_cafeine = rep

    #Actver la quantité si rep == oui
    if rep == "Oui" :
        combobox_quantite_cafeine.configure(state='readonly')
        combobox_quantite_cafeine.set("0")
    #Sinon remettre en disabled et réinitialiser la valeur
    else :
        combobox_quantite_cafeine.set("0")
        combobox_quantite_cafeine.configure(state='disabled')
        global selected_var_quantite_cafeine
        selected_var_quantite_cafeine = 0
def change_tasses_cafeine(rep):
    global selected_var_quantite_cafeine
    selected_var_quantite_cafeine = rep

label_cafeine = ctk.CTkLabel(master=frame_cafeine, text="Consommez vous de la cafeine : ")
label_cafeine.grid(row=0,column=0, ipadx=5, ipady=5)

combobox_cafeine = ctk.CTkComboBox(master=frame_cafeine, values=["Oui","Non"], state="readonly", command= lambda x : change_cafeine(x))
combobox_cafeine.grid(row=0,column=1)

label_cafeine = ctk.CTkLabel(master=frame_cafeine, text="Si oui, combien de tasses par jours : ")
label_cafeine.grid(row=1,column=0, ipadx=20, ipady=5)

combobox_quantite_cafeine = ctk.CTkComboBox(master=frame_cafeine, values=["0","1","2","3","4","Plus de 5"], state="disabled", command= lambda x : change_tasses_cafeine(x))
combobox_quantite_cafeine.grid(row=1,column=1)


######### Nicotine

frame_nicotine = ctk.CTkFrame(master=frame_quest_participant)
frame_nicotine.pack(padx= 50, pady=10, fill="both")
def change_nicotine(rep):
    global selected_var_nicotine
    selected_var_nicotine = rep

    #Actver la quantité si rep == oui
    if rep == "Oui" :
        combobox_quantite_nicotine.configure(state='readonly')
        combobox_quantite_nicotine.set("0")
    #Sinon remettre en disabled et réinitialiser la valeur
    else :
        combobox_quantite_nicotine.set("0")
        combobox_quantite_nicotine.configure(state='disabled')
        global selected_var_quantite_nicotine
        selected_var_quantite_nicotine = 0
def change_cigarettes_nicotine(rep):
    global selected_var_quantite_nicotine
    selected_var_quantite_nicotine = rep

label_nicotine = ctk.CTkLabel(master=frame_nicotine, text="Consommez vous de la nicotine : ")
label_nicotine.grid(row=0,column=0, ipadx=5, ipady=5)

combobox_nicotine = ctk.CTkComboBox(master=frame_nicotine, values=["Oui","Non"], state="readonly", command= lambda x : change_nicotine(x))
combobox_nicotine.grid(row=0,column=1)

label_nicotine = ctk.CTkLabel(master=frame_nicotine, text="Si oui, combien de cigarettes (ou équivalent) par jours : ")
label_nicotine.grid(row=1,column=0, ipadx=20, ipady=5)

combobox_quantite_nicotine = ctk.CTkComboBox(master=frame_nicotine, values=["0","1","2","3","4","Plus de 5"], state="disabled", command= lambda x : change_cigarettes_nicotine(x))
combobox_quantite_nicotine.grid(row=1,column=1)


def versPart2():
    frame_quest_participant.pack_forget()
    frame_quest_participant2.pack(pady=20, padx=20, fill="both", expand=True)


button_part2 = ctk.CTkButton(master=frame_quest_participant, text="Suivant", width=250, height=60, command=versPart2)
button_part2.configure(font=("Helvetica", 20, "bold"))
button_part2.pack(pady=10, padx=10, side=tk.BOTTOM)






##########PAGE 2

frame_quest_participant2 = ctk.CTkFrame(master=frame_participant)

def versPart1():
    frame_quest_participant2.pack_forget()
    frame_quest_participant.pack(pady=20, padx=20, fill="both", expand=True)


button_part1 = ctk.CTkButton(master=frame_quest_participant2, text="Retour", width=200, height=30, command=versPart1)
button_part1.configure(font=("Helvetica", 20, "bold"))
button_part1.pack(pady=10, padx=10)


def on_enter3(event):
    button_participant_f4.configure(text="❌ Fermer")
def on_leave3(event):
    button_participant_f4.configure(text="❌")

button_participant_f4 = ctk.CTkButton(master = frame_quest_participant, text="❌", width=15, command=lambda : arretExpe(True))
button_participant_f4.configure(fg_color="red", hover_color="white", text_color="black")
button_participant_f4.place(x=5,y=5)

button_participant_f4.bind("<Enter>", on_enter3)
button_participant_f4.bind("<Leave>", on_leave3)


def forget_retour_normal() :
    entry_forgotten.delete(0, tk.END)
    frame_button_cadre.pack_forget()
    aide_button_forget.pack_forget()

    button_errForget.pack(padx=10,side=tk.LEFT)
    aide_button_forget.pack(side=tk.LEFT)


def pack_button_tout() :

    #On unpack tout
    frame_button_err.pack_forget()
    frame_button_forget.pack_forget()
    frame_button_recap.pack_forget()
    frame_button_rapide.pack_forget()

    # On repack dans l'ordre
    frame_button_err.pack(pady=((height / 2) - 200, 0), anchor='center')
    frame_button_forget.pack(pady=10, anchor='center')
    frame_button_recap.pack(pady=10, anchor='center')
    frame_button_rapide.pack(pady=10, anchor='center')

    #Repacker forget et rapide dans le bon sens

    forget_retour_normal()
    unpack_textbox()




########## Situation Professionelle :

########## Titre SPro (Situation Professionelle) :

cadre_participantSPro = ctk.CTkFrame(master=frame_quest_participant2)
cadre_participantSPro.pack(pady=(30,10), padx=50)

label_participantSPro = ctk.CTkLabel(master= cadre_participantSPro, text="Situation professionelle :")
label_participantSPro.pack(pady=5, padx=50)
label_participantSPro.configure(font=("Helvetica", 15))

########## expérience :

frame_experience = ctk.CTkFrame(master=frame_quest_participant2)
frame_experience.pack(padx= 50, pady=10, fill="both")

def change_expe_travail(rep):
    global selected_var_experience
    selected_var_experience = rep

label_expe = ctk.CTkLabel(master=frame_experience, text="Depuis combien de temps faites-vous ce travail ?")
label_expe.grid(row=1,column=0, ipadx=5, ipady=5)

combobox_expe = ctk.CTkComboBox(master=frame_experience, values=["Moins d'un an", "2 ans", "3 ans"," 4 ans", "plus de 5 ans", "plus de 10 ans"], state="readonly", command= lambda x : change_expe_travail(x))
combobox_expe.grid(row=1,column=1)


########## Habilité informatique :

def magnet_likert_Hability_inf(valeur_actuelle) :
    """Magnetise la valeur à la plus proche sur l'echelle de likert """
    liste = [0, 16 , 39 , 53, 66, 83, 100]

    nouvelle_val = min(liste, key=lambda val: abs(val - valeur_actuelle))
    sliderHability_inf.set(nouvelle_val)
    global selected_var_Hability_inf
    selected_var_Hability_inf= dic_Hability_inf[nouvelle_val]


frame_Hability_inf = ctk.CTkFrame(master=frame_quest_participant2)
frame_Hability_inf.pack(pady=10, padx=50, fill="both")

label_Hability_inf = ctk.CTkLabel(master = frame_Hability_inf,text="A quel point êtes vous à l'aise avec les outils informatiques : ")
label_Hability_inf.pack(pady=10)
label_Hability_inf.configure(font=("Helvetica", 15))

###Slider

cadreHability_inf = ctk.CTkFrame(master=frame_Hability_inf)
cadreHability_inf.pack(anchor=tk.CENTER, pady=10)


label_Hability_inf_0 = ctk.CTkLabel(master = cadreHability_inf,text=dic_Hability_inf[0])
label_Hability_inf_0.grid(row=0, column=0, padx=10)
label_Hability_inf_0.configure(font=("Helvetica",13),text_color='green')

label_Hability_inf_1 = ctk.CTkLabel(master = cadreHability_inf,text=dic_Hability_inf[16])
label_Hability_inf_1.grid(row=0, column=1, padx=10)
label_Hability_inf_1.configure(font=("Helvetica",13),text_color='green')

label_Hability_inf_2 = ctk.CTkLabel(master = cadreHability_inf,text=dic_Hability_inf[39])
label_Hability_inf_2.grid(row=0, column=2, padx=10)
label_Hability_inf_2.configure(font=("Helvetica",13),text_color='green')

label_Hability_inf_3 = ctk.CTkLabel(master = cadreHability_inf,text=dic_Hability_inf[53])
label_Hability_inf_3.grid(row=0, column=3, padx=10)
label_Hability_inf_3.configure(font=("Helvetica",13),text_color='white')


label_Hability_inf_4 = ctk.CTkLabel(master = cadreHability_inf,text=dic_Hability_inf[66])
label_Hability_inf_4.grid(row=0, column=4, padx=10)
label_Hability_inf_4.configure(font=("Helvetica",13),text_color='red')

label_Hability_inf_5 = ctk.CTkLabel(master = cadreHability_inf,text=dic_Hability_inf[83])
label_Hability_inf_5.grid(row=0, column=5, padx=10)
label_Hability_inf_5.configure(font=("Helvetica",13),text_color='red')

label_Hability_inf_6 = ctk.CTkLabel(master = cadreHability_inf,text=dic_Hability_inf[100])
label_Hability_inf_6.grid(row=0, column=6, padx=10)
label_Hability_inf_6.configure(font=("Helvetica",13),text_color='red')

sliderHability_inf = ctk.CTkSlider(master = frame_Hability_inf, from_=0, to=100, width=600, command=magnet_likert_Hability_inf)
sliderHability_inf.pack()
sliderHability_inf.set(53)


########## Passion :

def magnet_likert_Passion(valeur_actuelle) :
    """Magnetise la valeur à la plus proche sur l'echelle de likert """
    liste = [0, 16 , 33 , 50, 66, 83, 100]

    nouvelle_val = min(liste, key=lambda val: abs(val - valeur_actuelle))
    sliderPassion.set(nouvelle_val)
    global selected_var_Passion
    selected_var_Passion= dic_Passion[nouvelle_val]


frame_Passion = ctk.CTkFrame(master=frame_quest_participant2)
frame_Passion.pack(pady=10, padx=50, fill="both")

label_Passion = ctk.CTkLabel(master = frame_Passion,text="A quel point aimez-vous ce travail ?: ")
label_Passion.pack(pady=10)
label_Passion.configure(font=("Helvetica", 15))

###Slider

cadrePassion = ctk.CTkFrame(master=frame_Passion)
cadrePassion.pack(anchor=tk.CENTER, pady=10)


label_Passion_0 = ctk.CTkLabel(master = cadrePassion,text=dic_Passion[0])
label_Passion_0.grid(row=0, column=0, padx=10)
label_Passion_0.configure(font=("Helvetica",13),text_color='green')

label_Passion_1 = ctk.CTkLabel(master = cadrePassion,text=dic_Passion[16])
label_Passion_1.grid(row=0, column=1, padx=10)
label_Passion_1.configure(font=("Helvetica",13),text_color='green')

label_Passion_2 = ctk.CTkLabel(master = cadrePassion,text=dic_Passion[33])
label_Passion_2.grid(row=0, column=2, padx=10)
label_Passion_2.configure(font=("Helvetica",13),text_color='green')

label_Passion_3 = ctk.CTkLabel(master = cadrePassion,text=dic_Passion[50])
label_Passion_3.grid(row=0, column=3, padx=10)
label_Passion_3.configure(font=("Helvetica",13),text_color='white')


label_Passion_4 = ctk.CTkLabel(master = cadrePassion,text=dic_Passion[66])
label_Passion_4.grid(row=0, column=4, padx=10)
label_Passion_4.configure(font=("Helvetica",13),text_color='red')

label_Passion_5 = ctk.CTkLabel(master = cadrePassion,text=dic_Passion[83])
label_Passion_5.grid(row=0, column=5, padx=10)
label_Passion_5.configure(font=("Helvetica",13),text_color='red')

label_Passion_6 = ctk.CTkLabel(master = cadrePassion,text=dic_Passion[100])
label_Passion_6.grid(row=0, column=6, padx=10)
label_Passion_6.configure(font=("Helvetica",13),text_color='red')

sliderPassion = ctk.CTkSlider(master = frame_Passion, from_=0, to=100, width=800, command=magnet_likert_Passion)
sliderPassion.pack()
sliderPassion.set(50)




########## Envorinemment de travail :

########## Titre ET (Envorinemment de travail) :

cadre_participantET = ctk.CTkFrame(master=frame_quest_participant2)
cadre_participantET.pack(pady=(40,10), padx=50)

label_participantET = ctk.CTkLabel(master= cadre_participantET, text="Envorinemment de travail :")
label_participantET.pack(pady=5, padx=50)
label_participantET.configure(font=("Helvetica", 15))


########## Bruit environnant :

def magnet_likert_Bruit(valeur_actuelle) :
    """Magnetise la valeur à la plus proche sur l'echelle de likert """
    liste = [0, 16 , 33 , 53.5, 66, 83, 100]

    nouvelle_val = min(liste, key=lambda val: abs(val - valeur_actuelle))
    sliderBruit.set(nouvelle_val)
    global selected_var_Bruit
    selected_var_Bruit= dic_Bruit[nouvelle_val]


frame_Bruit = ctk.CTkFrame(master=frame_quest_participant2)
frame_Bruit.pack(pady=10, padx=53.5, fill="both")

label_Bruit = ctk.CTkLabel(master = frame_Bruit,text="Le niveau de bruit dans votre environnement de travail est : ")
label_Bruit.pack(pady=10)
label_Bruit.configure(font=("Helvetica", 15))

###Slider

cadreBruit = ctk.CTkFrame(master=frame_Bruit)
cadreBruit.pack(anchor=tk.CENTER, pady=10)


label_Bruit_0 = ctk.CTkLabel(master = cadreBruit,text=dic_Bruit[0])
label_Bruit_0.grid(row=0, column=0, padx=10)
label_Bruit_0.configure(font=("Helvetica",13),text_color='green')

label_Bruit_1 = ctk.CTkLabel(master = cadreBruit,text=dic_Bruit[16])
label_Bruit_1.grid(row=0, column=1, padx=10)
label_Bruit_1.configure(font=("Helvetica",13),text_color='green')

label_Bruit_2 = ctk.CTkLabel(master = cadreBruit,text=dic_Bruit[33])
label_Bruit_2.grid(row=0, column=2, padx=10)
label_Bruit_2.configure(font=("Helvetica",13),text_color='green')

label_Bruit_3 = ctk.CTkLabel(master = cadreBruit,text=dic_Bruit[53.5])
label_Bruit_3.grid(row=0, column=3, padx=10)
label_Bruit_3.configure(font=("Helvetica",13),text_color='white')


label_Bruit_4 = ctk.CTkLabel(master = cadreBruit,text=dic_Bruit[66])
label_Bruit_4.grid(row=0, column=4, padx=10)
label_Bruit_4.configure(font=("Helvetica",13),text_color='red')

label_Bruit_5 = ctk.CTkLabel(master = cadreBruit,text=dic_Bruit[83])
label_Bruit_5.grid(row=0, column=5, padx=10)
label_Bruit_5.configure(font=("Helvetica",13),text_color='red')

label_Bruit_6 = ctk.CTkLabel(master = cadreBruit,text=dic_Bruit[100])
label_Bruit_6.grid(row=0, column=6, padx=10)
label_Bruit_6.configure(font=("Helvetica",13),text_color='red')

sliderBruit = ctk.CTkSlider(master = frame_Bruit, from_=0, to=100, width=653.5, command=magnet_likert_Bruit)
sliderBruit.pack()
sliderBruit.set(53.5)


######### Bouton + Vérif
# n_anonymat = 1


def validate_variables():
    variables = [
        selected_var_age,
        selected_var_genre,
        selected_var_sommeil,
        selected_var_trouble_sommeil,
        selected_var_cafeine,
        selected_var_nicotine,
        selected_var_experience
    ]
    i= 0
    for var in variables:
        if type(var) == int or type(var)== str :
            i+=1

    if i == 7 :
        return True
    else :
        return False

def versBouton() :
    """
    Récupère les données de l'utilisateur
    Donne un numéro de candidat
    Crée le répertoire
    stock les données utilisateur dans un csv
    lance le rec
    Affiche la page suivante
    """



    if validate_variables() :

        # recuperation_donnees_participant
        generer_ano()

        df = pd.read_excel("../Sources/info_participants.xlsx", index_col='N_Ano')
        global n_anonymat

        nouvelle_ligne ={
            "N_Ano" : n_anonymat,
            "Heure" : selected_var_heure,
            "Age" : selected_var_age,
            "Genre" : selected_var_genre,

            "Sommeil"  : selected_var_sommeil,
            "Troubles du sommeil"  : selected_var_trouble_sommeil,
            "Stress" : selected_var_stress,

            "Caféine"   : selected_var_cafeine,
            "Quantité de caféine"  : selected_var_quantite_cafeine,

            "Nicotine" : selected_var_nicotine,
            "Quantité de nicotine" : selected_var_quantite_nicotine,

            "Maîtrise de l'informatique"  : selected_var_Hability_inf,
            "Experience" : selected_var_experience,
            "Passion"  : selected_var_Passion,
            "Bruit"  : selected_var_Bruit
        }
        df.loc[n_anonymat] = nouvelle_ligne
        df.to_excel("../Sources/info_participants.xlsx", index=True)

        # versBouton
        creer_repertoire(n_anonymat)

        # Stock les données

        start_recording_thread()

        # Afficher page bouton

        frame_participant.pack_forget()
        frame_button.pack(pady=20, padx=50, fill="both", expand=True)

        pack_button_tout()

    else :
        print("Pas bien")

button_versB = ctk.CTkButton(master = frame_quest_participant2, text="Terminé !", width= 250, height=60, command=versBouton)
button_versB.configure(font=("Helvetica", 20, "bold"))
button_versB.pack(pady=10, padx=10,side=tk.BOTTOM)

def on_enter4(event):
    button_participant_f4_2.configure(text="❌ Fermer")
def on_leave4(event):
    button_participant_f4_2.configure(text="❌")

button_participant_f4_2 = ctk.CTkButton(master = frame_quest_participant2, text="❌", width=15, command=lambda : arretExpe(True))
button_participant_f4_2.configure(fg_color="red", hover_color="white", text_color="black")
button_participant_f4_2.place(x=5,y=5)

button_participant_f4_2.bind("<Enter>", on_enter4)
button_participant_f4_2.bind("<Leave>", on_leave4)




########################################################################### Frame 2 : Page d'utilisateur avec bouton

def forgottenErr1() :

#On unpack le bouton j'ai oublié
    button_errForget.pack_forget()

#On retir l'aide et le bouton
    aide_button_forget.pack_forget()
    frame_button_cadre.pack(pady=10, padx=10)

#On affiche la frame contenant l'entry et le bouton valider, ainsi que l'aide au bon endroit
    frame_button_cadre.pack(padx=10,side=tk.LEFT)
    aide_button_forget.pack(side=tk.LEFT)

#Si jamais la description rapide du bouton ajout rapide est affichée, on l'enlève
    unpack_textbox()


def forgottenErr2() :

    try :
        s = int(entry_forgotten.get())
        temps_stim = int(time.time() - (s * 60) - time_start)
        if isinstance(s, int) and temps_stim >= 0 :
            stimulation(2)  # Stimulation au moment du signalement de l'oubli
            stimulation(1,s) #Stimulation dans le passé
            button_errForget.pack(pady=10, padx=10)
            frame_button_cadre.pack_forget()
            entry_forgotten.delete(0, tk.END)
        else :
            print(f"Temps non valide")
    except Exception as e :
        print(f"Temps non valide : {e}")


def versQuestionnaire() :       #Changer de page vers page3 : Questionnaire
    """Retire la page bouton et affiche le questionnaire"""

    # Retier la page bouton
    frame_button.pack_forget()

    frame_quest.pack(pady=20, padx=50, fill="both", expand=True)

    creation_boutons_type()
    Concentration_Type()




################################################--Frame Bouton

frame_button = ctk.CTkFrame(master=root)

#########--BOUTON ERR PRINCIPAL

frame_button_err = ctk.CTkFrame(master = frame_button, fg_color="#2b2b2b")

button_err = ctk.CTkButton(master = frame_button_err, text="Renseigner un incident négatif",command=lambda : stimulation(0))
button_err.configure(height=200, width=200, corner_radius=20, font=("Helvetica", 30, "bold") )

#AIDE Button ERR

def Enter_aide1(event) :
    """Grise le help et fait apparaitre une tooltip avec une description"""
    aide_button_err.configure(image=photo_aide_button_errf)
    # afficher_bulle_1()
    show_tooltip(event,dico_aide["Erreur"])


def Leave_aide1(event) :
    aide_button_err.configure(image=photo_aide_button_err)
    hide_tooltip(event)

image_aide_button_err = Image.open(path_img_aide)
image_aide_button_err_resized = image_aide_button_err.resize((100, 100), Image.LANCZOS)
photo_aide_button_err = ctk.CTkImage(dark_image=image_aide_button_err_resized, size=(20, 20))

image_aide_button_errf = Image.open(path_img_aidef)
image_aide_button_errf_resized = image_aide_button_errf.resize((100, 100), Image.LANCZOS)
photo_aide_button_errf = ctk.CTkImage(light_image=image_aide_button_errf_resized, dark_image=image_aide_button_errf_resized, size=(20, 20))

# Afficher l'image dans un label
aide_button_err = ctk.CTkLabel(master=frame_button_err, image=photo_aide_button_err ,text='', cursor="hand2")
aide_button_err.configure(font=('Helvetica',15))

aide_button_err.bind("<Enter>", Enter_aide1)
aide_button_err.bind("<Leave>", Leave_aide1)
aide_button_err.bind("<Motion>", move_tooltip)


button_err.pack(pady=0, padx=10,side=tk.LEFT)
aide_button_err.pack(side=tk.LEFT,pady=100)






#TODO AjoutRapide stimulation

def unpack_textbox() :
    textbox_description.delete(0,tk.END)
    textbox_description.pack_forget()
    textbov_validation.pack_forget()

    label_image_btn.pack_forget()
    aide_button_rapide.pack_forget()
    label_image_btn.pack(pady=(15, 10), padx=(0, 105), side=tk.LEFT)
    aide_button_rapide.pack(side=tk.LEFT)

def pack_text_box() :

#On retire tout
    label_image_btn.pack_forget()
    aide_button_rapide.pack_forget()

#On pack dans le bon ordre
    textbox_description.pack(pady=10, padx=10,side=tk.LEFT)
    textbov_validation.pack(pady=10, padx=10,side=tk.LEFT)
    aide_button_rapide.pack(side=tk.LEFT)

#On remets forget fermé si jamais :
    forget_retour_normal()

def recup_desc() :
    # Récupère la description :
    global description_rapide
    description_rapide = textbox_description.get().strip()


    #Stimule :
    stimulation(3)
    #Remets les boutons
    unpack_textbox()
    aide_button_rapide.pack_forget()
    label_image_btn.pack(pady=(15, 10), padx=(0, 105), side=tk.LEFT)
    aide_button_rapide.pack(side=tk.LEFT)



frame_button_rapide = ctk.CTkFrame(master=frame_button,fg_color="#2b2b2b")

textbox_description = ctk.CTkEntry(master= frame_button_rapide, width= 200, placeholder_text="Rapide description...")
textbov_validation = ctk.CTkButton(master = frame_button_rapide, text= "Valider ou Ignorer", command=recup_desc)



def on_enter3(event):
    label_image_btn.configure(image=photo_btnf)
def on_leave3(event):
    label_image_btn.configure(image=photo_btn)


image_btn = Image.open(path_img_btn)
image_btn_resized = image_btn.resize((100, 100), Image.LANCZOS)
photo_btn = ctk.CTkImage(light_image=image_btn_resized, dark_image=image_btn_resized, size=(55, 55))

image_btnf = Image.open(path_img_btnf)
image_btnf_resized = image_btnf.resize((100, 100), Image.LANCZOS)
photo_btnf = ctk.CTkImage(light_image=image_btnf_resized, dark_image=image_btnf_resized, size=(55, 55))

# Afficher l'image dans un label
label_image_btn = ctk.CTkLabel(master=frame_button_rapide, image=photo_btn ,text='                                        Ajout Rapide', cursor="hand2")
label_image_btn.configure(font=('Helvetica',15))


label_image_btn.bind("<Button-1>", command=lambda x: pack_text_box())
label_image_btn.bind("<Enter>", on_enter3)
label_image_btn.bind("<Leave>", on_leave3)

#AIDE Button Rapide

def Enter_aide4(event) :
    """Grise le help et fait apparaitre une tooltip avec une description"""
    aide_button_rapide.configure(image=photo_aide_button_rapidef)
    show_tooltip(event, dico_aide["Rapide"])


def Leave_aide4(event) :
    aide_button_rapide.configure(image=photo_aide_button_rapide)
    hide_tooltip(event)


image_aide_button_rapide = Image.open(path_img_aide)
image_aide_button_rapide_resized = image_aide_button_rapide.resize((100, 100), Image.LANCZOS)
photo_aide_button_rapide = ctk.CTkImage(dark_image=image_aide_button_rapide_resized, size=(20, 20))

image_aide_button_rapidef = Image.open(path_img_aidef)
image_aide_button_rapidef_resized = image_aide_button_rapidef.resize((100, 100), Image.LANCZOS)
photo_aide_button_rapidef = ctk.CTkImage(light_image=image_aide_button_rapidef_resized, dark_image=image_aide_button_rapidef_resized, size=(20, 20))

# Afficher l'image dans un label
aide_button_rapide = ctk.CTkLabel(master=frame_button_rapide, image=photo_aide_button_rapide ,text='', cursor="hand2")
aide_button_rapide.configure(font=('Helvetica',15))

aide_button_rapide.bind("<Enter>", Enter_aide4)
aide_button_rapide.bind("<Leave>", Leave_aide4)
aide_button_rapide.bind("<Motion>", move_tooltip)


label_image_btn.pack(pady=(15, 10), padx=(0, 105),side=tk.LEFT)
aide_button_rapide.pack(side=tk.LEFT)



###############--Bouton forget

frame_button_forget = ctk.CTkFrame(master= frame_button,fg_color="#2b2b2b")

frame_button_cadre = ctk.CTkFrame(master=frame_button_forget)


button_errForget = ctk.CTkButton(master = frame_button_forget, text="J'ai oublié de renseigner un incident négatif", command=forgottenErr1)
button_errForget.configure(font=("Helvetica",15),height=50, width=300)

label_forget = ctk.CTkLabel(master = frame_button_cadre, text="Combien de temps s'est-il passé depuis l'incident négatif ? \n (En minutes)")
label_forget.configure(font=("Helvetica", 15))

entry_forgotten = ctk.CTkEntry(master = frame_button_cadre, placeholder_text=("Temps en minutes"))
entry_forgotten.bind("<Return>", lambda x : forgottenErr2())

button_errForget2 = ctk.CTkButton(master = frame_button_cadre, text="Valider", command=forgottenErr2)



###-_-Aide forget :



def Enter_aide2(event) :
    """Grise le help et fait apparaitre une tooltip avec une description"""
    aide_button_forget.configure(image=photo_aide_button_forgetf)
    show_tooltip(event, dico_aide["Forget"])


def Leave_aide2(event) :
    aide_button_forget.configure(image=photo_aide_button_forget)
    hide_tooltip(event)


image_aide_button_forget = Image.open(path_img_aide)
image_aide_button_forget_resized = image_aide_button_forget.resize((100, 100), Image.LANCZOS)
photo_aide_button_forget = ctk.CTkImage(dark_image=image_aide_button_forget_resized, size=(20, 20))

image_aide_button_forgetf = Image.open(path_img_aidef)
image_aide_button_forgetf_resized = image_aide_button_forgetf.resize((100, 100), Image.LANCZOS)
photo_aide_button_forgetf = ctk.CTkImage(light_image=image_aide_button_forgetf_resized, dark_image=image_aide_button_forgetf_resized, size=(20, 20))

# Afficher l'image dans un label
aide_button_forget = ctk.CTkLabel(master=frame_button_forget, image=photo_aide_button_forget ,text='', cursor="hand2")
aide_button_forget.configure(font=('Helvetica',15))

aide_button_forget.bind("<Enter>", Enter_aide2)
aide_button_forget.bind("<Leave>", Leave_aide2)
aide_button_forget.bind("<Motion>", move_tooltip)

button_errForget.pack(padx=10,side=tk.LEFT)
aide_button_forget.pack(side=tk.LEFT)

label_forget.pack(pady=10, padx=10)
entry_forgotten.pack(pady=5, padx=10)
button_errForget2.pack(pady=5, padx=10)


# label_image_btn.pack(pady=(15, 10), padx=(0, 105)

######################

entry_cachee = ctk.CTkEntry(master = frame_button)                               #Subterfuge pour appuyer sur le bouton Erreur avec "entrée"
entry_cachee.pack()                                                              #Subterfuge pour appuyer sur le bouton Erreur avec "entrée"
entry_cachee.place(x = 0,y=10000)
entry_cachee.bind("<Return>", lambda x : stimulation(0))               #Subterfuge pour appuyer sur le bouton Erreur avec "entrée"

def on_enter(event):
    button_f4.configure(text="❌ Fermer et Sauvegarder")
def on_leave(event):
    button_f4.configure(text="❌")

button_f4 = ctk.CTkButton(master = frame_button, text=" ❌ ", width=15 , command=arretExpe)
button_f4.configure(fg_color="red", hover_color="white", text_color="black")
button_f4.pack()
button_f4.place(x=5,y=5)

button_f4.bind("<Enter>", on_enter)
button_f4.bind("<Leave>", on_leave)


#TODO Voir ses  erreurs

def vers_frame_tab_err() :
    """Retire la page 2 et affiche le récapitulatif des erreurs"""
    # reset_entry(list_val) list_val = ['',50,"",50,'','',50,'']

    frame_button.pack_forget()
    display_table()
    display_table2()



    frame_recap.pack(pady=15, padx=30, fill="both", expand=True)

frame_button_recap = ctk.CTkFrame(master= frame_button,fg_color="#2b2b2b")


button_voir_err = ctk.CTkButton(master = frame_button_recap, text="Voir récapitulatif", command=vers_frame_tab_err)
button_voir_err.configure(font=("Helvetica",15))
button_voir_err.configure(height=50, width=300)

###-_-Aide Voir Recap :

def Enter_aide3(event) :
    """Grise le help et fait apparaitre une tooltip avec une description"""
    aide_button_voir_recap.configure(image=photo_aide_button_voir_recapf)
    show_tooltip(event, dico_aide["Recap"])


def Leave_aide3(event) :
    aide_button_voir_recap.configure(image=photo_aide_button_voir_recap)
    hide_tooltip(event)


image_aide_button_voir_recap = Image.open(path_img_aide)
image_aide_button_voir_recap_resized = image_aide_button_voir_recap.resize((100, 100), Image.LANCZOS)
photo_aide_button_voir_recap = ctk.CTkImage(dark_image=image_aide_button_voir_recap_resized, size=(20, 20))

image_aide_button_voir_recapf = Image.open(path_img_aidef)
image_aide_button_voir_recapf_resized = image_aide_button_voir_recapf.resize((100, 100), Image.LANCZOS)
photo_aide_button_voir_recapf = ctk.CTkImage(light_image=image_aide_button_voir_recapf_resized, dark_image=image_aide_button_voir_recapf_resized, size=(20, 20))

# Afficher l'image dans un label
aide_button_voir_recap = ctk.CTkLabel(master=frame_button_recap, image=photo_aide_button_voir_recap ,text='', cursor="hand2")
aide_button_voir_recap.configure(font=('Helvetica',15))

aide_button_voir_recap.bind("<Enter>", Enter_aide3)
aide_button_voir_recap.bind("<Leave>", Leave_aide3)
aide_button_voir_recap.bind("<Motion>", move_tooltip)

button_voir_err.pack(padx= 10,side=tk.LEFT)
aide_button_voir_recap.pack(side=tk.LEFT)

########################################################################### Frame Speciale : Voir erreurs

def sortir_recap() :
    """
    retourne vers la page 2
    """
    frame_recap.pack_forget()
    frame_button.pack(pady=20, padx=50, fill="both", expand=True)

    pack_button_tout()

    entry_cachee.focus_set()
    clear_table2()
    clear_table()

#Fenêtre racap
frame_recap = ctk.CTkFrame(master=root)

#Titre Principal
frame_recapTitre = ctk.CTkFrame(master=frame_recap)
frame_recapTitre.pack(pady=25, padx=50)

label_TitreRecap = ctk.CTkLabel(master= frame_recapTitre, text="Récapitulatif des incidents négatifs")
label_TitreRecap.pack(pady=10, padx=50)
label_TitreRecap.configure(font=("Helvetica", 35))

#SousTitre Info complétées :

frame_recapTitre2 = ctk.CTkFrame(master=frame_recap)
frame_recapTitre2.pack(pady=15, padx=50)

label_TitreRecap2 = ctk.CTkLabel(master= frame_recapTitre2, text="Informations complétées")
label_TitreRecap2.pack(pady=5, padx=50)
label_TitreRecap2.configure(font=("Helvetica", 20))

#Cadre du premier tableau (complétées)
container_frame2 = ctk.CTkFrame(master=frame_recap)
container_frame2.pack(pady=10, padx=25, fill="both", expand=True)
container_frame2.configure(fg_color=background_color)

# Créer un frame pour contenir le canvas et les scrollbars
container_frame = ctk.CTkFrame(master=container_frame2)
container_frame.pack(pady=10, padx=25, fill="both", expand=True)
container_frame.configure(fg_color=background_color)

# Créer un canvas pour le contenu défilant avec la même couleur de fond
canvas = tk.Canvas(container_frame, bg=background_color, bd=0, highlightthickness=0)
canvas.pack(side=tk.LEFT, fill="both", expand=True)

# Ajouter une barre de défilement verticale
scrollbar_v = ctk.CTkScrollbar(container_frame, orientation="vertical", command=canvas.yview)
scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)

# Ajouter une barre de défilement horizontale
scrollbar_h = ctk.CTkScrollbar(container_frame2, orientation="horizontal", command=canvas.xview)
scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)

# Lier les scrollbars au canvas
canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

# Créer un frame pour le contenu à l'intérieur du canvas
scrollable_frame = ctk.CTkFrame(canvas, fg_color=background_color)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def on_frame_configure(event=None):
    """Met à jour la région scrollable du canvas pour s'adapter au contenu."""
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", on_frame_configure)


###########  Tableau ajout rapide


#SousTitre Info complétées :

frame_recapTitre3 = ctk.CTkFrame(master=frame_recap)
frame_recapTitre3.pack(pady=15, padx=50)

label_TitreRecap3 = ctk.CTkLabel(master= frame_recapTitre3, text="Informations à compléter :")
label_TitreRecap3.pack(pady=5, padx=50)
label_TitreRecap3.configure(font=("Helvetica", 20))

#Cadre du second tableau (à compléter)
container_frame3 = ctk.CTkFrame(master=frame_recap)
container_frame3.pack(pady=10, padx=25, fill="both", expand=True)
container_frame3.configure(fg_color=background_color)

# Créer un frame pour contenir le canvas et les scrollbars
container_frame4 = ctk.CTkFrame(master=container_frame3)
container_frame4.pack(pady=10, padx=25, fill="both", expand=True)
container_frame4.configure(fg_color=background_color)

# Créer un canvas pour le contenu défilant avec la même couleur de fond
canvas2 = tk.Canvas(container_frame4, bg=background_color, bd=0, highlightthickness=0)
canvas2.pack(side=tk.LEFT, fill="both", expand=True)

# Ajouter une barre de défilement verticale
scrollbar_v2 = ctk.CTkScrollbar(container_frame4, orientation="vertical", command=canvas2.yview)
scrollbar_v2.pack(side=tk.RIGHT, fill=tk.Y)

# Ajouter une barre de défilement horizontale
scrollbar_h2 = ctk.CTkScrollbar(container_frame3, orientation="horizontal", command=canvas2.xview)
scrollbar_h2.pack(side=tk.BOTTOM, fill=tk.X)

# Lier les scrollbars au canvas
canvas2.configure(yscrollcommand=scrollbar_v2.set, xscrollcommand=scrollbar_h2.set)

# Créer un frame pour le contenu à l'intérieur du canvas
scrollable_frame2 = ctk.CTkFrame(canvas2, fg_color=background_color)
canvas2.create_window((0, 0), window=scrollable_frame2, anchor="nw")

def on_frame_configure2(event=None):
    """Met à jour la région scrollable du canvas pour s'adapter au contenu."""
    canvas2.configure(scrollregion=canvas2.bbox("all"))

scrollable_frame2.bind("<Configure>", on_frame_configure2)

def choisir_envoyer_etat() :
    if button_quit_Modif.winfo_ismapped() :
        envoyer_en_l_etat_modif()
    else :
        envoyer_en_l_etat()

def envoyer_en_l_etat() :
    # Récupération des données :

    type = get_selected_button_value()
    faute = selected_option_Bad.get()
    niveau_importance = dic_likert_Importance[sliderImportance.get()]
    description = entry_Commentaire.get("1.0", tk.END).strip()
    niveau_concentration = dic_likert_Concentration[sliderConcentration.get()]
    distraction = selected_optionDistraction.get()
    natureDistration = entry_Distraction.get()
    niveau_fatigue = dic_likert_Fatigue[sliderFatigue.get()]
    niveau_difficulte = selected_optionDifficulte.get()

    if id_time_code - 1 >= 0:  # ID d'erreurs indiquées au bon moment ont un id positif et de param 0
        parameter = 0  # Les erreurs oubliées ont un id négatif et sont donc de param 1
    else:
        parameter = 1

    path = f"../Data/{n_anonymat}/Record_{n_anonymat}_{horodatage_start}.edf"

    if description == "Description de l'incident négatif...":
        description = ''

    if (distraction == "Oui"):
        if (natureDistration != ''):
            nouvelle_ligne = pd.DataFrame({
                "ID": [dernier_id],
                "Path": [path],
                "Timecode": [dernier_time_code],
                "Parameter": [dernier_parametre],
                "ID Cible": [''],
                "Type": [type],
                "Faute": [faute],
                "Importance": [niveau_importance],
                "Description": [description],
                "Concentration": [niveau_concentration],
                "Distrait": [distraction],
                "NatureDistraction": [natureDistration],
                "Fatigue": [niveau_fatigue],
                "Difficulte": [niveau_difficulte]})

            df = pd.read_excel(excel_path)
            df = pd.concat([df, nouvelle_ligne])
            df.to_excel(excel_path, index=False)
            reset_entry()
            retourPage2()

    elif (distraction == "Non"):
        if (natureDistration == ''):
            nouvelle_ligne = pd.DataFrame({
                "ID": [dernier_id],
                "Path": [path],
                "Timecode": [dernier_time_code],
                "Parameter": [dernier_parametre],
                "ID Cible": [''],
                "Type": [type],
                "Faute": [faute],
                "Importance": [niveau_importance],
                "Description": [description],
                "Concentration": [niveau_concentration],
                "Distrait": [distraction],
                "NatureDistraction": [natureDistration],
                "Fatigue": [niveau_fatigue],
                "Difficulte": [niveau_difficulte]})

            df = pd.read_excel(excel_path)
            df = pd.concat([df, nouvelle_ligne])
            df.to_excel(excel_path, index=False)
            reset_entry()
            retourPage2()
    else :
        nouvelle_ligne = pd.DataFrame({
            "ID": [dernier_id],
            "Path": [path],
            "Timecode": [dernier_time_code],
            "Parameter": [dernier_parametre],
            "ID Cible": [''],
            "Type": [type],
            "Faute": [faute],
            "Importance": [niveau_importance],
            "Description": [description],
            "Concentration": [niveau_concentration],
            "Distrait": [distraction],
            "NatureDistraction": [natureDistration],
            "Fatigue": [niveau_fatigue],
            "Difficulte": [niveau_difficulte]})

        df = pd.read_excel(excel_path)
        df = pd.concat([df, nouvelle_ligne])
        df.to_excel(excel_path, index=False)
        reset_entry()
        retourPage2()

def verifier_quest1_complet_xlsx(row) :

    type = str(row['Type'])
    faute = str(row['Faute'])
    description = str(row['Description'])


    rep = (type != '' and faute != '' and description != "Description de l'incident négatif...")
    rep_vide = (type != 'nan' and faute != 'nan' and description != "nan")

    return rep and rep_vide


def envoyer_en_l_etat_modif() :
    print("sauvegarder modif ")

    global excel_path, row_modif

    type = get_selected_button_value()
    faute = selected_option_Bad.get()
    niveau_importance = dic_likert_Importance[sliderImportance.get()]
    description = entry_Commentaire.get("1.0", tk.END).strip()
    niveau_concentration = dic_likert_Concentration[sliderConcentration.get()]
    distraction = selected_optionDistraction.get()
    natureDistration = entry_Distraction.get()
    niveau_fatigue = dic_likert_Fatigue[sliderFatigue.get()]
    niveau_difficulte = selected_optionDifficulte.get()

    df = pd.read_excel(excel_path)

    if description == "Description de l'incident négatif..." :
        description= ''

    if (distraction == "Oui"):
        if (natureDistration != ''):

            updates = {
                "Type": type,
                "Faute": faute,
                "Importance": niveau_importance,
                "Description": description,
                "Concentration": niveau_concentration,
                "Distrait": distraction,
                "NatureDistraction": natureDistration,
                "Fatigue": niveau_fatigue,
                "Difficulte": niveau_difficulte}

            for column, new_value in updates.items():
                df.at[row_modif, column] = new_value

            df.to_excel(excel_path, index=False)

            reset_entry()
            button_done_modif.pack_forget()
            button_quit_Modif.place_forget()

            button_quit.place(x=5, y=5)
            frame_quest.pack_forget()

            frame_button.pack(pady=20, padx=50, fill="both", expand=True)

            pack_button_tout()

    elif (distraction == "Non"):
        if (natureDistration == ''):

            updates = {
                "Type": type,
                "Faute": faute,
                "Importance": niveau_importance,
                "Description": description,
                "Concentration": niveau_concentration,
                "Distrait": distraction,
                "NatureDistraction": natureDistration,
                "Fatigue": niveau_fatigue,
                "Difficulte": niveau_difficulte}

            for column, new_value in updates.items():
                df.at[row_modif, column] = new_value

            df.to_excel(excel_path, index=False)

            reset_entry()
            button_done_modif.pack_forget()
            button_quit_Modif.place_forget()

            button_quit.place(x=5, y=5)
            frame_quest.pack_forget()

            frame_button.pack(pady=20, padx=50, fill="both", expand=True)

            pack_button_tout()
    else :
        updates = {
            "Type": type,
            "Faute": faute,
            "Importance": niveau_importance,
            "Description": description,
            "Concentration": niveau_concentration,
            "Distrait": distraction,
            "NatureDistraction": natureDistration,
            "Fatigue": niveau_fatigue,
            "Difficulte": niveau_difficulte}

        for column, new_value in updates.items():
            df.at[row_modif, column] = new_value

        df.to_excel(excel_path, index=False)

        reset_entry()
        button_done_modif.pack_forget()
        button_quit_Modif.place_forget()

        button_quit.place(x=5, y=5)
        frame_quest.pack_forget()

        frame_button.pack(pady=20, padx=50, fill="both", expand=True)

        pack_button_tout()


def sauvegarder_modif() :
    """
    Récupère les données du quest

    """
    print("sauvegarder modif ")

    global excel_path, row_modif

    type = get_selected_button_value()
    faute = selected_option_Bad.get()
    niveau_importance = dic_likert_Importance[sliderImportance.get()]
    description = entry_Commentaire.get("1.0", tk.END).strip()
    niveau_concentration = dic_likert_Concentration[sliderConcentration.get()]
    distraction = selected_optionDistraction.get()
    natureDistration = entry_Distraction.get()
    niveau_fatigue = dic_likert_Fatigue[sliderFatigue.get()]
    niveau_difficulte = selected_optionDifficulte.get()

    df = pd.read_excel(excel_path)

    if ( type != '') and ( description != "Description de l'incident négatif...") and ( description != "") and ( distraction != '') and (niveau_difficulte != '') and (niveau_concentration != ' ') and (niveau_fatigue != ' ') :
        if ( distraction == "Oui") :
            if ( natureDistration != '' ) :

                updates = {
                    "Type": type,
                    "Faute": faute,
                    "Importance": niveau_importance,
                    "Description": description,
                    "Concentration": niveau_concentration,
                    "Distrait": distraction,
                    "NatureDistraction": natureDistration,
                    "Fatigue": niveau_fatigue,
                    "Difficulte": niveau_difficulte}

                for column, new_value in updates.items():
                    df.at[row_modif, column] = new_value

                df.to_excel(excel_path, index=False)

                reset_entry()
                button_done_modif.pack_forget()
                button_quit_Modif.place_forget()

                button_quit.place(x=5,y=5)
                frame_quest.pack_forget()

                frame_button.pack(pady=20, padx=50, fill="both", expand=True)

                pack_button_tout()

        elif (distraction == "Non"):
            if (natureDistration == ''):

                updates = {
                    "Type" : type,
                    "Faute" : faute,
                    "Importance": niveau_importance,
                    "Description": description,
                    "Concentration": niveau_concentration,
                    "Distrait": distraction,
                    "NatureDistraction": natureDistration,
                    "Fatigue": niveau_fatigue,
                    "Difficulte": niveau_difficulte}

                for column, new_value in updates.items():
                    df.at[row_modif, column] = new_value

                df.to_excel(excel_path, index=False)

                reset_entry()
                button_done_modif.pack_forget()
                button_quit_Modif.place_forget()

                button_quit.place(x=5, y=5)
                frame_quest.pack_forget()

                frame_button.pack(pady=20, padx=50, fill="both", expand=True)

                pack_button_tout()


            #ANNULER MODIF PRESENT ET SauvegarderModif aussi après utilisation





def affiche_Quest_Modif() :

    frame_quest.pack(pady=20, padx=50, fill="both", expand=True)
    button_quit.place_forget()
    button_quit_Modif.place(x=5, y=5)
    actualisation_options()
    Concentration_Type()

    # button_done.pack_forget()

def modifier_ligne(row) :
    """
    Récupère les informations de la n ième ligne du fichier excel_path
    les stock dans une liste
    reset_entry(liste)

    """
    global excel_path, row_modif
    row_modif = row
    df = pd.read_excel(excel_path)

    ligne = df.loc[df['ID'] == row_modif]
    ligne_liste = ligne.values.flatten().tolist()[5:]

    ligne_liste[2]  = {value: key for key, value in dic_likert_Importance.items()}[ligne_liste[2]]
    ligne_liste[4]  = {value: key for key, value in dic_likert_Concentration.items()}[ligne_liste[4]]
    ligne_liste[7]  = {value: key for key, value in dic_likert_Fatigue.items()}[ligne_liste[7]]

    reset_entry(ligne_liste)
    clear_table()
    clear_table2()
    frame_recap.pack_forget()
    creation_boutons_type()
    actualisation_options()
    if entry_Distraction.get() == 'NaN' :
        entry_Distraction.delete(0, tk.END)


    affiche_Quest_Modif()


def display_table(columns_to_exclude=["Path","ID Cible" ,"Timecode", "Parameter"]):
    global excel_path, frame_tableau

    df = pd.read_excel(excel_path)

    # Filtrer les colonnes indésirables :
    df_filtered = df.drop(columns=columns_to_exclude)

    frame_tableau = ctk.CTkFrame(master=scrollable_frame)
    frame_tableau.pack(fill="both", expand=True)

    # Ajout des en-têtes de colonnes
    headers = ["Modifier"] + list(df_filtered.columns)
    for col_num, col_name in enumerate(headers):
        header = ctk.CTkLabel(frame_tableau, text=col_name)
        header.grid(row=0, column=col_num, padx=10, pady=5)

        # Insérer les données et les boutons
        for row_num, row in df_filtered.iterrows():
  # On vérifie que la première page du quest est complétée pour l'afficher sur le bon tableau
            if verifier_quest1_complet_xlsx(row):
                # Ajouter un bouton dans la première colonne
                button = ctk.CTkButton(frame_tableau, text="Modifier", width=50,
                                       command=lambda row=row_num: modifier_ligne(row))
                button.grid(row=row_num + 1, column=0, padx=10, pady=5)

                # Ajouter les autres cellules
                for col_num, value in enumerate(row):
                    if str(value) == 'nan' or str(value) == ' ':
                        value = '--'
                    cell = ctk.CTkLabel(frame_tableau, text=value)
                    cell.grid(row=row_num + 1, column=col_num + 1, padx=10, pady=5)
        on_frame_configure()


def clear_table():
    global frame_tableau
    if frame_tableau:
        frame_tableau.destroy()
        frame_tableau = None


#RECAP AJOUT RAPIDE

def modifier_ligne2(row) :
    """
    Récupère les informations de la n ième ligne du fichier excel_path
    les stock dans une liste
    reset_entry(liste)

    """
    global excel_path, row_modif
    row_modif = row
    df = pd.read_excel(excel_path)

    ligne = df.loc[df['ID'] == row_modif]
    ligne_liste = ligne.values.flatten().tolist()[5:]


    try :
        ligne_liste[2] = {value: key for key, value in dic_likert_Importance.items()}[ligne_liste[2]]
        ligne_liste[4] = {value: key for key, value in dic_likert_Concentration.items()}[ligne_liste[4]]
        ligne_liste[7] = {value: key for key, value in dic_likert_Fatigue.items()}[ligne_liste[7]]
    except :
        ligne_liste[2] = 50
        ligne_liste[4] =  50
        ligne_liste[7] = 50

    reset_entry(ligne_liste)
    clear_table()
    clear_table2()
    frame_recap.pack_forget()
    creation_boutons_type()
    actualisation_options()
    if entry_Distraction.get() == 'NaN' :
        entry_Distraction.delete(0, tk.END)

    affiche_Quest_Modif()

    if entry_Commentaire.get("1.0", "end-1c") == 'NaN' :
        entry_Commentaire.delete("1.0", tk.END)
        add_placeholder()







def display_table2(columns_to_keep=["ID","Description"]):
    global excel_path, frame_tableau2

    df = pd.read_excel(excel_path)

    # Filtrer les colonnes indésirables :




    frame_tableau2 = ctk.CTkFrame(master=scrollable_frame2)
    frame_tableau2.pack(fill="both", expand=True)

    # Ajout des en-têtes de colonnes
    headers = ["Modifier"] + list(df[columns_to_keep].columns)
    for col_num, col_name in enumerate(headers):
        header = ctk.CTkLabel(frame_tableau2, text=col_name)
        header.grid(row=0, column=col_num, padx=10, pady=5)

    # Insérer les données et les boutons
    for row_num, row in df.iterrows():
        if not verifier_quest1_complet_xlsx(row):
            # Ajouter un bouton dans la première colonne
            button = ctk.CTkButton(frame_tableau2, text="Modifier", width=50,
                                   command=lambda row=row_num: modifier_ligne2(row))
            button.grid(row=row_num + 1, column=0, padx=10, pady=5)

            # Ajouter les autres cellules
            filtered_row = row[columns_to_keep]
            for col_num, value in enumerate(filtered_row):
                if str(value) == 'nan' or str(value) == ' ':
                    value = '--'
                cell = ctk.CTkLabel(frame_tableau2, text=value)
                cell.grid(row=row_num + 1, column=col_num + 1, padx=10, pady=5)
    on_frame_configure2()


def clear_table2():
    global frame_tableau2
    if frame_tableau2:
        frame_tableau2.destroy()
        frame_tableau2 = None


button_sortir_recap = ctk.CTkButton(master = frame_recap, text="Revenir", width=15 , command=sortir_recap)
button_sortir_recap.pack()
button_sortir_recap.place(x=5,y=5)



########################################################################### Frame 3 : Questionnaire

def Type_Concentration():

    if button_quit_Modif.winfo_ismapped() :
        button_done_modif.pack_forget()

    frame_questType.pack_forget()
    frame_questImportance.pack_forget()
    frame_questCommentaire.pack_forget()

    button_Type_Concentration.pack_forget()

    button_Concentration_Type.pack(padx=10, pady=10)

    frame_questConcentration.pack(pady=5, padx=50, fill="both", expand=True)
    frame_questDistraction.pack(pady=5, padx=50, fill="both", expand=True)
    frame_questFatigue.pack(pady=5, padx=50, fill="both", expand=True)
    frame_questDifficulte.pack(pady=5, padx=50, fill="both", expand=True)
    button_done.pack(pady=20, padx=10)

    if button_quit_Modif.winfo_ismapped() :
        button_done.pack_forget()
        button_done_modif.pack(pady=20, padx=10)


    root.focus_set()




def Concentration_Type():
    frame_questConcentration.pack_forget()
    frame_questDistraction.pack_forget()
    frame_questFatigue.pack_forget()
    frame_questDifficulte.pack_forget()
    button_done.pack_forget()
    button_Concentration_Type.pack_forget()

    if button_quit_Modif.winfo_ismapped() :
        button_done_modif.pack_forget()

    frame_questType.pack(pady=5, padx=50, fill="both", expand=True)
    frame_questImportance.pack(pady=5, padx=50, fill="both", expand=True)
    frame_questCommentaire.pack(pady=5, padx=50, fill="both", expand=True)

    button_Type_Concentration.pack(padx=10, pady=10)

    entry_Commentaire.focus_set()
    entry_actualise_options.focus_set()


    root.focus_set()


frame_quest = ctk.CTkFrame(master=root)

frame_questTitre = ctk.CTkFrame(master=frame_quest)
frame_questTitre.pack(pady=10, padx=50, expand=True)

label_quest = ctk.CTkLabel(master= frame_questTitre, text="Questionnaire sur l'incident négatif")
label_quest.pack(pady=20, padx=50)
label_quest.configure(font=("Helvetica", 35))

# Revenir en frame_button et supprimer l'enregistrement

def retourPage2(supp=0) :
    """Retire le questionnaire et affiche la page 2

    Si param = -1 alors on enlève la dernière stimulation ( à changer pour en ajouter une d'aun autre label à la place en indiquant l'id Cible ?)

    si param = 1 alors appelée depuis "annuler modification" pour remettre les bons boutons"

    """
    #De base on ne vient pas forcément de la modification
    vers_tab = False

    if supp == -1 :
        df = pd.read_csv(path_time_code)
        df = df.drop(df.index[-1])
        global id_time_code
        id_time_code -=1

        print("déstimulé")

        df.to_csv(path_time_code, index=False)
        df.to_csv(path_time_code_BackUp, index=False)

    elif supp == 1 :
        button_quit_Modif.place_forget()
        button_quit.place(x=5,y=5)
        button_done_modif.pack_forget()
        vers_tab = True



    reset_entry()                                                       #On reset les données du tableau
    frame_quest.pack_forget()                                           #On retire la page du questionnaire
    frame_button.pack(pady=20, padx=50, fill="both", expand=True)       #Puis faire apparaitre la page des buttons

                 # On réinitialise les cadres de la page bouton
    pack_button_tout()

    # Si on venait de la modification, en entre à nouveau dans la page du récap
    if vers_tab :
        vers_frame_tab_err()


button_quit = ctk.CTkButton(master = frame_quest, text="Annuler", command=lambda : retourPage2(-1))
button_quit.place(x=5,y=15)

button_quit_Modif = ctk.CTkButton(master = frame_quest, text="Annuler la modification", command=lambda : retourPage2(1))



# ✔ TODO            # Type de l'erreur

frame_questType = ctk.CTkFrame(master=frame_quest)
frame_questType.pack(pady=5, padx=50, fill="both", expand=True)

label_typeErreur = ctk.CTkLabel(master=frame_questType, text="Veuillez renseigner la nature de l'incident négatif")
label_typeErreur.pack(pady=10)
label_typeErreur.configure(font=("Helvetica", 15))


df_types = pd.read_excel("../Sources/types_err.xlsx")

options = list(df_types['Types'])
descriptions = list(df_types['Description'])
exemples = list(df_types['Exemple'])

def get_selected_button_value():
    for option, is_selected in button_states.items():
        if is_selected:
            return option
    return ''

def auto_toogle(val):
    # val = get_selected_button_value()
    for button in affichage_boutons.winfo_children():
        if button.cget("text").lower() == val:
            button.configure(fg_color="#106A43")
            button_states[button.cget("text")] = True


def actualisation_options(event=None):
    entered_text = entry_actualise_options.get().lower()
    # filtered_options = [option for option in options if entered_text in option.lower()]
#
#     # Supprimer tous les boutons existants
#     for widget in affichage_boutons.winfo_children():
#         widget.destroy()
#
#     for btn in button_states :
#         button_states[btn] = False
#
#     # Recréer les boutons filtrés
#     i, j = 0, 0
#     for e in filtered_options:
#         button_states[e] = False
#         def create_button(e):
#             button = ctk.CTkButton(affichage_boutons, text=e, fg_color="#2FA572", width=button_width, height=button_height)
#             button.configure(command=lambda btn=button, opt=e: toggle_button(btn, opt))
#             return button
#         button = create_button(e)
#         button.grid(row=j, column=i, pady=5, padx=5)
#         if i + 1 == 6:
#             i = 0
#             j += 1
#         else:
#             i += 1
    auto_toogle(entered_text)


entry_actualise_options = ctk.CTkEntry(master=frame_questType,width=200 ,placeholder_text=("Rechercher                                   🔎"))
# entry_actualise_options.pack(pady=5)
# entry_actualise_options.bind("<KeyRelease>", actualisation_options)

# def rajouterType():
#     """Rajoute un type d'erreur"""
#     df_types = pd.read_excel("../Sources/types_err.xlsx")
#
#     type = entry_rajouter_typeErreur.get()
#     description = entry_rajouter_typeErreurD.get()
#
#     global options
#
#     if (not type in options) and (type != '') and (description != ''):
#
#         nouvelle_erreur = pd.DataFrame({"Types": [type], "Description": [description]})
#         df_types = pd.concat([df_types, nouvelle_erreur])
#         df_types.to_excel("../Sources/types_err.xlsx", index=False)
#         print("Fait")
#
#         afficherPlus()
#
#         options = list(df_types["Types"])
#         entry_actualise_options.delete(0, tk.END)
#         entry_actualise_options.insert(tk.END, type)
#         actualisation_options()


# cadreNouveauType = ctk.CTkFrame(master=frame_questType)
#
# entry_rajouter_typeErreur = ctk.CTkEntry(master=cadreNouveauType,width=175, placeholder_text="Rajouter un type d'erreur")
# entry_rajouter_typeErreur.grid(row=0, column=0, pady=10, padx=10)
# entry_rajouter_typeErreurD = ctk.CTkEntry(master=cadreNouveauType, width=250,placeholder_text="Rajouter la description du type d'erreur")
# entry_rajouter_typeErreurD.grid(row=0, column=1, pady=10, padx=10)
#
# entry_rajouter_typeErreurD.bind("<Return>", lambda x: rajouterType())
#
# button_rajouter_typeErreur = ctk.CTkButton(master=cadreNouveauType, text="Rajouter", command=rajouterType)
# button_rajouter_typeErreur.grid(row=0, column=2, pady=10, padx=10)

# def afficherPlus():
#     if cadreNouveauType.winfo_ismapped():
#         cadreNouveauType.pack_forget()
#     else:
#         cadreNouveauType.pack(anchor=tk.CENTER, padx=10, pady=10)
#
# button_plus = ctk.CTkButton(master=frame_questType, text="Votre type d'erreur n'apparait pas ?", command=afficherPlus)


affichage_boutons = ctk.CTkFrame(master=frame_questType)
affichage_boutons.pack(anchor=tk.CENTER, padx=10, pady=10)


# Dictionnaire pour maintenir l'état des boutons
button_states = {}


# Fonction pour gérer le clic sur un bouton

# def toggle_button(button, option): #Plusieurs boutons
#     if button_states[option]:
#         button.configure(fg_color="#2FA572")
#     else:
#         button.configure(fg_color="#106A43")
#     button_states[option] = not button_states[option]

def toggle_button(button, option):
    # Vérifier si un autre bouton est sélectionné
    selected_button = None
    for btn_option, btn in button_states.items():
        if button_states[btn_option]:
            selected_button = btn_option
            break

    if selected_button == option:
        # Si le bouton sélectionné est pressé à nouveau, le désélectionner
        button.configure(fg_color="#2FA572")
        button_states[option] = False
    elif selected_button is None:
        # Si aucun bouton n'est sélectionné, sélectionner le bouton actuel
        button.configure(fg_color="#106A43")
        button_states[option] = True
    # Sinon, ne rien faire

# Dimensions des boutons
button_width = 180
button_height = 30



#Créer et placer les boutons avec tooltips et état appuyé/non
def creation_boutons_type():
    i, j = 0, 0
    for k in range(len(options)):
        type_button = options[k]
        description = descriptions[k]
        exemple = exemples[k]

        description = description.replace('\\n', '\n')
        exemple = exemple.replace('\\n', '\n')

        button_states[type_button] = False

        button = ctk.CTkButton(affichage_boutons, text=type_button, fg_color="#2FA572", width=button_width, height=button_height)
        button.configure(command=lambda btn=button, opt=type_button: toggle_button(btn, opt))
        button.grid(row=j, column=i, pady=5, padx=5)

        if i + 1 == 3:
            i = 0
            j += 1
        else:
            i += 1

        text_survol = f"{description} \n Ex :  {exemple}"

        button.bind("<Enter>", lambda event, text=text_survol: show_tooltip(event, text))
        button.bind("<Leave>", hide_tooltip)
        button.bind("<Motion>", move_tooltip)

creation_boutons_type()



#TODO Faute Système/User :


selected_option_Bad = tk.StringVar() #Variable qui stock la séléection oui/non

cadre_boutons_Bad = ctk.CTkFrame(master = frame_questType, width=100)
cadre_boutons_Bad.pack(ipadx=10,pady=10)

label_bad = ctk.CTkLabel(master=cadre_boutons_Bad, text="Selon vous, qui est responsable de l'incident ?", fg_color="#333333", corner_radius=50 )
label_bad.pack(pady=(10,0),padx=0)



# Radiobutton 2
bad_button_2 = ctk.CTkRadioButton(cadre_boutons_Bad, text="Système (Machine)", variable=selected_option_Bad, value="Système (Machine)")
bad_button_2.pack(pady=10,padx=10,side="right")
bad_button_2.configure(font=("Helvetica",13))


# Radiobutton 1
bad_button_1 = ctk.CTkRadioButton(cadre_boutons_Bad, text="", variable=selected_option_Bad, value="Utilisateur (Moi)")
bad_button_1.pack(pady=10,padx=(0,10),side="right")

bad_label_1 = ctk.CTkLabel(master=cadre_boutons_Bad, text="Utilisateur (Moi)")
bad_label_1.configure(font=("Helvetica",13),cursor="hand2")
bad_label_1.pack(pady=10,padx=10,side="right")
bad_label_1.bind("<Button-1>", lambda event:selected_option_Bad.set("Utilisateur (Moi)"))


#  TODO            # Echelle d'importance de l'erreur


def magnet_likert_importance(valeur_actuelle) :
    """Magnetise la valeur à la plus proche sur l'echelle de likert """
    liste = [0, 16 , 33 , 50, 66, 83, 100]

    nouvelle_val = min(liste, key=lambda val: abs(val - valeur_actuelle))
    sliderImportance.set(nouvelle_val)


frame_questImportance = ctk.CTkFrame(master=frame_quest)
frame_questImportance.pack(pady=5, padx=50, fill="both", expand=True)

label_typeImportance = ctk.CTkLabel(master = frame_questImportance,text="Veuillez renseigner l'importance (la gravité) de l'incident négatif")
label_typeImportance.pack(pady=10)
label_typeImportance.configure(font=("Helvetica", 15))

###Slider

cadreImportance = ctk.CTkFrame(master=frame_questImportance)
cadreImportance.pack(anchor=tk.CENTER, pady=10)


label_importance_0 = ctk.CTkLabel(master = cadreImportance,text="Insignifiante")
label_importance_0.grid(row=0, column=0, padx=10)
label_importance_0.configure(font=("Helvetica",13),text_color='green')

label_importance_1 = ctk.CTkLabel(master = cadreImportance,text="Peu Importante")
label_importance_1.grid(row=0, column=1, padx=10)
label_importance_1.configure(font=("Helvetica",13),text_color='green')

label_importance_2 = ctk.CTkLabel(master = cadreImportance,text="Pas Très Importante")
label_importance_2.grid(row=0, column=2, padx=10)
label_importance_2.configure(font=("Helvetica",13),text_color='green')

label_importance_3 = ctk.CTkLabel(master = cadreImportance,text="Neutre")
label_importance_3.grid(row=0, column=3, padx=10)
label_importance_3.configure(font=("Helvetica",13),text_color='white')


label_importance_4 = ctk.CTkLabel(master = cadreImportance,text="Assez Importante")
label_importance_4.grid(row=0, column=4, padx=10)
label_importance_4.configure(font=("Helvetica",13),text_color='red')

label_importance_5 = ctk.CTkLabel(master = cadreImportance,text="Importante")
label_importance_5.grid(row=0, column=5, padx=10)
label_importance_5.configure(font=("Helvetica",13),text_color='red')

label_importance_6 = ctk.CTkLabel(master = cadreImportance,text="Très Importante")
label_importance_6.grid(row=0, column=6, padx=10)
label_importance_6.configure(font=("Helvetica",13),text_color='red')

sliderImportance = ctk.CTkSlider(master = frame_questImportance, from_=0, to=100, width=600, command=magnet_likert_importance)
sliderImportance.pack()

#Ligne rajoutée


# ✔ TODO            # Commentaires

frame_questCommentaire = ctk.CTkFrame(master=frame_quest)
frame_questCommentaire.pack(pady=5, padx=50, fill="both", expand=True)

label_Commentaire = ctk.CTkLabel(master = frame_questCommentaire,text="Décrivez l'incident négatif : ")
label_Commentaire.pack(pady=(10,5))
label_Commentaire.configure(font=("Helvetica", 15))
# Créer une zone de texte pour les commentaires
entry_Commentaire = ctk.CTkTextbox(master=frame_questCommentaire, width=400, height=100)
entry_Commentaire.pack(pady=5)

# Fonction pour ajouter le placeholder
def add_placeholder(event=None):
    if entry_Commentaire.get("1.0", "end-1c") == "":
        entry_Commentaire.insert("1.0", "Description de l'incident négatif...")

# Fonction pour retirer le placeholder
def remove_placeholder(event):
    if entry_Commentaire.get("1.0", "end-1c") == "Description de l'incident négatif...":
        entry_Commentaire.delete("1.0", "end")

# Ajouter le placeholder initialement
entry_Commentaire.insert("1.0", "Description de l'incident négatif...")

# Lier les événements focus in et focus out pour gérer le placeholder
entry_Commentaire.bind("<FocusIn>", remove_placeholder)
entry_Commentaire.bind("<FocusOut>", add_placeholder)

###### Page suivante


button_Type_Concentration = ctk.CTkButton(master=frame_quest, text="Suivant", command=Type_Concentration)
button_Type_Concentration.pack( padx= 10, pady=10)


button_Concentration_Type = ctk.CTkButton(master=frame_quest, text="Retour", command=Concentration_Type)






# TODO            # Echelle du niveau de concentration

def magnet_likert_concentration(valeur_actuelle) :
    """Magnetise la valeur à la plus proche sur l'echelle de likert """
    liste = [0, 16 , 33 , 50, 66, 83, 100]

    nouvelle_val = min(liste, key=lambda val: abs(val - valeur_actuelle))
    sliderConcentration.set(nouvelle_val)

frame_questConcentration = ctk.CTkFrame(master = frame_quest)

label_Concentration = ctk.CTkLabel(master = frame_questConcentration,text="Sur une échelle de 1 à 7, comment évalueriez-vous votre niveau de concentration \n au moment où incident négatif a été commis ?")
label_Concentration.pack(pady=10)
label_Concentration.configure(font=("Helvetica", 15))



###Slider

cadreConcentration = ctk.CTkFrame(master=frame_questConcentration)
cadreConcentration.pack(anchor=tk.CENTER, pady=10)


label_Concentration_0 = ctk.CTkLabel(master = cadreConcentration,text="Très faible")
label_Concentration_0.grid(row=0, column=0, padx=10)
label_Concentration_0.configure(font=("Helvetica",13),text_color='green')

label_Concentration_1 = ctk.CTkLabel(master = cadreConcentration,text="Faible")
label_Concentration_1.grid(row=0, column=1, padx=10)
label_Concentration_1.configure(font=("Helvetica",13),text_color='green')

label_Concentration_2 = ctk.CTkLabel(master = cadreConcentration,text="Plutôt faible")
label_Concentration_2.grid(row=0, column=2, padx=10)
label_Concentration_2.configure(font=("Helvetica",13),text_color='green')

label_Concentration_3 = ctk.CTkLabel(master = cadreConcentration,text="Neutre")
label_Concentration_3.grid(row=0, column=3, padx=10)
label_Concentration_3.configure(font=("Helvetica",13),text_color='white')


label_Concentration_4 = ctk.CTkLabel(master = cadreConcentration,text="Plutôt élevé")
label_Concentration_4.grid(row=0, column=4, padx=10)
label_Concentration_4.configure(font=("Helvetica",13),text_color='red')

label_Concentration_5 = ctk.CTkLabel(master = cadreConcentration,text="Élevé")
label_Concentration_5.grid(row=0, column=5, padx=10)
label_Concentration_5.configure(font=("Helvetica",13),text_color='red')

label_Concentration_6 = ctk.CTkLabel(master = cadreConcentration,text="Très élevé")
label_Concentration_6.grid(row=0, column=6, padx=10)
label_Concentration_6.configure(font=("Helvetica",13),text_color='red')

sliderConcentration = ctk.CTkSlider(master = frame_questConcentration, from_=0, to=100, width=425, command=magnet_likert_concentration)
sliderConcentration.pack()
sliderConcentration.set(50.1)

#### #TODO Distraction


# Fonction pour cacher/montrer le cadre en fonction de l'option sélectionnée
def check_selection(*args):
    if selected_optionDistraction.get() == "Oui":
        cadreDetailDistraction.pack(pady=10)
    else:
        entry_Distraction.delete(0, tk.END)
        cadreDetailDistraction.pack_forget()


frame_questDistraction = ctk.CTkFrame(master = frame_quest)

label_Distraction_1 = ctk.CTkLabel(master = frame_questDistraction,text="Étiez-vous distrait(e) par quelque chose au moment où l'incident négatif s'est produit ?")
label_Distraction_1.pack()
label_Distraction_1.configure(font=("Helvetica",15))

selected_optionDistraction = tk.StringVar() #Variable qui stock la séléection oui/non

cadre_boutons = ctk.CTkFrame(master = frame_questDistraction)
cadre_boutons.pack(padx=10,pady=10)

# Radiobutton 1
radio_button_1 = ctk.CTkRadioButton(cadre_boutons, text="Oui", variable=selected_optionDistraction, value="Oui", command= lambda : cadreDetailDistraction.pack(padx=10,pady=10))
radio_button_1.grid(row=1, column=0, pady=5, padx=10)

# Radiobutton 2
radio_button_2 = ctk.CTkRadioButton(cadre_boutons, text="Non", variable=selected_optionDistraction, value="Non")
radio_button_2.grid(row=1, column=1, pady=5, padx=0)

cadreDetailDistraction = ctk.CTkFrame(master = frame_questDistraction)

label_Distraction_2 = ctk.CTkLabel(master = cadreDetailDistraction,text="Si oui, veuillez en spécifier la nature :")
label_Distraction_2.grid(row=0,column=0, pady=5, padx=10)
label_Distraction_2.configure(font=("Helvetica",13))

entry_Distraction = ctk.CTkEntry(master = cadreDetailDistraction)
entry_Distraction.grid(row=0,column=2, pady=5, padx=10)
entry_Distraction.configure(font=("Helvetica",13))

selected_optionDistraction.trace_add("write", check_selection)

##TODO Fatigue

def magnet_likert_Fatigue(valeur_actuelle) :
    """Magnetise la valeur à la plus proche sur l'echelle de likert """
    liste = [0, 16 , 33 , 50, 66, 83, 100]

    nouvelle_val = min(liste, key=lambda val: abs(val - valeur_actuelle))
    sliderFatigue.set(nouvelle_val)

frame_questFatigue = ctk.CTkFrame(master = frame_quest)

label_Fatigue = ctk.CTkLabel(master = frame_questFatigue,text="Sur une échelle de 1 à 7, à quel point vous sentiez-vous mentalement \n fatigué au moment de l'incident négatif ?")
label_Fatigue.pack(pady=10)
label_Fatigue.configure(font=("Helvetica", 15))



###Slider

cadreFatigue = ctk.CTkFrame(master=frame_questFatigue)
cadreFatigue.pack(anchor=tk.CENTER, pady=10)


label_Fatigue_0 = ctk.CTkLabel(master = cadreFatigue,text="Pas fatigué")
label_Fatigue_0.grid(row=0, column=0, padx=10)
label_Fatigue_0.configure(font=("Helvetica",13),text_color='green')

label_Fatigue_1 = ctk.CTkLabel(master = cadreFatigue,text="Très peu fatigué")
label_Fatigue_1.grid(row=0, column=1, padx=10)
label_Fatigue_1.configure(font=("Helvetica",13),text_color='green')

label_Fatigue_2 = ctk.CTkLabel(master = cadreFatigue,text="Peu fatigué")
label_Fatigue_2.grid(row=0, column=2, padx=10)
label_Fatigue_2.configure(font=("Helvetica",13),text_color='green')

label_Fatigue_3 = ctk.CTkLabel(master = cadreFatigue,text="Neutre")
label_Fatigue_3.grid(row=0, column=3, padx=10)
label_Fatigue_3.configure(font=("Helvetica",13),text_color='white')


label_Fatigue_4 = ctk.CTkLabel(master = cadreFatigue,text="Plutôt fatigué")
label_Fatigue_4.grid(row=0, column=4, padx=10)
label_Fatigue_4.configure(font=("Helvetica",13),text_color='red')

label_Fatigue_5 = ctk.CTkLabel(master = cadreFatigue,text="fatigué")
label_Fatigue_5.grid(row=0, column=5, padx=10)
label_Fatigue_5.configure(font=("Helvetica",13),text_color='red')

label_Fatigue_6 = ctk.CTkLabel(master = cadreFatigue,text="Vraiment fatigué")
label_Fatigue_6.grid(row=0, column=6, padx=10)
label_Fatigue_6.configure(font=("Helvetica",13),text_color='red')

sliderFatigue = ctk.CTkSlider(master = frame_questFatigue, from_=0, to=100, width=500, command=magnet_likert_Fatigue)
sliderFatigue.pack()
sliderFatigue.set(50.1)

####### Difficulte

frame_questDifficulte = ctk.CTkFrame(master = frame_quest)


label_Difficulte_1 = ctk.CTkLabel(master = frame_questDifficulte,text="Comment qualifieriez-vous la difficulté de la tâche au moment de l'incident négatif ?")
label_Difficulte_1.pack()
label_Difficulte_1.configure(font=("Helvetica",15))

selected_optionDifficulte = tk.StringVar() #Variable qui stock la séléection

cadre_boutons = ctk.CTkFrame(master = frame_questDifficulte)
cadre_boutons.pack(padx=10,pady=10)


button_difficult_1 = ctk.CTkRadioButton(cadre_boutons, text="Très Simple", variable=selected_optionDifficulte, value="Très Simple")
button_difficult_1.grid(row=1, column=0, pady=5, padx=10)

button_difficult_2 = ctk.CTkRadioButton(cadre_boutons, text="Simple", variable=selected_optionDifficulte, value="Simple")
button_difficult_2.grid(row=1, column=1, pady=5, padx=0)

button_difficult_3 = ctk.CTkRadioButton(cadre_boutons, text="Moyenne", variable=selected_optionDifficulte, value="Moyenne")
button_difficult_3.grid(row=1, column=2, pady=5, padx=0)

button_difficult_4 = ctk.CTkRadioButton(cadre_boutons, text="Difficile", variable=selected_optionDifficulte, value="Difficile")
button_difficult_4.grid(row=1, column=3, pady=5, padx=0)

button_difficult_5 = ctk.CTkRadioButton(cadre_boutons, text="Très Difficile", variable=selected_optionDifficulte, value="Très Difficile")
button_difficult_5.grid(row=1, column=4, pady=5, padx=0)


#TODO            # Screen ?


# # ✔ TODO "Annuler" et fin "done" retour page bouton + fontion reset_entry()
def reset_entry(list_val = ['','',50,"",50.1,'','',50.1,'']) :
    """
    Fait en sorte que les entry soient mises sur les val correspondantes lors de la prochaine ouverture de la page questionnaire
    """
#   Entry Recherche Type

    entry_actualise_options.delete(0,tk.END)
    entry_actualise_options.insert(tk.END, list_val[0])

    # entry_rajouter_typeErreur.delete(0,tk.END)
    # entry_rajouter_typeErreur.insert(tk.END, list_val[0])
    #
    # entry_rajouter_typeErreurD.delete(0,tk.END)
    # entry_rajouter_typeErreurD.insert(tk.END, list_val[0])
    #
    # if cadreNouveauType.winfo_ismapped():
    #     cadreNouveauType.pack_forget()
    #
    # for widget in affichage_boutons.winfo_children():
    #     widget.destroy()

#Faute

    selected_option_Bad.set(list_val[1])


#   Likert Importance/Gravité

    sliderImportance.set(list_val[2])

#   TextBox description + Placeholder

    entry_Commentaire.delete("1.0", tk.END)
    entry_Commentaire.insert("1.0", list_val[3])
    add_placeholder("<FocusOut>")

#   Likert Concentration

    sliderConcentration.set(list_val[4])

#   Choix Distraction

    selected_optionDistraction.set(list_val[5])

    #   Nature distraction

    entry_Distraction.delete(0,tk.END)
    entry_Distraction.insert(tk.END, list_val[6])

#   Likert Fatigue

    sliderFatigue.set(list_val[7])

#   Choix Difficulté

    selected_optionDifficulte.set(list_val[8])






def sauvegarderQuest() :
    """
    # Logique "Done" :
          Verifier type :
              d'erreur.entry_get() non vide
          Stocker les entry dans des variables
          ajouter à "../DATA/n°Ano/Data_n°Ano.xls"
         Puis appeler reset_entre
         RetourPage2

    """

    # Récupération des données :

    type = get_selected_button_value()
    faute = selected_option_Bad.get()
    niveau_importance = dic_likert_Importance[sliderImportance.get()]
    description = entry_Commentaire.get("1.0", tk.END).strip()
    niveau_concentration = dic_likert_Concentration[sliderConcentration.get()]
    distraction = selected_optionDistraction.get()
    natureDistration = entry_Distraction.get()
    niveau_fatigue = dic_likert_Fatigue[sliderFatigue.get()]
    niveau_difficulte = selected_optionDifficulte.get()

    if id_time_code-1 >= 0 : #ID d'erreurs indiquées au bon moment ont un id positif et de param 0
        parameter = 0       #Les erreurs oubliées ont un id négatif et sont donc de param 1
    else :
        parameter = 1

    path = f"../Data/{n_anonymat}/Record_{n_anonymat}_{horodatage_start}.edf"


    if ( type != '') and ( description != "Description de l'incident négatif...") and ( description != "") and ( distraction != '') and (niveau_difficulte != '') and (niveau_concentration != ' ') and (niveau_fatigue != ' ') :
        if ( distraction == "Oui") :
            if ( natureDistration != '' ) :


                nouvelle_ligne = pd.DataFrame({
                    "ID" : [dernier_id],
                    "Path" : [path],
                    "Timecode" : [dernier_time_code],
                    "Parameter" : [dernier_parametre],
                    "ID Cible" : [''],
                    "Type" : [type],
                    "Faute" : [faute],
                    "Importance" : [niveau_importance],
                    "Description" : [description] ,
                    "Concentration" : [niveau_concentration] ,
                    "Distrait" : [distraction],
                    "NatureDistraction" : [natureDistration] ,
                    "Fatigue" : [niveau_fatigue] ,
                    "Difficulte" : [niveau_difficulte]})

                df = pd.read_excel(excel_path)
                df = pd.concat([df, nouvelle_ligne])
                df.to_excel(excel_path, index=False)
                reset_entry()
                retourPage2()

        elif (distraction == "Non") :
            if (natureDistration == '') :

                nouvelle_ligne = pd.DataFrame({
                    "ID": [dernier_id],
                    "Path": [path],
                    "Timecode": [dernier_time_code],
                    "Parameter": [dernier_parametre],
                    "ID Cible": [''],
                    "Type" : [type],
                    "Faute" : [faute],
                    "Importance": [niveau_importance],
                    "Description": [description],
                    "Concentration": [niveau_concentration],
                    "Distrait": [distraction],
                    "NatureDistraction": [natureDistration],
                    "Fatigue": [niveau_fatigue],
                    "Difficulte": [niveau_difficulte]})

                df = pd.read_excel(excel_path)
                df = pd.concat([df, nouvelle_ligne])
                df.to_excel(excel_path, index=False)
                reset_entry()
                retourPage2()



button_done = ctk.CTkButton(master=frame_quest, text="Envoyer le questionnaire Complet", command=lambda : sauvegarderQuest())

text_button_done = "Si vous avez intentionnellement laissé les échelles sur neutre, \nil est nécessaire de les déplacer puis de les remettre sur neutre afin que la réponse soit prise en compte."

button_done.bind("<Enter>",lambda event,text = text_button_done: show_tooltip(event, text))
button_done.bind("<Leave>", hide_tooltip)
button_done.bind("<Motion>", move_tooltip)

button_done_modif = ctk.CTkButton(master=frame_quest, text="Sauvegarder les changements", command=lambda : sauvegarder_modif())

bouton_envoyer_etat = ctk.CTkButton(master=frame_quest, text="Envoyer en l'état",command=choisir_envoyer_etat)
bouton_envoyer_etat.pack(pady=10, side=tk.BOTTOM)
root.mainloop()