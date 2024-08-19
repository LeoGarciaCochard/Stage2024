from Interface_Graphique.var_fonc.functions import resource_path
import pandas as pd

def actualise_taches() :
    df_taches = pd.read_excel(resource_path("../Sources/taches.xlsx"))
    global taches
    taches =list(df_taches['Tâches'])


taches = []


n_anonymat = []

dic_selected_var = {'selected_var_tache' : None}





actualise_taches()