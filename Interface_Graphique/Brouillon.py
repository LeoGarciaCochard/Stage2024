import customtkinter as ctk

class Page1(ctk.CTkFrame):
    def __init__(self, master, switch_page_callback):
        super().__init__(master)
        self.label = ctk.CTkLabel(self, text="Page 1")
        self.label.pack(pady=20)

        self.button = ctk.CTkButton(self, text="Go to Page 2", command=switch_page_callback)
        self.button.pack(pady=20)


class Page2(ctk.CTkFrame):
    def __init__(self, master, switch_page_callback):
        super().__init__(master)
        self.label = ctk.CTkLabel(self, text="Page 2")
        self.label.pack(pady=20)

        self.button = ctk.CTkButton(self, text="Go to Page 1", command=switch_page_callback)
        self.button.pack(pady=20)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CustomTkinter App")
        self.geometry("400x300")

        self.page1 = Page1(self, self.show_page2)
        self.page2 = Page2(self, self.show_page1)

        self.page1.pack(fill="both", expand=True)

    def show_page1(self):
        self.page2.pack_forget()
        self.page1.pack(fill="both", expand=True)

    def show_page2(self):
        self.page1.pack_forget()
        self.page2.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
