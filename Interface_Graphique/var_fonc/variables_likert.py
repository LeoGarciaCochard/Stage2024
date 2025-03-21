

#Likert

dic_stress= {
    0: "Aucun stress",
    16: "Très peu stressé(e)",
    33: "Peu stressé(e)",
    48.5: "Modérément",
    66: "Plutôt stressé(e)",
    83: "Très stressé(e)",
    100: "Extrêmement stressé(e)"
}

dic_aisance_informatique = {
    0: "Pas dutout à l'aise",
    16: "Très peu à l’aise",
    39: "Peu à l’aise",
    53: "Moyennement",
    66: "Plutôt à l’aise",
    83: "Très à l’aise",
    100: "Extrêmement à l’aise"
}

dic_passion = {
    0: "Pas du tout motivé(e)",
    16: "Très peu motivé(e)",
    33: "Peu motivé(e)",
    50: "Motivation neutre",
    66: "Légèrement motivé(e)",
    83: "Très motivé(e)",
    100: "Extrêmement motivé(e)"
}


dic_bruit = {
    0: "Pas du tout bruyant",
    16: "Très peu bruyant",
    33: "Légèrement bruyant",
    53.5: "Normal",
    66: "Assez bruyant",
    83: "Très bruyant",
    100: "Extrêmement bruyant"
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
    "passion" : "Quelle est votre niveau de motivation pour ce travail ? ",
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
selected_var_hability_inf = [dic_aisance_informatique[53]]
selected_var_stress = [dic_stress[48.5]]