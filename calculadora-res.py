import tkinter as tk
from tkinter import ttk

class Calculadora(tk.Tk):
    def __init__(self):
        super().__init__()

        self.resultado_mostrado = tk.StringVar(self, value = "")

        display_text = tk.Label(self, font=("Arial", 18), justify = "right", textvariable = self.resultado_mostrado)
        display_text.grid(row = 0, column = 0, columnspan = 4)

        numbers_frame = NumberFrame(self)
        numbers_frame.grid(row = 1, column = 0, rowspan = 4, columnspan = 3)
        ops_frame = OperatorFrame(self)
        ops_frame.grid(row = 1, column = 3, rowspan = 4)

    def add_char(self, caracter):
        self.resultado_mostrado.set(self.resultado_mostrado.get() + caracter)

    def remove_content(self):
        self.resultado_mostrado.set("")

    def calculate_result(self):
        resultado = eval(self.resultado_mostrado.get())
        self.resultado_mostrado.set(resultado)

class NumberFrame(ttk.Frame):
    def __init__(self, master: Calculadora):
        super().__init__(master)
        lista_numeros = ['9','8','7','6','5','4','3','2','1','0','C','=']

        for i, num in enumerate(lista_numeros):
            if i < 10:
                def funcion_aux(n = num):
                    self.master.add_char(n)
                tk.Button(self, text = num, font =("Arial", 16), command = funcion_aux).grid(row = i//3, column = 2-i%3)
            elif num == 'C':
                tk.Button(self, text = num, font=("Arial", 16), command = self.master.remove_content).grid(row = i//3, column = 2-i%3)
            elif num == '=':
                tk.Button(self, text = num, font=("Arial", 16), command = self.master.calculate_result).grid(row = i//3, column = 2-i%3)


class OperatorFrame(ttk.Frame):
    def __init__(self, master: Calculadora):
        super().__init__(master)

        lista_operadores = ['+','-','*','/']

        for i, op in enumerate(lista_operadores):
            def funcion_aux(n = op):
                self.master.add_char(n)
            tk.Button(
                self,text = op, font=("Arial", 16), command = funcion_aux).grid(row = i)
            

app = Calculadora()
app.mainloop()