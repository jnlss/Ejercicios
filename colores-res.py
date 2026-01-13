import tkinter as tk
import random


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cambio de color mediante eventos")
        self.geometry("300x200")

        self.label = tk.Label(self, text="¡Hola, mundo!", font = ("Arial", 20))

        self.label.pack(pady = 30)

        self.boton = tk.Button(self, text="Cambiar color", command = self.generar_evento)
        self.boton.pack()

        self.bind("<<CambiarColor>>", self.cambiar_color)

    def generar_evento(self):
        self.event_generate("<<CambiarColor>>")
        
    def cambiar_color(self, event):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        color_hex = f"#{r:0x}{g:02x}{b:02x}"

        self.label.config(fg = color_hex)

if __name__ == "__main__":
    app = App()
    app.mainloop()