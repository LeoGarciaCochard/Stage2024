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

frame_quest_participant = ctk.CTkFrame(master=frame_participant)
frame_quest_participant.pack(pady=20, padx=20, fill="both", expand=True)

########## Dictionnaires :

dic_stress= {
    0: "Sans stress",  # 11 caractères
    16: "Pas trop stressé(e)",  # 12 caractères
    33: "Légèrement stressé(e)",  # 20 caractères
    50: "Neutre",  # 6 caractères
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
    0: "Pas du tout passionné",        # 20 caractères
    16: "Très peu passionné",          # 18 caractères
    33: "Légèrement passionné",        # 21 caractères
    50: "Passion neutre",              # 14 caractères
    66: "Passionné",                   # 9 caractères
    83: "Très passionné",              # 15 caractères
    100: "Extrêmement passionné"       # 22 caractères
}

dic_Bruit = {
    0: "Pas du tout bruyant",          # 19 caractères
    16: "Très peu bruyant",            # 16 caractères
    33: "Légèrement bruyant",          # 20 caractères
    50: "Bruit neutre",                # 12 caractères
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
selected_var_stress = dic_stress[50]

selected_var_cafeine = tk.StringVar()
selected_var_quantite_cafeine = 0

selected_var_nicotine = tk.StringVar()
selected_var_quantite_nicotine = 0

##Travail :

selected_var_Hability_inf = dic_Hability_inf[53]
selected_var_experience = tk.StringVar()
selected_var_Passion = dic_Passion[50]

selected_var_distractions_travail = tk.StringVar()
selected_var_Bruit = dic_Bruit[50]

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
    liste = [0, 16 , 33 , 50, 66, 83, 100]

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

label_Stress_3 = ctk.CTkLabel(master = cadreStress,text=dic_stress[50])
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

######### Caféine

frame_cafeine = ctk.CTkFrame(master=frame_quest_participant)
frame_cafeine.pack(padx= 50, pady=10, fill="both")
def change_cafeine(rep):
    global selected_var_cafeine
    selected_var_cafeine = rep

    #Actver la quantité si rep == oui
    if rep == "Oui" :
        combobox_quantite_cafeine.configure(state='readonly')
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

##########PAGE 2

frame_quest_participant2 = ctk.CTkFrame(master=frame_participant)
########## Situation Professionelle :

########## Titre SPro (Situation Professionelle) :

cadre_participantSPro = ctk.CTkFrame(master=frame_quest_participant2)
cadre_participantSPro.pack(pady=10, padx=50)

label_participantSPro = ctk.CTkLabel(master= cadre_participantSPro, text="Situation professionelle :")
label_participantSPro.pack(pady=5, padx=50)
label_participantSPro.configure(font=("Helvetica", 15))

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
            selected_var_quantite_nicotine,

            selected_var_Hability_inf,
            selected_var_experience,
            selected_var_Passion,

            selected_var_distractions_travail,
            selected_var_Bruit)

    frame_quest_participant.pack_forget()
    frame_quest_participant2.pack(pady=20, padx=20, fill="both", expand=True)

button_versB = ctk.CTkButton(master = frame_quest_participant, text="Suivant", width= 250, height=60, command=printed)
button_versB.configure(font=("Helvetica", 20, "bold"))
button_versB.pack(pady=10, padx=10)


root.mainloop()
