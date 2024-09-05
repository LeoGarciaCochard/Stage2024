import tkinter as tk
from dataclasses import dataclass
from typing import List

import customtkinter as ctk

from Interface_Graphique.tools.buttons import Button
from Interface_Graphique.tools.comboboxes import Combobox
from Interface_Graphique.tools.entries import Entry
from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.tools.labels import Label
from Interface_Graphique.tools.radiobuttons import RadioButton
from Interface_Graphique.tools.textboxes import TextBox
from Interface_Graphique.tools.tooltips import Tooltip


@dataclass(kw_only=True)
class Format:
    master: ctk.CTk | ctk.CTkFrame
    text: str

    fill: str | None = None
    expand: bool = False
    px: int | tuple[int, int] = 10
    py: int | tuple[int, int] = 10
    ipx: int | tuple[int, int] = 0
    ipy: int | tuple[int, int] = 0
    border_width: int = 0
    corner_radius: int = 5
    border_color: str = "#106a43"
    fg_color: str = "#333333"
    anchor: str = 'center'

    row: int = 0
    column: int = 0
    columnspan: int = 1

    police: int = 15
    font: str = 'Helvetica'
    style: str = "normal"
    text_bg: str = "#333333"
    text_px: int | tuple[int, int] = 10
    text_py: int | tuple[int, int] = 5
    text_ipx: int | tuple[int, int] = 0
    text_ipy: int | tuple[int, int] = 0

    text_row: int = 0
    text_column: int = 0
    text_columnspan: int = 1

    cadre = None

    def __post_init__(self):
        pass

    def create_cadre(self):
        self.cadre = Frame(master=self.master, border_width=self.border_width, corner_radius=self.corner_radius,
                           border_color=self.border_color, fg_color=self.fg_color, px=self.px, py=self.py,
                           ipx=self.ipx, ipy=self.ipy, fill=self.fill, expand=self.expand, anchor=self.anchor,
                           row=self.row, column=self.column, columnspan=self.columnspan)

    def afficher(self):
        self.cadre.afficher()

    def cacher(self):
        self.cadre.cacher()

    def fixer(self):
        self.cadre.fixer()

@dataclass(kw_only=True)
class FormatTitre(Format):

    fg_color: str = "#242424"
    style: str = "bold"
    text_bg: str = "#242424"

    label_titre = None

    def __post_init__(self):
        super().__post_init__()
        self.create_cadre()
        self.create_titre()
        self.label_titre.afficher()

    def create_titre(self):

        self.label_titre = Label(text=self.text, master=self.cadre.frame, police=self.police, style=self.style,
                           bg=self.text_bg, px=self.text_px, py=self.text_py, ipx=self.text_ipx, ipy=self.text_ipy,
                           row=self.text_row, column=self.text_column, columnspan=self.text_columnspan)


@dataclass(kw_only=True)
class FormatQuestionCombobox(Format):
    variable: str # clef str de la variable dans dic_informations
    values: List[str]

    text_column: int = 0
    text_columnspan: int = 1
    text_row: int = 0

    box_state: str = "readonly"

    box_width: int = 200
    box_height: int = 30
    box_px: int | tuple[int, int] = 10
    box_py: int | tuple[int, int] = 10
    box_ipx: int | tuple[int, int] = 0
    box_ipy: int | tuple[int, int] = 0
    box_side: str = tk.TOP

    box_column: int = 1
    box_columnspan: int = 1
    box_row: int = 0

    label_question = None
    combobox = None

    def __post_init__(self):
        super().__post_init__()

        self.create_cadre()
        self.create_question_combobox()
        self.label_question.fixer()
        self.combobox.fixer()

    def create_question_combobox(self):

        self.label_question = Label(text=self.text, master=self.cadre.frame, police=self.police,
                                    style=self.style, bg=self.text_bg, px=self.text_px, py=self.text_py,
                                    ipx=self.text_ipx, ipy=self.text_ipy,
                                    row=self.text_row, column=self.text_column, columnspan=self.text_columnspan)

        self.combobox = Combobox(master=self.cadre.frame, values=self.values,
                                 variable_name=self.variable, state=self.box_state,
                                 width=self.box_width, height=self.box_height,
                                 px=self.box_px, py=self.box_py, ipx=self.box_ipx, ipy=self.box_ipy, side=self.box_side,
                                 row=self.box_row, column=self.box_column,columnspan=self.box_columnspan)



