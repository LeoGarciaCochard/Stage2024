import customtkinter as ctk

# Initialisation de l'application principale
root = ctk.CTk()
root.title("Exemple de RadioButton Personnalisé")
root.geometry("400x300")

# Initialisation de customtkinter
ctk.set_appearance_mode("System")  # Options: "System" (par défaut), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue" (par défaut), "green", "dark-blue"

# Cadre principal
frame_questType = ctk.CTkFrame(master=root)
frame_questType.pack(padx=20, pady=20, fill="both", expand=True)

# Variable qui stocke la sélection oui/non
selected_option_Bad = ctk.StringVar()

# Cadre pour les boutons radio
cadre_boutons_Bad = ctk.CTkFrame(master=frame_questType)
cadre_boutons_Bad.pack(ipadx=10, pady=10)

# Label
label_bad = ctk.CTkLabel(master=cadre_boutons_Bad, text="Selon vous, qui est responsable de l'incident ?")
label_bad.pack(pady=10, padx=10)

# Fonction pour créer un radio button personnalisé avec la case à droite
def create_custom_radiobutton(master, text, variable, value):
    frame = ctk.CTkFrame(master=master, fg_color="transparent")
    label = ctk.CTkLabel(master=frame, text=text)
    label.pack(side="left")
    radio_button = ctk.CTkRadioButton(master=frame, text='' ,variable=variable, value=value)
    radio_button.pack(side="right")
    frame.pack(pady=10, padx=10)

# Radiobutton 1
create_custom_radiobutton(cadre_boutons_Bad, text="Utilisateur (Moi)", variable=selected_option_Bad, value="Utilisateur (Moi)")

# Radiobutton 2
create_custom_radiobutton(cadre_boutons_Bad, text="Système (Machine)", variable=selected_option_Bad, value="Système (Machine)")

# Lancer la boucle principale de l'application
root.mainloop()
