

#Likert

dic_stress= {
    0: "Sans stress",  # 11 caractères
    16: "Pas trop stressé(e)",  # 12 caractères
    33: "Légèrement stressé(e)",  # 20 caractères
    48.5: "Neutre",  # 6 caractères
    66: "Assez stressé(e)",  # 13 caractères
    83: "Très stressé(e)",  # 12 caractères
    100: "Extrêmement stressé(e)"
}

dic_hability_inf = {
    0: "Aucunes compétences",        # 19 caractères
    16: "Très peu compétent(e)",          # 18 caractères
    39: "Peu compétent(e)",        # 21 caractères
    53: "Moyen",          # 18 caractères
    66: "Compétent(e)",                   # 9 caractères
    83: "Très compétent(e)",              # 15 caractères
    100: "Extrêmement compétent(e)"       # 22 caractères
}

dic_passion = {
    0: "Pas du tout passionné(e)",        # 20 caractères
    16: "Très peu passionné(e)",          # 18 caractères
    33: "Peu passionné(e)",        # 21 caractères
    50: "Passion neutre",              # 14 caractères
    66: "Légèrement passionné(e)",                   # 9 caractères
    83: "Très passionné(e)",              # 15 caractères
    100: "Extrêmement passionné(e)"       # 22 caractères
}


dic_bruit = {
    0: "Pas du tout bruyant",          # 19 caractères
    16: "Très peu bruyant",            # 16 caractères
    33: "Légèrement bruyant",          # 20 caractères
    53.5: "Normal",                # 12 caractères
    66: "Assez bruyant",               # 13 caractères
    83: "Très bruyant",                # 12 caractères
    100: "Extrêmement bruyant"         # 21 caractères
}

dic_importance = {
    0: "Insignifiante",
    16: "Peu Importante",
    33: "Pas Très Importante",
    50: "Neutre",
    66: "Assez Importante",
    83: "Importante",
    100: "Très Importante"
}


dic_concentration = {
    0: "Très Faible",
    16: "Faible",
    33: "Plutôt Faible",
    # 50.1 : ' ',
    50: "Neutre",
    66: "Plutôt élevé",
    83: "Elevé",
    100: "Très élevé"}


dic_fatigue = {
    0: "Pas fatigué",
    16: "Très peu fatigué",
    33: "Peu fatigué",
    # 50.1 : ' ',
    50: "Neutre",
    66: "Plutôt fatigué",
    83: "Fatigué",
    100: "Vraiment fatigué"}

dico_text = {
    "stress" : "De manière générale, comment décrivez-vous votre état de stress",
    "bruit" : "Le niveau de bruit dans votre environnement de travail est : ",
    "passion" : "À quel point aimez-vous ce travail ?: ",
    "habilite_inf" : "À quel point êtes vous à l'aise avec les outils informatiques : ",

    "importance" : "Veuillez renseigner l'importance (la gravité) de l'incident négatif",
    "concentration" : "Sur une échelle de 1 à 7, comment évalueriez-vous votre niveau de concentration \n au moment où l'incident négatif a été commis ?",
    "fatigue" : "Sur une échelle de 1 à 7, à quel point vous sentiez-vous mentalement \n fatigué au moment de l'incident négatif ?"
    }

selected_var_importance = [dic_importance[50]]
selected_var_concentration = [dic_concentration[50]]
selected_var_fatigue = [dic_fatigue[50]]

selected_var_bruit = [dic_bruit[53.5]]
selected_var_passion = [dic_passion[50]]
selected_var_hability_inf = [dic_hability_inf[53]]
selected_var_stress = [dic_stress[48.5]]