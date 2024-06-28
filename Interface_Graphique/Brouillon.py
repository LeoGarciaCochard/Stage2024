import tkinter as tk
from datetime import datetime
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Exemple avec CTk")
root.geometry("1080x720")

frame_participant = ctk.CTkFrame(master=root)
frame_participant.pack(pady=20, padx=20, fill="both", expand=True)

########## Variables :

selected_var_heure = datetime.now().strftime("%Hh%M")

##Informations personnelles :

selected_var_age = tk.StringVar()
selected_var_genre = tk.StringVar()

##Informations de contexte :

selected_var_sommeil = tk.StringVar()
selected_var_trouble_sommeil = tk.StringVar()
selected_var_stress = tk.StringVar()

selected_var_cafeine = tk.StringVar()
selected_var_quantite_cafeine = 0

selected_var_nicotine = tk.StringVar()
selected_var__quantite_nicotine = 0

##Travail :

selected_var_hability_inf = tk.StringVar()
selected_var_experience = tk.StringVar()
selected_var_passion_job = tk.StringVar()

selected_var_distractions_travail = tk.StringVar()
selected_var_bruit = tk.StringVar()

########## Titre :

cadre_participantTitre = ctk.CTkFrame(master=frame_participant)
cadre_participantTitre.pack(pady=25, padx=50)

label_participantTitre = ctk.CTkLabel(master= cadre_participantTitre, text="Merci de remplir ces informations anonymes")
label_participantTitre.pack(pady=10, padx=50)
label_participantTitre.configure(font=("Helvetica", 35,"bold"))

########## Titre IP (Info Perso) :

cadre_participantIP = ctk.CTkFrame(master=frame_participant)
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

frame_age= ctk.CTkFrame(master=frame_participant)
frame_age.pack(padx= 50, pady=10, fill="both")

label_box_age = ctk.CTkLabel(master=frame_age, text="Veuillez cliquer ici pour renseigner votre âge :   ...", cursor="hand2")
label_box_age.grid(row=0,column=0, ipadx=5, ipady=5)
label_box_age.bind("<Button-1>", command=lambda x: ouvrir_menu_age())


########## Genre :

def change_genre(genre):
    global selected_var_genre
    selected_var_genre = genre

frame_genre = ctk.CTkFrame(master=frame_participant)
frame_genre.pack(padx= 50, pady=10, fill="both")

label_genre = ctk.CTkLabel(master=frame_genre, text="Veuillez renseigner votre genre : ")
label_genre.grid(row=0,column=0, ipadx=5, ipady=5)

combobox_genre = ctk.CTkComboBox(master=frame_genre, values=["Femme","Homme","Autre"], state="readonly", command= lambda x : change_genre(x))
combobox_genre.grid(row=0,column=1)

########## Situation personelle :

########## Titre SP (Situation personelle) :

cadre_participantSP = ctk.CTkFrame(master=frame_participant)
cadre_participantSP.pack(pady=10, padx=50)

label_participantSP = ctk.CTkLabel(master= cadre_participantSP, text="Situation personelle :")
label_participantSP.pack(pady=5, padx=50)
label_participantSP.configure(font=("Helvetica", 15))

########## Sommeil :

frame_sommeil = ctk.CTkFrame(master=frame_participant)
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

label_sommeil = ctk.CTkLabel(master=frame_sommeil, text="Souffez vous de troubles du sommeil : ")
label_sommeil.grid(row=1,column=0, ipadx=5, ipady=5)

combobox_genre = ctk.CTkComboBox(master=frame_sommeil, values=["Oui","Non"], state="readonly", command= lambda x : change_troubles_sommeil(x))
combobox_genre.grid(row=1,column=1)

########## Stess :







######### Bouton + Vérif

def printed() :
    print(  selected_var_heure,
            selected_var_age,
            selected_var_genre,

            selected_var_sommeil,
            selected_var_trouble_sommeil,
            selected_var_stress,

            selected_var_cafeine,
            selected_var_quantite_cafeine,

            selected_var_nicotine,
            selected_var__quantite_nicotine,

            selected_var_hability_inf,
            selected_var_experience,
            selected_var_passion_job,

            selected_var_distractions_travail,
            selected_var_bruit)


button_versB = ctk.CTkButton(master = frame_participant, text="Suivant", width= 250, height=60, command=printed)
button_versB.configure(font=("Helvetica", 20, "bold"))
button_versB.pack(pady=10, padx=10)


root.mainloop()
