import customtkinter as ctk
import tkinter as tk

# Initialisation de l'application principale
app = ctk.CTk()

# Définir les dimensions de la fenêtre principale
app.geometry("400x300")
app.title("Fenêtre Principale")


# Fonction pour afficher la pop-up
def show_popup(event):
    # Obtenir les coordonnées du curseur de la souris
    x = event.x_root
    y = event.y_root

    # Création de la fenêtre pop-up
    popup = ctk.CTkToplevel(app)
    popup.geometry(f"200x150+{x}+{y}")
    popup.title("Pop-up Verte")

    # Définir le fond vert
    popup.configure(bg='green')

    # Ajouter un label dans la pop-up
    label = ctk.CTkLabel(popup, text="Ceci est une pop-up verte!", fg_color="white", bg_color="green")
    label.pack(pady=20)

    # Bouton pour fermer la pop-up
    close_button = ctk.CTkButton(popup, text="Fermer", command=popup.destroy)
    close_button.pack(pady=10)

    # Mettre la fenêtre pop-up au premier plan
    popup.lift()
    popup.grab_set()
    popup.focus_force()


# Ajouter un bouton dans la fenêtre principale pour afficher la pop-up
button = ctk.CTkButton(app, text="Afficher Pop-up")
button.pack(pady=20)
# Lier le clic du bouton à la fonction show_popup
button.bind("<Button-1>", show_popup)

# Lancer l'application
app.mainloop()
