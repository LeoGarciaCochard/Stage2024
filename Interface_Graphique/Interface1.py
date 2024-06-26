import tkinter
## Interface Graphique pour récupérations de données EEG sur l'ErrP


# ✔ TODO    #Page1 d'acceuil simple
# ✔ TODO        #Renseigner le numéro d'anonymat pour identifier la data qui sera enregistré.

# ✔TODO    #Changer de page vers Page2 : Bouton "J'ai commis une erreur"

# ✔TODO  #Changer de page vers page3 : Questionnaire
#            # Revenir
#            # Type de l'erreur
#            # Echelle d'Concentration de l'erreur
#            # Echelle du niveau de concentration
#            # Commentaires
#            # Screen ?

# ✔ TODO    #Revenir sur la page2.

# ✔ Todo bouton femer


########################################################################### Imports

from tkinter import ttk
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
from tkinter import Toplevel, Label

########################################################################### Variables Globales

screen_width = 3072
width = 1000                        #Taille de la fenêtre
height = 800                          #Taille de la fenêtre
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
                         50: "Neutre",
                         66: "Plutôt élevé",
                         83: "Elevé",
                         100: "Très élevé"}


dic_likert_Fatigue =    { 0: "Pas fatigué",
                         16: "Très peu fatigué",
                         33: "Peu fatigué",
                         50: "Neutre",
                         66: "Plutôt fatigué",
                         83: "Fatigué",
                         100: "Vraiment fatigué"}

path_img_btn = "../Sources/btn.png"
path_img_btnf = "../Sources/btn_f.png"

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

openvibe_executable = r"C:\Program Files\openvibe-3.6.0-64bit\bin\openvibe-designer.exe"

scenario_file_Ecriture = r"C:\Users\milio\PycharmProjects\Stage\OpenVibe\Scenario\EcritureEEG.xml"
scenario_file_Stim = r"C:\Users\milio\PycharmProjects\Stage\OpenVibe\Scenario\placementStimulation.xml"

record_ov = r"C:/Users/milio/PycharmProjects/Stage/OpenVibe/enregistrement_en_cours/record.ov"

path_recordStim_edf = r"C:/Users/milio/PycharmProjects/Stage/OpenVibe/enregistrements_avec_stim/recordStim.edf"
path_recordStim_ov = r"C:/Users/milio/PycharmProjects/Stage/OpenVibe/enregistrements_avec_stim/recordStim.ov"



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
                1 si l'erreur est déclérée à posteriori
                2 le moment ou l'erreur est déclarée à posteriori

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

        global description_ajout_rapide

        nouvelle_ligne2 = pd.DataFrame({
            "ID": [dernier_id],
            "Path": [f"../Data/{n_anonymat}/Record_{n_anonymat}_{horodatage_start}.edf"],
            "Timecode": [dernier_time_code],
            "Parameter": [dernier_parametre],
            "Description": [description_ajout_rapide]})
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
        arreterRecEEG()
        root.destroy()



########################################################################### Frame 1 : Page d'accueil

# ✔ TODO sur page numéro anonymat : creer un repertoire du numéro d'anonymat dans "../DATA/n°Ano" + creer un fichier Excel "../DATA/n°Ano/Data_n°Ano.xls"
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
        colonnes = ["ID", "Path", "Timecode", "Parameter","ID Cible" , "Type","Faute", "Importance","Description", "Concentration",
                    "Distrait","NatureDistraction", "Fatigue", "Difficulte"]
        df = pd.DataFrame(columns=colonnes)
        df.to_excel(excel_path, index=False)                                                                    #S'il n'éxiste pas on enregistre le fichier Excel


def versPage2() :
    """
    Stock le n° d'anonymat dans n_anonymat puis affiche la page suivante si l'entrée est un nombre, ne fait rien sinon
    """
    try :
        global n_anonymat
        n_anonymat = int(entry_n_anonymat.get())

        frame_acc.pack_forget()
        frame_info.pack(pady=20, padx=50, fill="both", expand=True)

        versB() #TODO RETIRER

    except Exception as e :
        print("Ca bug")
        print(f"Erreur : {e}")


