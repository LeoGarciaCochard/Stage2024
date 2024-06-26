import customtkinter as ctk
from PIL import Image, ImageTk

path_img_btn = "../Sources/btn.png"

# Initialisation de l'application principale
root = ctk.CTk()
root.title("Exemple de Bouton Rond")
root.geometry("400x300")

# Initialisation de customtkinter
ctk.set_appearance_mode("System")  # Options: "System" (par défaut), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue" (par défaut), "green", "dark-blue"

# Charger et redimensionner l'image
image_btn = Image.open(path_img_btn)
image_btn_resized = image_btn.resize((50, 50), Image.LANCZOS)
photo_btn = ctk.CTkImage(light_image=image_btn_resized, dark_image=image_btn_resized, size=(50, 50))

# Fonction pour gérer le clic sur le bouton rond
def on_round_button_click():
    print("Bouton rond cliqué !")

# Cadre pour le bouton
frame_button = ctk.CTkFrame(master=root)
frame_button.pack(pady=20)

# Création d'un bouton avec l'image redimensionnée
label_image_btn = ctk.CTkButton(master=frame_button, image=photo_btn, text="Ajout rapide", command=on_round_button_click, width=100, height=100, compound='top')
label_image_btn.pack(pady=20)

# Lancer la boucle principale de l'application
root.mainloop()