@dataclass(kw_only=True)
class FormatChoix2RadioBox(Format):
    choix1: str
    choix2: str
    variable: tk.StringVar

    box_choix_1 = None
    box_choix_2 = None
    question = None
    label_choix1 = None


    def __post_init__(self):
        self.create_cadre()
        self.create_radio_boxes()

    def create_radio_boxes(self):

        self.question = FormatTitre(master=self.cadre.frame, text=self.text, police=15, style="normal")

        self.cadre_buttons = Frame(master=self.cadre.frame, border_width=0, py=0, fg_color=self.fg_color)

        self.label_choix1 = Label(master=self.cadre_buttons.frame, text=self.choix1, police=15, style="normal", cursor="hand2",
                                  py=10, px=10, side="right")

        self.label_choix1.label.bind("<Button-1>", lambda e: self.variable.set(self.choix1))

        self.box_choix_1 = RadioButton(master=self.cadre_buttons.frame, text='', variable=self.variable, value=self.choix1,
                                       police=self.police, font=self.font, style=self.style,
                                       py=10, px=10, side="right")

        self.box_choix_2 = RadioButton(master=self.cadre_buttons.frame, text=self.choix2, variable=self.variable,
                                       value=self.choix2, police=self.police, font=self.font, style=self.style,
                                       py=10, px=10, side="right")

        self.question.afficher()
        self.cadre_buttons.afficher()
        self.box_choix_2.afficher()
        self.box_choix_1.afficher()
        self.label_choix1.afficher()

@dataclass(kw_only=True)
class FormatChoix2RadioBoxDeroulement(FormatChoix2RadioBox):
    text_deroulement: str
    placeholder_deroulement: str

    height_entry_deroulement: int = 5

    def __post_init__(self):
        self.create_cadre()
        self.create_radio_boxes()
        self.variable.trace_add("write", self.check_selection)

    def check_selection(self, *args):
        if self.variable.get() == self.choix1:
            self.create_deroulement()
        else:
            self.destroy_deroulement()

    def create_deroulement(self):
        self.cadre_deroulement = Frame(master=self.cadre.frame, border_width=0, py=0, fg_color=self.fg_color)

        self.question = FormatTitre(master=self.cadre_deroulement.frame, text=self.text_deroulement,
                                    police=13, style="normal")

        self.entry_deroulement = Entry(master=self.cadre_deroulement.frame,placeholder=self.placeholder_deroulement,
                                       px=10, py=0, ipx=10, ipy=10, height=self.height_entry_deroulement, police=13)

        self.cadre_deroulement.afficher()
        self.question.afficher()
        self.entry_deroulement.afficher()

    def get_entry_deroulement(self):
        if self.variable.get() == self.choix1:
            return self.entry_deroulement.entry.get()
        else:
            return "Pas de distraction"

    def destroy_deroulement(self):
        try:
            self.cadre_deroulement.destroy()
        except AttributeError:
            pass

    def set(self, choix, valeur):
        self.destroy_deroulement()
        self.variable.set(choix)
        if choix == self.choix1:
            try :
                self.entry_deroulement.entry.delete("0", "end")
            except Exception as e:
                pass
            self.entry_deroulement.entry.insert(tk.END, valeur)

@dataclass(kw_only=True)
class FormatRadiosButtons(Format):
    choix: List[str]
    variable: tk.StringVar

    box = None
    question = None
    cadre_buttons = None

    def __post_init__(self):
        self.create_cadre()
        self.create_radio_buttons()

    def create_radio_buttons(self):

        self.question = FormatTitre(master=self.cadre.frame, text=self.text, police=15, style="normal")

        self.cadre_buttons = Frame(master=self.cadre.frame, border_width=0, py=0, fg_color=self.fg_color)

        self.question.afficher()
        self.cadre_buttons.afficher()

        for option in self.choix :

            self.box = RadioButton(master=self.cadre_buttons.frame, text=option, variable=self.variable, value=option,
                                   police=self.police, font=self.font, style=self.style,
                                   py=10, px=10, side="left")
            self.box.afficher()

    def destroy(self):
        self.cadre.destroy()
        self.variable.set("")


