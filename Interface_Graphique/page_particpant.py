import customtkinter as ctk

# Initialize the application
app = ctk.CTk()
app.geometry("800x600")
app.title("Information")


# Create the main frame
frame_info = ctk.CTkFrame(app)
frame_info.pack(pady=15, padx=30, fill="both", expand=True)

frame_info_texte = ctk.CTkFrame(frame_info, fg_color="#2b2b2b", border_width=2, border_color="#106a43")
frame_info_texte.pack(ipadx=20, ipady=20, pady=15, expand=True, anchor="center")

# Texts
texte_titre = "Information"
texte_p1 =("Bonjour, \n\nNous vous remercions d'avoir accepté de participer à cette étude. "
            "L'objectif de cette recherche est de collecter des données sur les potentiels d'erreur pendant votre séance de travail, "
            "afin de mieux comprendre leur fonctionnement et d'améliorer leur détection. À cette fin, vous avez été équipé d'un casque EEG, "
            "permettant de capter les signaux émis par votre cerveau. ")
texte_p2 = ("Durant les prochaines heures, votre rôle consistera à travailler comme d'habitude. "
            "Cependant, lorsque vous constatez un incident négatif (une erreur), il sera crucial de ne pas bouger pendant quelques secondes car tout mouvement "
            "pourrait introduire des artefacts moteurs c'est-à-dire des bruits parasites dans les signaux EEG causés par des mouvements physiques nuisant à la précision des données. "
            "Ensuite, utilisez cette application pour le signaler et, si vous avez le temps, le décrire en répondant au questionnaire qui s'affichera. "
            "Vous pourrez ensuite reprendre votre travail jusqu'au prochain incident négatif ou à la fin du temps de participation.")
texte_sTitre2 = "Informations supplémentaires :"
texte_liste = ("— Vous pourrez utiliser la fonction de signalement rapide, vous permettant de simplement signaler l'incident, puis de le compléter quand vous aurez le temps.\n"
               "— Vous pouvez signaler un incident négatif ultérieurement en indiquant approximativement le nombre de minutes écoulées depuis sa survenue.\n"
               "— Vous pouvez également modifier un incident négatif déjà signalé en consultant la section 'Récapitulatif'.\n"
               "— Vous avez la possibilité d'interrompre l'expérience à tout moment en appuyant sur le bouton 'Quitter et sauvegarder' en haut à gauche de la page principale.")
texte_thanks = "Votre participation est essentielle pour nous aider à mieux comprendre les erreurs de travail et à améliorer leur détection. \nMerci pour votre collaboration !"

# Fonts
font_titre = ("Helvetica", 30, "bold")
font_p1 = ("Helvetica", 20)
font_sTitre2 = ("Helvetica", 25)
font_liste = ("Helvetica", 20)
font_thanks = ("Helvetica", 18, "italic")

# Title
frame_titre = ctk.CTkFrame(frame_info_texte)
info_titre = ctk.CTkLabel(frame_titre, text=texte_titre, font=font_titre)
info_titre.pack()
frame_titre.pack(pady=20, ipady=5, ipadx=30, anchor="center")

# P1
frame_p1 = ctk.CTkFrame(frame_info_texte)
info_p1 = ctk.CTkLabel(frame_p1, text=texte_p1, font=font_p1, justify="left", wraplength=1200)
info_p1.pack()
frame_p1.pack(pady=10, ipady=5, ipadx=30, anchor="center")

# P2
frame_p2 = ctk.CTkFrame(frame_info_texte)
info_p2 = ctk.CTkLabel(frame_p2, text=texte_p2, font=font_p1, justify="left", wraplength=1200)
info_p2.pack()
frame_p2.pack(pady=10, ipady=5, ipadx=30, anchor="center")

# Additional Information Title
frame_sTitre2 = ctk.CTkFrame(frame_info_texte)
info_sTitre2 = ctk.CTkLabel(frame_sTitre2, text=texte_sTitre2, font=font_sTitre2)
info_sTitre2.pack()
frame_sTitre2.pack(pady=20, ipady=5, ipadx=30, anchor="center")

# List
frame_liste = ctk.CTkFrame(frame_info_texte)
info_liste = ctk.CTkLabel(frame_liste, text=texte_liste, font=font_liste, justify="left", wraplength=1200)
info_liste.pack()
frame_liste.pack(pady=20, ipady=5, ipadx=30, anchor="center")

# Thanks
frame_thanks = ctk.CTkFrame(frame_info_texte)
info_thanks = ctk.CTkLabel(frame_thanks, text=texte_thanks, font=font_thanks, justify="left", wraplength=1200)
info_thanks.pack()
frame_thanks.pack(pady=20, ipady=5, ipadx=30, anchor="center")

# Display the application
app.mainloop()
