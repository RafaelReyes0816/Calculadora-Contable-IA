import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import numpy as np
from datetime import datetime
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# DATASET Y ENTRENAMIENTO DEL MODELO IA
import joblib
import os
import sys

# CARGA DEL MODELO IA PRE-ENTRENADO
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(BASE_DIR, 'modelo_ia.pkl')
METRICS_FILE = os.path.join(BASE_DIR, 'metricas_ia.pkl')

if not os.path.exists(MODEL_FILE) or not os.path.exists(METRICS_FILE):
    import tkinter.messagebox as messagebox
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('Error', 'No se encontró el modelo de la Inteligencia Artificial.\\nPor favor, ejecute primero el archivo "entrenador_ia.py" para que el programa pueda estudiar el Excel.')
    sys.exit(1)

# Cargar el cerebro entrenado
modelo_ia = joblib.load(MODEL_FILE)
metricas_ia = joblib.load(METRICS_FILE)

def predecir_cuenta(descripcion):
    probas = modelo_ia.predict_proba([descripcion])[0]
    clase_idx = np.argmax(probas)
    cuenta = modelo_ia.classes_[clase_idx]
    confianza = probas[clase_idx] * 100
    
    # Umbral de duda de la Inteligencia Artificial (40%)
    if confianza < 40.0:
        cuenta = "Desconocido - Requiere Revisión Humana"
        
    return cuenta, confianza

# FUNCIONES CONTABLES
asientos_session = []

def calcular_compra(monto_total, descripcion):
    iva = monto_total * 0.13
    neto = monto_total * 0.87
    cuenta_sugerida, confianza = predecir_cuenta(descripcion)
    return {
        'tipo': 'Compra', 'descripcion': descripcion, 'monto_total': monto_total,
        'neto': round(neto, 2), 'iva': round(iva, 2), 'it': 0.00,
        'cuenta_sugerida': cuenta_sugerida, 'confianza_ia': round(confianza, 2),
        'debe': [{'cuenta': cuenta_sugerida, 'monto': round(neto, 2)},
                 {'cuenta': 'Crédito Fiscal IVA', 'monto': round(iva, 2)}],
        'haber': [{'cuenta': 'Caja/Bancos', 'monto': monto_total}]
    }

def calcular_venta(monto_total, descripcion):
    iva = monto_total * 0.13
    it = monto_total * 0.03
    neto = monto_total * 0.84
    cuenta_sugerida, confianza = predecir_cuenta(descripcion)
    return {
        'tipo': 'Venta', 'descripcion': descripcion, 'monto_total': monto_total,
        'neto': round(neto, 2), 'iva': round(iva, 2), 'it': round(it, 2),
        'cuenta_sugerida': cuenta_sugerida, 'confianza_ia': round(confianza, 2),
        'debe': [{'cuenta': 'Caja/Bancos', 'monto': monto_total}],
        'haber': [{'cuenta': cuenta_sugerida, 'monto': round(neto, 2)},
                  {'cuenta': 'Débito Fiscal IVA', 'monto': round(iva, 2)},
                  {'cuenta': 'IT por Pagar', 'monto': round(it, 2)}]
    }

def validar_asiento(debe, haber):
    total_debe = sum(item['monto'] for item in debe)
    total_haber = sum(item['monto'] for item in haber)
    return abs(total_debe - total_haber) < 0.01

def limpiar_nombre_archivo(nombre):
    caracteres_invalidos = r'[<>:"/\\|?*]'
    nombre_limpio = re.sub(caracteres_invalidos, '', nombre).replace(' ', '_')
    if len(nombre_limpio) > 50: nombre_limpio = nombre_limpio[:50]
    if len(nombre_limpio) < 3: nombre_limpio = "asientos_contables"
    return nombre_limpio

