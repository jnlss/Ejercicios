import tkinter as tk
from tkinter import ttk


class Calculadora(tk.Tk):
    def __init__(self):
        # Inicializamos tk.Tk() como se hace normalmente
        super().__init__()
        
        # Como alternativa a esto, se puede usar el "config" con display_text continuamente
        # De esta forma, lo que se guarde en esta variable actualiza automáticamente el Label
        self.resultado_mostrado = tk.StringVar(self, value="")
        # Creamos una entrada de texto para imprimir el resultado de la calculadora
        display_text = tk.Label(self, font=("Arial", 18), justify="right",
                                textvariable=self.resultado_mostrado)
        # El columnspan nos otorga 4 columnas de longitud
        display_text.grid(row=0, column=0, columnspan=4)
        
        # Frames de la calculadora
        self.numbers_frame = NumberFrame(self)
        self.numbers_frame.grid(row=1, column=0, rowspan=4, columnspan=3)
        self.ops_frame = OperatorFrame(self)
        self.ops_frame.grid(row=1, column=3, rowspan=4)
        self.historial_frame = Historial(self)
        
        self.historial_on = False
        
        # Botón de cambio de calculadora
        tk.Button(self, font=("Arial", 18), text="Cambiar", command=self.switch_historial).grid(row=5)
        
    # Función para cambiar al historial
    def switch_historial(self):
        if self.historial_on:
            self.historial_frame.grid_forget()
            self.numbers_frame.grid(row=1, column=0, rowspan=4, columnspan=3)
            self.ops_frame.grid(row=1, column=3, rowspan=4)
        else:
            self.numbers_frame.grid_forget()
            self.ops_frame.grid_forget()
            self.historial_frame.grid(row=1, column=0, rowspan=4, columnspan=4)
            
        self.historial_on = not self.historial_on
        
    # definimos una función que añade un caracter a la String
    def add_char(self, caracter):
        self.resultado_mostrado.set(self.resultado_mostrado.get() + caracter)
    
    # elimina todo el contenido
    def remove_content(self):
        self.resultado_mostrado.set("")
        
    # muestra el resultado final
    def calculate_result(self):
        # La función "eval" evalúa una función matemática en forma de string.
        # Si no, tendríamos que crear nosotros mismos esta lógica
        resultado = eval(self.resultado_mostrado.get())
        
        # Añadimos al historial el texto que corresponda
        self.historial_frame.texto_historial.set(
            self.historial_frame.texto_historial.get() +
            "\n" + self.resultado_mostrado.get() + "=" + str(resultado)
            )
        
        self.resultado_mostrado.set(resultado)
        

# Frame con los números      
class NumberFrame(ttk.Frame):
    def __init__(self, master: Calculadora):
        super().__init__(master)
        lista_números = ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0', 'C', '=']
        
        for i, num in enumerate(lista_números):
            # Caso de los dígitos
            if i < 10:
                def función_auxiliar(n=num):
                    self.master.add_char(n)
                tk.Button(
                    self,
                    text=num,
                    font=("Arial", 16),
                    command=función_auxiliar
                    ).grid(row=i//3, column=2-i%3)
            elif num == 'C':
                tk.Button(
                    self,
                    text=num,
                    font=("Arial", 16),
                    command=self.master.remove_content
                    ).grid(row=i//3, column=2-i%3)
            elif num == '=':
                tk.Button(
                    self,
                    text=num,
                    font=("Arial", 16),
                    command=self.master.calculate_result
                    ).grid(row=i//3, column=2-i%3)
                
class OperatorFrame(ttk.Frame):
    def __init__(self, master: Calculadora):
        super().__init__(master)
        
        lista_operadores = ['+', '-', '*', '/']
        
        for i, op in enumerate(lista_operadores):
            def función_auxiliar(n=op):
                self.master.add_char(n)
            tk.Button(
                self,
                text=op,
                font=("Arial", 16),
                command=función_auxiliar
                ).grid(row=i)
            
class Historial(ttk.Frame):
    def __init__(self, master: Calculadora):
        super().__init__(master)
        
        self.texto_historial = tk.StringVar()
        display_hist = ttk.Label(self, font=("Arial", 18),
                                textvariable=self.texto_historial)
        display_hist.grid(row=0)
        
            
app = Calculadora()
app.mainloop()