def versB() :
    affichePageB()
    creer_repertoire(n_anonymat)
    start_recording_thread()


frame_info = ctk.CTkFrame(master=root)

image_path = "../Sources/Information_R.png"
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)

# Afficher l'image dans un label
label_image = tk.Label(master=frame_info, image=photo)
label_image.pack(pady=(100,20), padx=10)

button_versB = ctk.CTkButton(master = frame_info, text="Compris !", command=versB, width= 250, height=60)
button_versB.configure(font=("Helvetica", 30, "bold"))
button_versB.pack(pady=10, padx=10)




#TODO -moments ou j'ai oublié


def affichePageB() :
    """
    Retire la page 1 (frame_acc) et affiche la 2 (frame_button)
    """
    frame_info.pack_forget()
    frame_button.pack(pady=20, padx=50, fill="both", expand=True)
    button_err.pack(pady=((height / 2) -100  , 30), padx=10)

    button_errForget.pack(pady=10, padx=10)
    button_voir_err.pack(pady=0, padx=10)
    label_image_btn.pack(pady=(15, 10), padx=(0, 105))
    entry_cachee.focus_set()                                                                                            #TODO retirer ca #Subterfuge pour appuyer sur le bouton Erreur avec "entrée"

frame_acc = ctk.CTkFrame(master=root)
frame_acc.pack(pady=20, padx=50, fill="both", expand=True)

