import tkinter as tk
from tkinter import ttk

class MainApp(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.pack()
        self.form = Formulario(self)
        self.results = Resultados(self)
        
        # Ubicamos primero el formulario
        self.form.pack()


class Formulario(tk.Frame):
    def limpiar_formulario(self):
        # El 0 indica que se borra desde la primeraz posición
        self.nameEntry.delete(0, 'end')
        self.edad_spinbox.set("")
        self.genero_combo.set("Masculino")
        self.pais_combo.set("España")
        
    def mostrar_resultados(self):
        results_frame = self.master.results
        nuevo_texto = f"""
📋 DATOS REGISTRADOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 Información Personal:
   • Nombre: {self.nameEntry.get()}
   • Edad: {self.edad_spinbox.get()} años
   • Género: {self.genero_combo.get()}
   • País: {self.pais_combo.get()}
        """
        results_frame.resultado_label.config(text=nuevo_texto)
        # Hacemos que se visualice el otro Frame
        self.pack_forget()
        results_frame.pack()
    
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        
        self.nameLabel = ttk.Label(self, text="Inserta tu nombre:", font=50)
        self.nameEntry = ttk.Entry(self, font=50)
        self.nameLabel.grid(row=0, column=0)
        self.nameEntry.grid(row=0, column=1)

        ttk.Label(self, text="Edad:").grid(row=2, column=0)
        self.edad_spinbox = ttk.Spinbox(self, width=10)
        self.edad_spinbox.grid(row=2, column=1)
        
        ttk.Label(self, text="Género:").grid(row=3, column=0)
        self.genero_combo = ttk.Combobox(self, 
                                   values=["Masculino", "Femenino", "Otro", "Prefiero no decir"],
                                   state="readonly")
        self.genero_combo.grid(row=3, column=1)
        self.genero_combo.set("Masculino")  # Valor por defecto
        
        ttk.Label(self, text="País:").grid(row=4, column=0)
        paises = ["España", "México", "Argentina", "Colombia", "Chile", "Perú", "Venezuela", "Ecuador"]
        self.pais_combo = ttk.Combobox(self, 
                                 values=paises, state="readonly")
        self.pais_combo.grid(row=4, column=1)
        self.pais_combo.set("España")  # Valor por defecto
        
        self.showButton = ttk.Button(self, text="Mostrar Resultado", command=self.mostrar_resultados)
        # La función destroy cierra el Frame
        # Como lo que queremos es que se cierre la aplicación, tenemos que llamar al destroy de root
        self.cleanButton = ttk.Button(self, text="Limpiar Formulario", command=self.limpiar_formulario)
        
        self.showButton.grid(row=5, column=0)
        self.cleanButton.grid(row=5, column=1)


class Resultados(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title_label = ttk.Label(self, text="Información Registrada", 
                                             padding="20")
        self.title_label.pack()
        
        # Label para mostrar que no hay datos
        self.resultado_label = ttk.Label(self, 
                                       text="No hay datos para mostrar.\nCompleta el formulario y haz clic en 'Enviar Datos'.",
                                       font=("Arial", 12), justify="center")
        self.resultado_label.pack(expand=True)
        
        # Botón para volver
        ttk.Button(self, text="Volver", command=self.volver).pack()
        # Botón para limpiar resultados
        ttk.Button(self, text="Limpiar Resultados", 
                  command=self.limpiar_resultados).pack()
        
    def limpiar_resultados(self):
        self.resultado_label.config(text="No hay datos para mostrar.\nCompleta el formulario y haz clic en 'Enviar Datos'.")
    
    # Nueva función: cambio de frame
    def volver(self):
        self.pack_forget()
        self.master.form.pack()


root = tk.Tk()
app = MainApp(root)
root.mainloop()