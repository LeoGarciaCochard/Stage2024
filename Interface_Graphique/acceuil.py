import customtkinter as ctk
from screeninfo import get_monitors
from tools.frames import *
from tools.buttons import *
from tools.labels import *


# Stocker la largeur et la hauteur de l'écran dans des variables
screen_width = get_monitors()[0].width
width = 800                        #Taille de la fenêtre
height = 600                       #Taille de la fenêtre


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



if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

#Root
    root = ctk.CTk()
    root.geometry(str(width) + 'x' + str(height))
    root.title("Interface Graphique ErrP")

#Fullscreen
    fullscreen = False
    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Escape>", end_fullscreen)
    toggle_fullscreen()

#Frame page d'acceuil
    page_acceuil = Frame(root,border_width=3, expand=True,fill="both",px=20,py=20)
    page_acceuil.afficher()

# Bouton quitter
    bouton_quitter = ButtonQuitter(master=page_acceuil.frame, only_destroy=True, root=root)

#Titre
    cadre_titre = Frame(page_acceuil.frame, border_width= 3, corner_radius= 100, expand=True)
    cadre_titre.afficher()
    label_titre = Label(text="Options de lancement :", master=cadre_titre.frame, police=40, style="bold")
    label_titre.afficher()

#Cadre

    def nouveau():
        page_acceuil.destroy()


    def existant():
        print("existant")

    cadre_boutons = Frame(page_acceuil.frame)
    cadre_boutons.afficher()

    bouton_nouveau_participant = Button(master=cadre_boutons,text="Générer un numéro d'anonymat", function = nouveau )
    bouton_participant_existant = Button(master=cadre_boutons,text="Utiliser un numéro existant",function= existant )
    bouton_nouveau_participant.afficher()
    bouton_participant_existant.afficher()


    root.mainloop()