entry_n_anonymat = ctk.CTkEntry(master=frame_acc, placeholder_text=("N° d'anonymat"))
entry_n_anonymat.pack(pady=(50+(height//2),0), padx=10)



button_vers2 = ctk.CTkButton(master=frame_acc, text="Suivant", command=lambda : versPage2())
button_vers2.pack(pady=10, padx=10)

entry_n_anonymat.bind("<Return>", lambda x : versPage2())


def on_enter2(event):
    button_acc_f4.configure(text="❌ Fermer")
def on_leave2(event):
    button_acc_f4.configure(text="❌")

button_acc_f4 = ctk.CTkButton(master = frame_acc, text="❌", width=15, command=lambda : arretExpe(True))
button_acc_f4.configure(fg_color="red", hover_color="white", text_color="black")
button_acc_f4.pack()
button_acc_f4.place(x=5,y=5)

button_acc_f4.bind("<Enter>", on_enter2)
button_acc_f4.bind("<Leave>", on_leave2)

########################################################################### Frame 2 : Page d'utilisateur avec bouton

def forgottenErr1() :

    button_errForget.pack_forget()
    button_voir_err.pack_forget()
    label_image_btn.pack_forget()
    frame_button_cadre.pack(pady=10, padx=10)
    unpack_textbox()
    label_forget.pack(pady=10, padx=10)
    entry_forgotten.pack(pady=5, padx=10)
    button_errForget2.pack(pady=5, padx=10)
    button_voir_err.pack(pady=0, padx = 10)
    label_image_btn.pack(pady=(15, 10), padx=(0, 105))


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
    """Retire la page 2 et affiche le questionnaire"""
    # reset_entry(list_val) list_val = ['',50,"",50,'','',50,'']
    frame_button.pack_forget()
    button_errForget.pack_forget()
    entry_forgotten.pack_forget()
    button_errForget2.pack_forget()
    button_voir_err.pack_forget()
    label_image_btn.pack_forget()
    label_forget.pack_forget()
    frame_quest.pack(pady=20, padx=50, fill="both", expand=True)
    creation_boutons_type()
    Concentration_Type()


frame_button = ctk.CTkFrame(master=root)
button_err = ctk.CTkButton(master = frame_button, text="Renseigner un incident négatif",command=lambda : stimulation(0))
button_err.configure(height=200, width=200, corner_radius=20, font=("Helvetica", 30, "bold") )


#TODO AjoutRapide

def unpack_textbox() :
    textbox_description.delete("1.0", tk.END)
    textbox_description.pack_forget()
    textbov_validation.pack_forget()

def pack_text_box() :
    textbox_description.pack(pady=10, padx=10)
    textbov_validation.pack(pady=10, padx=10)
    textbox_description.focus_set()

def recup_desc() :
    # Récupère la description :
    global description_ajout_rapide
    description_ajout_rapide = textbox_description.get("1.0", tk.END).strip()

    #Stimule :
    stimulation(3)
    unpack_textbox()




textbox_description = ctk.CTkTextbox(master= frame_button, width= 100, height=50)
textbov_validation = ctk.CTkButton(master = frame_button, text= "Valider ou Ignorer", command=recup_desc)



def on_enter3(event):
    label_image_btn.configure(image=photo_btnf)
def on_leave3(event):
    label_image_btn.configure(image=photo_btn)


image_btn = Image.open(path_img_btn)
image_btn_resized = image_btn.resize((100, 100), Image.LANCZOS)
photo_btn = ctk.CTkImage(light_image=image_btn_resized, dark_image=image_btn_resized, size=(100, 60))

image_btnf = Image.open(path_img_btnf)
image_btnf_resized = image_btnf.resize((100, 100), Image.LANCZOS)
photo_btnf = ctk.CTkImage(light_image=image_btnf_resized, dark_image=image_btnf_resized, size=(100, 60))

# Afficher l'image dans un label
label_image_btn = ctk.CTkLabel(master=frame_button, image=photo_btn ,text='                                        Ajout Rapide', cursor="hand2")
label_image_btn.configure(font=('Helvetica',15))


label_image_btn.bind("<Button-1>", command=lambda x: pack_text_box())
label_image_btn.bind("<Enter>", on_enter3)
label_image_btn.bind("<Leave>", on_leave3)


#TODO Trouver bonne forme

frame_button_cadre = ctk.CTkFrame(master=frame_button)


button_errForget = ctk.CTkButton(master = frame_button, text="J'ai oublié de renseigner un incident négatif", command=forgottenErr1)
button_errForget.configure(font=("Helvetica",15),height=50, width=300)

label_forget = ctk.CTkLabel(master = frame_button_cadre, text="Combien de temps s'est-il passé depuis l'incident négatif ? \n (En minutes)")
label_forget.configure(font=("Helvetica", 15))

entry_forgotten = ctk.CTkEntry(master = frame_button_cadre, placeholder_text=("Temps en minutes"))
entry_forgotten.bind("<Return>", lambda x : forgottenErr2())

button_errForget2 = ctk.CTkButton(master = frame_button_cadre, text="Valider", command=forgottenErr2)

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



    frame_recap.pack(pady=15, padx=30, fill="both", expand=True)

button_voir_err = ctk.CTkButton(master = frame_button, text="Voir ses incidents négatifs", command=vers_frame_tab_err)
button_voir_err.configure(font=("Helvetica",15))
button_voir_err.configure(height=50, width=300)


########################################################################### Frame Speciale : Voir erreurs

def sortir_recap() :
    """
    retourne vers la page 2
    """
    frame_recap.pack_forget()
    frame_button.pack(pady=20, padx=50, fill="both", expand=True)
    button_err.pack(pady=((height / 2) - 100, 30), padx=10)
    button_errForget.pack(pady=10, padx=10)
    frame_button_cadre.pack_forget()
    button_voir_err.pack_forget()
    unpack_textbox()
    label_image_btn.pack_forget()

    button_voir_err.pack(pady=0, padx=10)
    label_image_btn.pack(pady=(15, 10), padx=(0, 105))
    entry_cachee.focus_set()
    clear_table()

frame_recap = ctk.CTkFrame(master=root)

frame_recapTitre = ctk.CTkFrame(master=frame_recap)
frame_recapTitre.pack(pady=25, padx=50)

label_TitreRecap = ctk.CTkLabel(master= frame_recapTitre, text="Récapitulatif des incidents négatifs commises")
label_TitreRecap.pack(pady=10, padx=50)
label_TitreRecap.configure(font=("Helvetica", 35))

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

    if ( type != '') and ( description != "Description de l'incident négatif...") and ( description != "") and ( distraction != '') and (niveau_difficulte != '') :
        if ( distraction == "Oui") :
            if ( natureDistration != '' ) :

                df = pd.read_excel(excel_path)

                updates = {
                    "Type" : type,
                    "Faute" : faute,
                    "Importance" : niveau_importance,
                    "Description" : description ,
                    "Concentration" : niveau_concentration ,
                    "Distrait" : distraction,
                    "NatureDistraction" : natureDistration ,
                    "Fatigue" : niveau_fatigue ,
                    "Difficulte" : niveau_difficulte}

                for column, new_value in updates.items():
                    df.at[row_modif, column] = new_value

                df.to_excel(excel_path, index=False)

                reset_entry()
                button_done_modif.pack_forget()
                button_quit_Modif.place_forget()

                button_quit.place(x=5,y=5)
                frame_quest.pack_forget()

                frame_button.pack(pady=20, padx=50, fill="both", expand=True)

                entry_forgotten.delete(0, tk.END)
                frame_button_cadre.pack_forget()
                unpack_textbox()
                label_image_btn.pack_forget()
                button_errForget.pack(pady=10, padx=10)
                button_voir_err.pack(pady=0, padx=10)
                label_image_btn.pack(pady=(15, 10), padx=(0, 105))

        elif (distraction == "Non"):
            if (natureDistration == ''):

                df = pd.read_excel(excel_path)

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

                entry_forgotten.delete(0, tk.END)
                frame_button_cadre.pack_forget()
                unpack_textbox()
                label_image_btn.pack_forget()
                button_errForget.pack(pady=10, padx=10)
                button_voir_err.pack(pady=0, padx=10)
                label_image_btn.pack(pady=(15, 10), padx=(0, 105))



            #ANNULER MODIF PRESENT ET SauvegarderModif aussi après utilisation





def affiche_Quest_Modif() :

    frame_quest.pack(pady=20, padx=50, fill="both", expand=True)
    button_quit.place_forget()
    button_quit_Modif.place(x=5, y=5)
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
    frame_recap.pack_forget()
    actualisation_options()
    if entry_Distraction.get() == 'NaN' :
        entry_Distraction.delete(0, tk.END)

    affiche_Quest_Modif()

def display_table(columns_to_exclude=["Path","ID Cible" ,"Timecode", "Parameter"]):
    global excel_path, frame_tableau

    df = pd.read_excel(excel_path)

    # Filtrer les colonnes indésirables :

    df_filtered = df[df['Parameter'] != 2]
    #Supprimer les lignes dont la colonne "Parameter" est == 2

    df_filtered = df[df['Parameter'] != 3]
    # Supprimer les lignes dont la colonne "Parameter" est == 3

    df_filtered = df_filtered.drop(columns=columns_to_exclude)


    frame_tableau = ctk.CTkFrame(master=scrollable_frame)
    frame_tableau.pack(fill="both", expand=True)

    # Ajout des en-têtes de colonnes
    headers = ["Modifier"] + list(df_filtered.columns)
    for col_num, col_name in enumerate(headers):
        header = ctk.CTkLabel(frame_tableau, text=col_name)
        header.grid(row=0, column=col_num, padx=10, pady=5)

    # Insérer les données et les boutons
    for row_num, row in df_filtered.iterrows():
        # Ajouter un bouton dans la première colonne
        button = ctk.CTkButton(frame_tableau, text="Modifier", width=50,
                               command=lambda row=row_num: modifier_ligne(row))
        button.grid(row=row_num + 1, column=0, padx=10, pady=5)

        # Ajouter les autres cellules
        for col_num, value in enumerate(row):
            cell = ctk.CTkLabel(frame_tableau, text=value)
            cell.grid(row=row_num + 1, column=col_num + 1, padx=10, pady=5)
    on_frame_configure()


def clear_table():
    global frame_tableau
    if frame_tableau:
        frame_tableau.destroy()
        frame_tableau = None

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
    """Retire le questionnaire et affiche la page 2"""
    #TODO supprimer_rec(dernier_rec_path)

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



    reset_entry()
    frame_quest.pack_forget()
    frame_button.pack(pady=20, padx=50, fill="both", expand=True)
    entry_forgotten.delete(0, tk.END)
    frame_button_cadre.pack_forget()
    unpack_textbox()
    label_image_btn.pack_forget()
    button_errForget.pack(pady=10, padx=10)
    button_voir_err.pack(pady=0, padx=10)
    label_image_btn.pack(pady=(15, 10), padx=(0, 105))

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

# Initialisation de la variable globale
tooltip_window = None

# # Fonction pour afficher la bulle d'info lors du survol
# def show_tooltip(event, text):
#     global tooltip_window
#     if tooltip_window:
#         return
#     x, y = event.widget.winfo_pointerxy()
#     tooltip_window = Toplevel(event.widget)
#     tooltip_window.wm_overrideredirect(True)
#     tooltip_window.wm_geometry(f"+{x + 20}+{y + 20}")
#     frame = ctk.CTkFrame(tooltip_window,fg_color=None)
#     frame.pack()
#     label = ctk.CTkLabel(frame, text=text, text_color="white", fg_color="black")
#     label.pack(ipady=5, ipadx=5)
#
#
# # Fonction pour cacher la bulle d'info lorsque la souris quitte le bouton
# def hide_tooltip(event):
#     global tooltip_window
#     if tooltip_window:
#         tooltip_window.destroy()
#         tooltip_window = None
#
# # Fonction pour déplacer la bulle d'info lorsque la souris se déplace
# def move_tooltip(event):
#     global tooltip_window
#     if tooltip_window:
#         x, y = event.widget.winfo_pointerxy()
#         tooltip_window.wm_geometry(f"+{x + 20}+{y + 20}")
#
#


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


# Fonction pour déplacer la bulle d'info lorsque la souris se déplace
# def move_tooltip(event):
#     global tooltip_window
#     if tooltip_window:
#         x, y = event.widget.winfo_pointerxy()
#         screen_width = event.widget.winfo_screenwidth()
#         tooltip_width = tooltip_window.winfo_width()
#         print(f"x :{x} / {screen_width} \n {int(x) <= int(screen_width) // 2} ")
#         if int(x) <= int(screen_width) // 2:
#             print("droite")
#             # Positionner à droite du curseur
#             tooltip_window.wm_geometry(f"+{x + 20}+{y + 20}")
#         else:
#             print("gauche")
#             # Positionner à gauche du curseur
#             tooltip_window.wm_geometry(f"+{x - tooltip_width - 20}+{y + 20}")


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


# Créer et placer les boutons avec gestion de l'état et tooltips
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

        # Lien des événements de survol au bouton
        button.bind("<Enter>", lambda event, text=text_survol: show_tooltip(event, text))
        button.bind("<Leave>", hide_tooltip)
        button.bind("<Motion>", move_tooltip)

creation_boutons_type()

#
# button_plus.pack(pady=5, padx=10)

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
def add_placeholder(event):
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
def reset_entry(list_val = ['','',50,"",50,'','',50,'']) :
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
    # TODO Logique "Done" :
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


    if ( type != '') and ( description != "Description de l'incident négatif...") and ( description != "") and ( distraction != '') and (niveau_difficulte != '') :
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



button_done = ctk.CTkButton(master=frame_quest, text="Envoyer le questionnaire", command=lambda : sauvegarderQuest())

button_done_modif = ctk.CTkButton(master=frame_quest, text="Sauvegarder les changements", command=lambda : sauvegarder_modif())

root.mainloop()