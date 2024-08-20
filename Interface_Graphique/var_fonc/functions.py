import os
import sys
def resource_path(relative_path):
    """ On crée un path absolut depuis le relatif """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    new_path = os.path.join(base_path, relative_path)

    return new_path.replace("\\", "/")


def passer(page_actuelle, page_suivante):
    """ On cache la page actuelle et on affiche la suivante """
    page_actuelle.cacher()
    page_suivante.afficher()


def passer_definitif(page_actuelle, page_suivante):
    """ On détruit la page actuelle et on affiche la suivante """
    page_actuelle.destroy()
    page_suivante.afficher()



def tout_complet() :
    """ Vérifie si toutes les informations sont complétées """
    return False

def stimulation(n) :
    """ Fonction de stimulation """
    pass
