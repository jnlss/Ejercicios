import tkinter as tk
from tkinter import ttk

class PiramideFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.lista_labels = list()

    def crearPiramide(self, numRows):
        # Destruir piramide anterior
        for elem in self.lista_labels:
            elem.destroy()
        self.lista_labels = list()

        totalCols = 1 + (numRows - 1) * 2

        puntoMedio = totalCols // 2

        for row in range(numRows):
            for col in range(totalCols):
                if puntoMedio - row <= col <= puntoMedio + row:
                    letra = "x"
                else:
                    letra = " "
                new_label = ttk.Label(self, text = letra)
                self.lista_labels.append(new_label)

                new_label.grid(column = col, row = row)

    
class MainFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.title = ttk.Label(self, text = "Creador de piramides", font = 50)
        self.title.grid(row = 0)

        self.textNumber = ttk.Label(self, text = "Introduce el numero de pisos:", font = 50)
        self.textNumber.grid(row = 1, column = 0)
        self.entryNumber = ttk.Entry(self)
        self.entryNumber.grid(row = 1, column = 1)

        self.piramide = PiramideFrame(self)
        self.piramide.grid(row = 3)

        self.button = ttk.Button(self, text = "Calcular", command = self.refresh_piramide)
        self.button.grid(row = 2)

        self.pack()

    def refresh_piramide(self):
        self.piramide.crearPiramide(int(self.entryNumber.get()))


class App:
    def __init__(self, master):
        self.master = master
        self.master.geometry("600x500")
        self.master.resizable(True, True)

        self.mainFrame = MainFrame(self.master)


if __name__ == '__main__':
    root = tk.Tk()
    App(root)
    root.mainloop()