import tkinter as tk
import customtkinter as ctk

class CadreTableauScrollable:
    def __init__(self, master, bg_color="#333333", width=None, height=None):
        # Créer le cadre principal qui contiendra tout
        self.container_frame2 = ctk.CTkFrame(master=master, width=width, height=height)
        self.container_frame2.pack(pady=10, padx=25, fill="both", expand=True)
        self.container_frame2.configure(fg_color=bg_color)

        # Créer un cadre pour contenir le canvas et les scrollbars
        self.container_frame = ctk.CTkFrame(master=self.container_frame2)
        self.container_frame.pack(pady=10, padx=25, fill="both", expand=True)
        self.container_frame.configure(fg_color=bg_color)

        # Créer un canvas pour le contenu défilant avec la même couleur de fond
        self.canvas = tk.Canvas(self.container_frame, bg=bg_color, bd=0, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill="both", expand=True)

        # Ajouter une barre de défilement verticale
        self.scrollbar_v = ctk.CTkScrollbar(self.container_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)

        # Ajouter une barre de défilement horizontale
        self.scrollbar_h = ctk.CTkScrollbar(self.container_frame2, orientation="horizontal", command=self.canvas.xview)
        self.scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)

        # Lier les scrollbars au canvas
        self.canvas.configure(yscrollcommand=self.scrollbar_v.set, xscrollcommand=self.scrollbar_h.set)

        # Créer un cadre pour le contenu à l'intérieur du canvas
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color=bg_color)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Lier l'événement de redimensionnement pour ajuster la zone scrollable
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event=None):
        """Met à jour la région scrollable du canvas pour s'adapter au contenu."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def get_frame(self):
        """Retourne le cadre défilable pour y ajouter des widgets."""
        return self.scrollable_frame

    def pack(self, **kwargs):
        """Permet de packer le cadre principal."""
        self.container_frame2.pack(**kwargs)

    def grid(self, **kwargs):
        """Permet de grider le cadre principal."""
        self.container_frame2.grid(**kwargs)

    def place(self, **kwargs):
        """Permet de placer le cadre principal."""
        self.container_frame2.place(**kwargs)


