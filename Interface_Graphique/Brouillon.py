import customtkinter as ctk
from tkinter import Toplevel
import pandas as pd
import tkinter as tk

# Lire les données du fichier Excel
df_types = pd.read_excel("/mnt/data/image.png")  # Modifier avec le bon chemin

options = list(df_types['Types'])
description = list(df_types['Description'])

# Création de la fenêtre principale
root = ctk.CTk()
root.geometry("600x400")

frame_quest = ctk.CTkFrame(master=root)
frame_quest.pack(pady=10, padx=10, fill="both", expand=True)

frame_questType = ctk.CTkFrame(master=frame_quest)
frame_questType.pack(pady=5, padx=50, fill="both", expand=True)

label_typeErreur = ctk.CTkLabel(master=frame_questType, text="Veuillez renseigner la nature de l'erreur commise")
label_typeErreur.pack(pady=10)
label_typeErreur.configure(font=("Helvetica", 15))

affichage_boutons = ctk.CTkFrame(master=frame_questType)
affichage_boutons.pack(anchor=tk.CENTER, padx=10, pady=10)

# Dictionnaire pour maintenir l'état des boutons
button_states = {}

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

# Fonction pour afficher la bulle d'info lors du survol
def show_tooltip(event, text):
    global tooltip_window
    if tooltip_window:
        return
    x, y = event.widget.winfo_pointerxy()
    tooltip_window = Toplevel(event.widget)
    tooltip_window.wm_overrideredirect(True)
    tooltip_window.wm_geometry(f"+{x + 20}+{y + 20}")
    tooltip_window.attributes("-alpha", 0.9)  # Réglez la transparence ici
    label = tk.Label(tooltip_window, text=text, bg="black", fg="white")
    label.pack(ipady=5, ipadx=5)

# Fonction pour cacher la bulle d'info lorsque la souris quitte le bouton
def hide_tooltip(event):
    global tooltip_window
    if tooltip_window:
        tooltip_window.destroy()
        tooltip_window = None

# Fonction pour déplacer la bulle d'info lorsque la souris se déplace
def move_tooltip(event):
    global tooltip_window
    if tooltip_window:
        x, y = event.widget.winfo_pointerxy()
        tooltip_window.wm_geometry(f"+{x + 20}+{y + 20}")

# Créer et placer les boutons avec gestion de l'état et tooltips
def creation_boutons_type():
    i, j = 0, 0
    for k in range(len(options)):
        e = options[k]
        d = description[k]

        button_states[e] = False

        button = ctk.CTkButton(affichage_boutons, text=e, fg_color="#2FA572", width=button_width, height=button_height)
        button.configure(command=lambda btn=button, opt=e: toggle_button(btn, opt))
        button.grid(row=j, column=i, pady=5, padx=5)

        if i + 1 == 6:
            i = 0
            j += 1
        else:
            i += 1

        # Lien des événements de survol au bouton
        button.bind("<Enter>", lambda event, text=d: show_tooltip(event, text))
        button.bind("<Leave>", hide_tooltip)
        button.bind("<Motion>", move_tooltip)

creation_boutons_type()

# Boucle principale de l'application
root.mainloop()
