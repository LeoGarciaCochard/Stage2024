import customtkinter as ctk
from screeninfo import get_monitors
from dataclasses import dataclass, field

from Interface_Graphique.pages.acceuil import PageAcceuil


@dataclass
class Interface:
    width: int = 800
    height: int = 600
    fullscreen: bool = field(default=False, init=False)
    root: ctk.CTk = field(default=None, init=False)
    screen_width: int = field(init=False)

    def __post_init__(self):
        self.screen_width = get_monitors()[0].width
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.root = ctk.CTk()
        self.root.geometry(f'{self.width}x{self.height}')
        self.root.title("Interface Graphique ErrP")

        self.root.bind("<F11>", lambda x: self.toggle_fullscreen())
        self.root.bind("<Escape>", lambda x: self.end_fullscreen())
        self.toggle_fullscreen()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        return "break"

    def end_fullscreen(self):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)
        return "break"

    def run(self):
        self.root.mainloop()

from Interface_Graphique.pages.principal import PagePrincipale

if __name__ == '__main__':
    app = Interface()

    page_acceuil = PageAcceuil(app.root)
    page_acceuil.afficher_page_acceuil()
    # page_principale = PagePrincipale(app.root)
    # page_principale.afficher()

    app.run()