def exportar_asientos(asientos, filepath, formato='excel'):
    filas = []
    for asiento in asientos:
        total_debe = sum(item['monto'] for item in asiento['debe'])
        total_haber = sum(item['monto'] for item in asiento['haber'])
        filas.append({
            'Fecha/Hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Tipo': asiento['tipo'],
            'Descripción': asiento['descripcion'],
            'Cuenta Sugerida': asiento['cuenta_sugerida'],
            'Confianza IA (%)': asiento['confianza_ia'],
            'Total Debe': total_debe,
            'Total Haber': total_haber,
            'Neto': asiento['neto'],
            'IVA': asiento['iva'],
            'IT': asiento['it']
        })
    df_export = pd.DataFrame(filas)
    if formato == 'excel':
        df_export.to_excel(filepath, index=False, sheet_name='Asientos')
    else:
        df_export.to_csv(filepath, index=False, encoding='utf-8-sig')
    return True, filepath

# INTERFAZ GRÁFICA (Tkinter)
class CalculadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Contable Inteligente - Bolivia")
        self.root.geometry("900x700")
        self.root.resizable(True, True)  # Ventana redimensionable
        self.root.configure(bg="#2C3E50")  # Fondo azul oscuro profesional

        style = ttk.Style()
        style.theme_use('clam')
        
        # Configuración de colores vivos y profesionales
        style.configure('TNotebook', background='#34495E', bordercolor='#1ABC9C')
        style.configure('TNotebook.Tab', padding=[20, 12], font=('Arial', 11, 'bold'), 
                       background='#3498DB', foreground='white', bordercolor='#2980B9')
        style.map('TNotebook.Tab', background=[('selected', '#1ABC9C'), ('active', '#2980B9')])
        
        style.configure('TLabel', background="#2C3E50", foreground='white', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=8,
                       background='#3498DB', foreground='white', bordercolor='#2980B9')
        style.map('TButton', background=[('active', '#2980B9'), ('pressed', '#1ABC9C')])
        
        style.configure('TRadiobutton', background="#2C3E50", foreground='white', 
                       font=('Arial', 10), focuscolor='none')
        style.configure('TLabelFrame', background="#2C3E50", foreground='#ECF0F1', 
                       bordercolor='#3498DB', font=('Arial', 11, 'bold'))
        style.configure('TLabelFrame.Label', background="#2C3E50", foreground='#1ABC9C', 
                       font=('Arial', 12, 'bold'))
        
        # Estilos para Entry (campos de texto)
        style.configure('TEntry', fieldbackground='#34495E', foreground='white', 
                       bordercolor='#3498DB', insertcolor='white')
        style.map('TEntry', fieldbackground=[('focus', '#4A5F7F')])
        
        # Estilos para Treeview (tabla)
        style.configure('Treeview', background='#34495E', foreground='white', 
                       fieldbackground='#34495E', bordercolor='#3498DB')
        style.configure('Treeview.Heading', background='#3498DB', foreground='white', 
                       font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#1ABC9C')])
        
        # Estilo para Frame
        style.configure('TFrame', background='#2C3E50')

        # Notebook (Pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Tabs
        self.tab_registro = ttk.Frame(self.notebook, padding=20)
        self.tab_registro.configure(style='TFrame')
        self.tab_visor = ttk.Frame(self.notebook, padding=20)
        self.tab_visor.configure(style='TFrame')
        self.tab_metricas = ttk.Frame(self.notebook, padding=20)
        self.tab_metricas.configure(style='TFrame')

        self.notebook.add(self.tab_registro, text="Registrar Asiento")
        self.notebook.add(self.tab_visor, text="Ver y Exportar Asientos")
        self.notebook.add(self.tab_metricas, text="Métricas del Modelo")

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        self.setup_tab_registro()
        self.setup_tab_visor()
        self.setup_tab_metricas()

    def setup_tab_registro(self):
        # Frame Inputs
        frame_inputs = ttk.LabelFrame(self.tab_registro, text=" Nuevo Asiento ", padding=15)
        frame_inputs.pack(fill="x", pady=(0, 15))

        # Tipo (RadioButtons)
        ttk.Label(frame_inputs, text="Tipo de operación:").grid(row=0, column=0, sticky='w', pady=5)
        self.var_tipo = tk.StringVar(value='1')
        ttk.Radiobutton(frame_inputs, text="Compra", variable=self.var_tipo, value='1').grid(row=0, column=1, sticky='w', padx=5, pady=5)
        ttk.Radiobutton(frame_inputs, text="Venta", variable=self.var_tipo, value='2').grid(row=0, column=2, sticky='w', padx=5, pady=5)

        # Monto
        ttk.Label(frame_inputs, text="Monto Total (Bs):").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_monto = ttk.Entry(frame_inputs, width=20, font=('Arial', 11))
        self.entry_monto.grid(row=1, column=1, columnspan=2, sticky='we', padx=5, pady=5)

        # Descripción
        ttk.Label(frame_inputs, text="Descripción:").grid(row=2, column=0, sticky='w', pady=5)
        self.entry_desc = ttk.Entry(frame_inputs, width=50, font=('Arial', 11))
        self.entry_desc.grid(row=2, column=1, columnspan=2, sticky='we', padx=5, pady=5)

        frame_inputs.columnconfigure(1, weight=1)
        frame_inputs.columnconfigure(2, weight=1)

        # Botón Registrar
        btn_registrar = ttk.Button(self.tab_registro, text="Generar Asiento", command=self.registrar)
        btn_registrar.pack(fill="x", pady=(0, 10))

        # Cuadro de resultados (log)
        frame_log = ttk.LabelFrame(self.tab_registro, text=" Resultado del Asiento ", padding=10)
        frame_log.pack(expand=True, fill="both")
        
        self.text_log = tk.Text(frame_log, height=15, state='disabled', font=('Courier New', 10, 'bold'), 
                           bg="#0D1117", fg="#58A6FF", insertbackground="#58A6FF", 
                           selectbackground="#1F6FEB", selectforeground="white")
        self.text_log.pack(expand=True, fill="both")
        
        # Mensaje de bienvenida
        mensaje_bienvenida = "🤖=== SIMULADOR CONTABLE INTELIGENTE ===🤖\n" \
                             "📊 Normativa: Ley 843 (Bolivia)\n" \
                             "💰 IVA: 13% | IT: 3%\n\n" \
                             "⚠️  Nota: La clasificación de cuentas depende 100% del dataset.\n" \
                             "📚 Para que nuevos ítems se clasifiquen correctamente, deben\n" \
                             "    ser agregados al modelo de entrenamiento.\n\n" \
                             "✨ ¡Listo para registrar tus transacciones! ✨\n\n"
        self.text_log.config(state='normal')
        self.text_log.insert(tk.END, mensaje_bienvenida)
        self.text_log.config(state='disabled')

    def registrar(self):
        tipo = self.var_tipo.get()
        monto_str = self.entry_monto.get().strip()
        desc = self.entry_desc.get().strip()
        
        if not monto_str:
            messagebox.showerror("Error", "Debe ingresar un monto.")
            return
        
        try:
            monto = float(monto_str)
            if monto <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto numérico válido mayor a 0.")
            return
            
        if len(desc) < 5:
            messagebox.showerror("Error", "La descripción debe tener al menos 5 caracteres.")
            return
            
        if tipo == '1':
            asiento = calcular_compra(monto, desc)
        else:
            asiento = calcular_venta(monto, desc)
            
        if validar_asiento(asiento['debe'], asiento['haber']):
            asientos_session.append(asiento)
            
            # Formatear log
            log = f"\n{'='*60}\n"
            log += f" ASIENTO REGISTRADO EXITOSAMENTE\n"
            log += f"{'='*60}\n"
            log += f" TIPO:        {asiento['tipo']}\n"
            log += f" DESCRIPCIÓN: {asiento['descripcion']}\n"
            log += f" MONTO TOTAL: Bs {asiento['monto_total']:.2f}\n"
            log += f"{'-'*60}\n"
            log += f" IA Sugiere Cuenta: {asiento['cuenta_sugerida']}\n"
            log += f" Confianza IA:      {asiento['confianza_ia']:.1f}%\n"
            log += f"{'-'*60}\n"
            log += f" ASIENTO CONTABLE:\n"
            log += f"{'-'*60}\n"
            
            for item in asiento['debe']:
                log += f" [DEBE]  {item['cuenta']:<35} Bs {item['monto']:>10.2f}\n"
            for item in asiento['haber']:
                log += f" [HABER] {item['cuenta']:<35} Bs {item['monto']:>10.2f}\n"
            log += f"{'='*60}\n"
            
            self.text_log.config(state='normal')
            self.text_log.insert(tk.END, log)
            self.text_log.see(tk.END)
            self.text_log.config(state='disabled')
            
            # Limpiar entradas
            self.entry_monto.delete(0, tk.END)
            self.entry_desc.delete(0, tk.END)
            self.entry_monto.focus()
            
            # Actualizar tabla si la pestaña está visible
            self.actualizar_tabla()
        else:
            messagebox.showerror("Error Crítico", "El asiento no cuadra. Revise los cálculos.")

    def setup_tab_visor(self):
        # Tabla de Asientos
        columns = ('#', 'Tipo', 'Descripción', 'Cuenta Sugerida', 'Monto', 'Confianza')
        self.tree = ttk.Treeview(self.tab_visor, columns=columns, show='headings', height=15)
        
        self.tree.heading('#', text='#')
        self.tree.heading('Tipo', text='Tipo')
        self.tree.heading('Descripción', text='Descripción')
        self.tree.heading('Cuenta Sugerida', text='Cuenta Sugerida')
        self.tree.heading('Monto', text='Monto (Bs)')
        self.tree.heading('Confianza', text='Confianza')
        
        self.tree.column('#', width=40, anchor='center')
        self.tree.column('Tipo', width=80, anchor='center')
        self.tree.column('Descripción', width=200)
        self.tree.column('Cuenta Sugerida', width=180)
        self.tree.column('Monto', width=100, anchor='e')
        self.tree.column('Confianza', width=90, anchor='center')
        
        scrollbar = ttk.Scrollbar(self.tab_visor, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(expand=True, fill='both', pady=(0, 5))
        scrollbar.place(in_=self.tree, relx=1.0, rely=0, relheight=1.0, anchor="ne")

        # Label contador
        self.lbl_contador = ttk.Label(self.tab_visor, text="Asientos registrados: 0", font=('Arial', 10, 'bold'))
        self.lbl_contador.pack(anchor='w', pady=(0, 15))

        # Frame de Exportación
        frame_export = ttk.LabelFrame(self.tab_visor, text=" Exportar ", padding=15)
        frame_export.pack(fill='x')
        
        ttk.Label(frame_export, text="Formato:").grid(row=0, column=0, sticky='w', pady=5)
        self.var_formato = tk.StringVar(value='excel')
        ttk.Radiobutton(frame_export, text="Excel (.xlsx)", variable=self.var_formato, value='excel').grid(row=0, column=1, padx=5)
        ttk.Radiobutton(frame_export, text="CSV (.csv)", variable=self.var_formato, value='csv').grid(row=0, column=2, padx=5)
        
        btn_exportar = ttk.Button(frame_export, text="Exportar Asientos", command=self.exportar)
        btn_exportar.grid(row=0, column=3, padx=20)

    def on_tab_change(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        if "Ver" in tab_text:
            self.actualizar_tabla()

    def actualizar_tabla(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Llenar datos
        for i, asiento in enumerate(asientos_session, 1):
            self.tree.insert('', tk.END, values=(
                i,
                asiento['tipo'],
                asiento['descripcion'],
                asiento['cuenta_sugerida'],
                f"{asiento['monto_total']:.2f}",
                f"{asiento['confianza_ia']:.1f}%"
            ))
            
        # Actualizar contador
        if hasattr(self, 'lbl_contador'):
            self.lbl_contador.config(text=f"Asientos registrados: {len(asientos_session)}")

    def exportar(self):
        if not asientos_session:
            messagebox.showinfo("Exportar", "No hay asientos registrados para exportar.")
            return
            
        formato = self.var_formato.get()
        ext = ".xlsx" if formato == "excel" else ".csv"
        filetypes = [("Excel files", "*.xlsx")] if formato == "excel" else [("CSV files", "*.csv")]
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=filetypes,
            title="Guardar como",
            initialfile="asientos_contables"
        )
        
        if not filepath:
            return  # Canceló dialog
            
        try:
            exito, resultado = exportar_asientos(asientos_session, filepath, formato)
            if exito:
                messagebox.showinfo("Éxito", f"Archivo exportado correctamente en:\n{resultado}")
        except PermissionError:
            messagebox.showerror("Error", "El archivo está abierto en Excel. Ciérralo e intenta nuevamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado al exportar:\n{str(e)}")

    def setup_tab_metricas(self):
        # Frame de métricas textuales
        frame_info = ttk.LabelFrame(self.tab_metricas, text=" Información de Entrenamiento del Modelo ", padding=20)
        frame_info.pack(fill="x", pady=(0, 20))
        
        acc = metricas_ia['acc']
        total_muestras = metricas_ia['total_filas']
        cuentas_unicas = metricas_ia['cuentas_unicas']
        muestras_test = metricas_ia['muestras_test']
        
        info_text = (
            f"🎯  IA Entrenada: Naive Bayes (MultinomialNB)\n\n"
            f"📊  Total de muestras en el dataset (Conocimiento): {total_muestras}\n"
            f"🗂️  Cuentas contables únicas clasificadas: {cuentas_unicas}\n\n"
            f"🧪  Muestras separadas para validación de examen: {muestras_test}\n"
            f"⭐  Precisión del Modelo (Accuracy): {acc * 100:.2f}%\n"
        )
        
        lbl_info = ttk.Label(frame_info, text=info_text, font=('Arial', 12), justify="left")
        lbl_info.pack(anchor="w", padx=10, pady=10)
        
        # Frame del Gráfico
        frame_grafico = ttk.LabelFrame(self.tab_metricas, text=" Visualización para Informes ", padding=20)
        frame_grafico.pack(fill="x")
        
        ttk.Label(frame_grafico, text="Puedes generar un gráfico dinámico presionando el botón de abajo.\nEsto abrirá una ventana para que puedas tomar una captura de pantalla y adjuntarla a tus documentos.", justify="center", font=('Arial', 10)).pack(pady=(0,15))
        
        btn_grafico = ttk.Button(frame_grafico, text="📸 Generar Gráfico de Rendimiento Base", command=self.mostrar_grafico)
        btn_grafico.pack(pady=10)
        
    def mostrar_grafico(self):
        import matplotlib.pyplot as plt
        
        acc = metricas_ia['acc']
        total_muestras = metricas_ia['total_filas']
        cuentas_unicas = metricas_ia['cuentas_unicas']
        
        plt.figure(figsize=(8, 5))
        bars = plt.bar(['Precisión del Modelo IA'], [acc], color='#4ECDC4', edgecolor='black')
        plt.ylim(0, 1.1)
        plt.ylabel('Rendimiento (0 a 1)')
        plt.title('Rendimiento de Simulación: Clasificación Contable', fontsize=14, pad=15)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Añadir porcentaje sobre la barra
        plt.text(0, acc + 0.03, f"{acc * 100:.2f}%", ha='center', fontweight='bold', fontsize=14, color='#292f36')
        
        # Etiqueta inferior con contexto de los datos
        plt.figtext(0.1, 0.01, f"Muestras de entrenamiento: {total_muestras}  |  Total Cuentas: {cuentas_unicas}", 
                    ha="left", fontsize=9, bbox={"facecolor":"orange", "alpha":0.2, "pad":5})
                    
        plt.tight_layout(rect=[0, 0.05, 1, 1])
        plt.show()

if __name__ == "__main__":
    acc = metricas_ia['acc']
    print(f"Modelo cargado. Precisión en pruebas: {acc*100:.2f}%")
    
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()