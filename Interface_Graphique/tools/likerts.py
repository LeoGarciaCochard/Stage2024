import customtkinter as ctk
from dataclasses import dataclass, field
from typing import List, Dict

from Interface_Graphique.var_fonc.variables_likert import *

@dataclass
class LikertLabel:
    master_frame: ctk.CTkFrame
    dic: Dict[int, str]
    text : str
    px: int = 10
    py: int = 10
    ipx: int = 10
    ipy: int = 10
    police: int = 15
    couleur: List[str] = field(default_factory=lambda: ["green", "green", "green", "white", "red", "red", "red"])

    def __post_init__(self):
        pass

    def grid_labels(self):
        label = ctk.CTkLabel(self.master_frame,text=self.text, font=("Helvetica", self.police))
        label.grid(row=0,column=0,columnspan=7, padx=self.px, pady=self.py)
        valeurs = list(self.dic.values())
        for i in range(len(valeurs)):
            label = ctk.CTkLabel(master=self.master_frame, text=valeurs[i], font=("Helvetica", 13), text_color=self.couleur[i])
            label.grid(row=1, column=i, padx=self.px)

        self.master_frame.pack()

@dataclass
class LikertSlider:
    master_frame: ctk.CTkFrame
    selected_var: List[str]
    dic: Dict[int, str]
    width: int = 700

    slider = None

    def __post_init__(self):
        self.liste = list(self.dic.keys())


    def magnet_likert(self, valeur_actuelle):
        """Magnetise la valeur à la plus proche sur l'echelle de likert """
        nouvelle_val = min(self.liste, key=lambda val: abs(val - valeur_actuelle))
        self.slider.set(nouvelle_val)
        self.selected_var[0] = self.dic[nouvelle_val]

    def pack_slider(self):
        self.slider = ctk.CTkSlider(master=self.master_frame, from_=0, to=100, width=self.width, command=self.magnet_likert)
        self.slider.grid(row=2, column=0, columnspan=7, pady = (0,10))
        self.slider.set(self.liste[3]+0.1)
        self.master_frame.pack()


@dataclass
class Likert() :
    master : ctk.CTkFrame
    dic : Dict[int,str]
    var : List[int]
    text :str

    bg : str = "#333333"
    px: int = 10
    py: int = 10
    ipx: int = 10
    ipy: int = 10
    sliderwidth : int | float = 700
    police: int = 15
    expand: bool = True

    def __post_init__(self):
        self.create_likert()

    def create_likert(self):
        self.cadre = ctk.CTkFrame(master = self.master, fg_color= self.bg)
        self.labels = LikertLabel(self.cadre, self.dic, text=self.text, police=self.police)
        self.slider =LikertSlider(self.cadre, self.var, self.dic, width=self.sliderwidth)

    def afficher(self):
        self.cadre.pack(ipadx=self.ipx, ipady=self.ipy, padx=self.px, pady=self.py, anchor='center',expand=self.expand)
        self.slider.pack_slider()
        self.labels.grid_labels()




# if __name__ == '__main__':
#
#     ctk.set_appearance_mode("dark")
#     ctk.set_default_color_theme("green")
#
#     root = ctk.CTk()
#     root.geometry("1080x800")
#     root.title("Interface Graphique ErrP")
#
#
#
#     likert_importance = Likert(root,dic_importance,selected_var_importance,text= dico_text["importance"], Sliderwidth=600 )
#     likert_concentration = Likert(root,dic_concentration,selected_var_concentration, text= dico_text["concentration"], Sliderwidth=425)
#     likert_fatigue = Likert(root,dic_fatigue,selected_var_fatigue, text= dico_text["fatigue"], Sliderwidth=500)
#
#
#     likert_bruit = Likert(root,dic_bruit,selected_var_bruit, text= dico_text["bruit"], Sliderwidth=653.5)
#     likert_passion = Likert(root,dic_passion,selected_var_passion, text= dico_text["passion"], Sliderwidth=800)
#     likert_hability_inf = Likert(root,dic_hability_inf,selected_var_hability_inf, text= dico_text["habilite_inf"], Sliderwidth=600)
#     likert_stress = Likert(root,dic_stress,selected_var_stress, text= dico_text["stress"])
#
#
#     root.mainloop()