@dataclass(kw_only=True)
class FormatGridButtons(Format):
    options: List[str]
    descriptions: List[str]
    exemples: List[str]

    def __post_init__(self):
        self.create_cadre()
        self.create_grid_buttons()

    def create_grid_buttons(self):
        self.question = FormatTitre(master=self.cadre.frame, text=self.text, police=15, style="normal")
        self.question.afficher()

        self.cadre_buttons = Frame(master=self.cadre.frame, border_width=0, py=0, fg_color=self.fg_color)
        self.cadre_buttons.afficher()

        i = 0
        j = 0
        self.dic_button_states = {}

        for n in range(len(self.options)) :

            button = Button(master=self.cadre_buttons.frame, text=self.options[n],
                            row=j, column=i, py=5, px=5, fg_color="#2FA572",function=lambda: None)
            button.fixer()

            text_tooltip = f"{self.descriptions[n]}\nExemple : {self.exemples[n]}"
            Tooltip(button.button, text_tooltip)

            self.dic_button_states[self.options[n]] = False

            button.button.bind("<Button-1>", lambda e,
                                                    btn = button, opt=self.options[n]: self.toggle_button(button=btn,
                                                                                                          option=opt))

            # Faire des rangées de 3 boutons
            if i + 1 == 3:
                i = 0
                j += 1
            else:
                i += 1


    def toggle_button(self,button,option):

        if self.dic_button_states[option]:
            button.button.configure(fg_color="#2FA572")
            self.dic_button_states[option] = False

        elif any(self.dic_button_states.values()) :
            pass

        else:
            button.button.configure(fg_color="#106A43")
            self.dic_button_states[option] = True

    def get_selected(self):
        if any(self.dic_button_states.values()) :
            rep = [key for key, value in self.dic_button_states.items() if value]
        else :
            rep = None

        return rep

    def set(self, selected_option):

        #On détruit les boutons déjà présents
        self.cadre_buttons.destroy()

        #On le reconstruis en selectionnant l'option choisie

        self.cadre_buttons = Frame(master=self.cadre.frame, border_width=0, py=0, fg_color=self.fg_color)
        self.cadre_buttons.afficher()

        i = 0
        j = 0
        self.dic_button_states = {}

        for n in range(len(self.options)):

            button = Button(master=self.cadre_buttons.frame, text=self.options[n],
                            row=j, column=i, py=5, px=5, fg_color="#2FA572", function=lambda: None)
            button.fixer()

            text_tooltip = f"{self.descriptions[n]}\nExemple : {self.exemples[n]}"
            Tooltip(button.button, text_tooltip)

            self.dic_button_states[self.options[n]] = False

            button.button.bind("<Button-1>", lambda e,
                                                    btn=button, opt=self.options[n]: self.toggle_button(button=btn,
                                                                                                        option=opt))
            if self.options[n] == selected_option:
                self.toggle_button(button, self.options[n])

            # Faire des rangées de 3 boutons
            if i + 1 == 3:
                i = 0
                j += 1
            else:
                i += 1


@dataclass(kw_only=True)
class FormatTextBox(Format):
    placeholder: str

    textbox_height: int = 100
    textbox_width: int = 400

    titre = None
    text_box = None


    def __post_init__(self):
        self.create_cadre()
        self.create_text_box()

    def create_text_box(self):

        self.titre = FormatTitre(master=self.cadre.frame, text=self.text, police=15, style="normal")
        self.titre.afficher()

        self.text_box = TextBox(master=self.cadre.frame, placeholder=self.placeholder, height=self.textbox_height,
                                width=self.textbox_width, px=10, py=5, ipx=0, ipy=0)
        self.text_box.afficher()

    def get_text(self):
        return self.text_box.get_text()

    def set(self, text):
        self.text_box.remove_placeholder()
        self.text_box.textbox.insert("1.0", text)
