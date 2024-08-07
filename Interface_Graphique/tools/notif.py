from dataclasses import dataclass, field
import customtkinter as ctk


@dataclass
class NotificationWindow:
    notif: ctk.CTk = field(init=False, default_factory=ctk.CTk)

    def __post_init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.notif.geometry("420x100")
        self.notif.title("IMPORTANT")

        self.setup_widgets()

    def setup_widgets(self):

        label = ctk.CTkLabel(self.notif, text="  Tous les incidents n'ont pas été renseignés correctement  ")
        label.pack(pady=10, ipadx=5)
        label.configure(fg_color="#2b2b2b", font=("Helvetica", 15))

        button_frame = ctk.CTkFrame(self.notif, fg_color="#242424")
        button_frame.pack(pady=(5, 15))

        close_button = ctk.CTkButton(button_frame, text="Fermer quand même", command=self.arret_force)
        close_button.grid(row=0, column=0, padx=10)

        complete_button = ctk.CTkButton(button_frame, text="Compléter les renseignements", command=self.retourner)
        complete_button.grid(row=0, column=1, padx=10)

    def arret_force(self):
        """Enregistre le rec, ferme app et notif"""
        # arreterRecEEG()
        root.destroy()
        self.notif.destroy()

    def retourner(self):
        """Ferme la notif et ouvre le menu recap"""
        vers_frame_tab_err()
        self.notif.destroy()

    def run(self):
        self.notif.mainloop()


notif_window = NotificationWindow()
notif_window.run()
