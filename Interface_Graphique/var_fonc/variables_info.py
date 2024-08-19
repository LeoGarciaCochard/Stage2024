from Interface_Graphique.var_fonc.functions import resource_path
import pandas as pd

def actualise_taches() :
    df_taches = pd.read_excel(resource_path("../Sources/taches.xlsx"))
    global taches
    taches =list(df_taches['Tâches'])

def actualise_instance_tache(instance) :
    """ On actualise l'instance de la combobox de BarreTache à tâche """
    instance.combobox_tache.combobox.set(dic_informations['selected_var_tache'])


taches = []

dic_informations = {'n_anonymat' : None, 'selected_var_tache' : None}





actualise_taches()