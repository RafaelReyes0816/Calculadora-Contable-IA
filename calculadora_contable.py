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

# =============================================================================
# DATASET Y ENTRENAMIENTO DEL MODELO IA
# =============================================================================
data = {
    'descripcion': [
        'Compra de papel bond para oficina', 'Compra de libros contables', 'Compra de material de escritorio',
        'Compra de bolígrafos y carpetas', 'Compra de grapas y engargolados', 'Compra de sobres y etiquetas',
        'Adquisición de computadoras laptop', 'Adquisición de impresora', 'Compra de celular para gerente',
        'Compra de monitor pantalla', 'Compra de teclado y mouse', 'Compra de disco duro externo',
        'Pago de servicios de internet', 'Pago de agua y luz', 'Pago de teléfono', 'Pago de energía eléctrica',
        'Pago de servicio de agua potable', 'Compra de útiles de limpieza', 'Compra de jabón y desinfectante',
        'Compra de escobas y trapeadores', 'Compra de papel higiénico', 'Adquisición de mobiliario de oficina',
        'Compra de escritorio', 'Compra de sillas', 'Compra de archiveros metálicos', 'Compra de estantes',
        'Compra de mercadería para reventa', 'Compra de productos para venta', 'Compra de inventario',
        'Compra de repuestos para vehículos', 'Pago de gasolina vehículos', 'Compra de aceite para motor',
        'Mantenimiento de flota vehicular', 'Servicio de asesoría legal', 'Pago de honorarios abogado',
        'Servicio de consultoría contable', 'Pago de auditoría externa', 'Compra de alimentos para personal',
        'Compra de carne para asado', 'Compra de almuerzos para empleados', 'Compra de refrigerios para reunión',
        'Pago de viáticos alimentación', 'Compra de tornillos y herramientas', 'Compra de martillo y destornilladores',
        'Compra de equipo de seguridad', 'Pago de alquiler de local', 'Pago de renta de oficina', 'Alquiler de bodega',
        'Venta de productos terminados', 'Venta de mercadería al contado', 'Prestación de servicios profesionales',
        'Venta de maquinaria usada', 'Venta de servicios', 'Facturación de servicios', 'Pago de gasolina vehículos',
        'Compra de diesel para flota', 'Carga de combustible', 'Pago de seguros', 'Gastos de representación',
        'Comisiones bancarias', 'Pago de licencias de software',
        'Compra de televisor LED', 'Compra de pantalla smart TV', 'Adquisición de televisor 4K',
        'Compra de proyector', 'Adquisición de cañonera',
        'Compra de refrigerador', 'Adquisición de nevera',
        'Compra de microondas', 'Compra de licuadora',
        'Servicio de hosting web', 'Pago de dominio internet',
        'Compra de cámara fotográfica', 'Adquisición de webcam',
        'Pago de pasajes', 'Compra de boletos aéreos',
        'Compra de impresora 3D', 'Adquisición de plotter',
        # Nuevos: Hogar / Muebles
        'Compra de cama matrimonial', 'Adquisición de sofá para sala',
        'Compra de comedor de madera', 'Adquisición de ropero',
        # Nuevos: Equipos de Computación
        'Compra de servidor rack', 'Adquisición de tarjeta gráfica',
        'Compra de memoria RAM', 'Compra de procesador intel',
        'Compra de placa base', 'Adquisición de tablet iPad',
        'Compra de router inalámbrico', 'Compra de switch de red',
        # Nuevos: Comidas y Víveres
        'Compra de mercado para la semana', 'Adquisición de víveres',
        'Compra de verduras y frutas', 'Pago de cuenta en restaurante',
        'Compra de comida rápida', 'Compra de snacks y bebidas',
        'Compra de café y azúcar', 'Compra de desayuno ejecutivo',
        # Nuevos: Productos para el hogar / Limpieza
        'Compra de detergente para ropa', 'Adquisición de lavandina y cloro',
        'Compra de desodorante ambiental', 'Compra de bolsas de basura',
        'Compra de cera para pisos', 'Compra de esponjas y lavavajillas',
        # Nuevos: Electrodomésticos
        'Compra de lavadora de ropa', 'Adquisición de secadora',
        'Compra de cocina a gas', 'Compra de estufa eléctrica',
        'Compra de horno eléctrico', 'Compra de aire acondicionado',
        # Nuevos: Enseres menores
        'Compra de tostadora', 'Compra de plancha de ropa',
        'Compra de batidora de mano', 'Compra de cafetera eléctrica',
        # Nuevos: Útiles de Oficina / Ventas Adicionales
        'Venta de cuartillas de papel', 'Venta de hojas de cuartilla',
        'Compra de paquete de cuartilla', 'Adquisición de cuartilla blanca'
    ],
    'cuenta_sugerida': [
        'Gasto - Útiles de Oficina', 'Gasto - Útiles de Oficina', 'Gasto - Útiles de Oficina',
        'Gasto - Útiles de Oficina', 'Gasto - Útiles de Oficina', 'Gasto - Útiles de Oficina',
        'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación',
        'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación',
        'Gasto - Servicios Básicos', 'Gasto - Servicios Básicos', 'Gasto - Servicios Básicos', 'Gasto - Servicios Básicos',
        'Gasto - Servicios Básicos', 'Gasto - Limpieza y Aseo', 'Gasto - Limpieza y Aseo', 'Gasto - Limpieza y Aseo',
        'Gasto - Limpieza y Aseo', 'Activo Fijo - Muebles y Enseres', 'Activo Fijo - Muebles y Enseres',
        'Activo Fijo - Muebles y Enseres', 'Activo Fijo - Muebles y Enseres', 'Activo Fijo - Muebles y Enseres',
        'Activo - Mercaderías', 'Activo - Mercaderías', 'Activo - Mercaderías',
        'Gasto - Mantenimiento Vehículos', 'Gasto - Mantenimiento Vehículos', 'Gasto - Mantenimiento Vehículos',
        'Gasto - Mantenimiento Vehículos', 'Gasto - Honorarios Profesionales', 'Gasto - Honorarios Profesionales',
        'Gasto - Honorarios Profesionales', 'Gasto - Honorarios Profesionales', 'Gasto - Alimentación Personal',
        'Gasto - Alimentación Personal', 'Gasto - Alimentación Personal', 'Gasto - Alimentación Personal',
        'Gasto - Alimentación Personal', 'Gasto - Herramientas', 'Gasto - Herramientas', 'Gasto - Herramientas',
        'Gasto - Alquileres', 'Gasto - Alquileres', 'Gasto - Alquileres',
        'Ingreso - Ventas', 'Ingreso - Ventas', 'Ingreso - Servicios', 'Ingreso - Ventas', 'Ingreso - Servicios',
        'Ingreso - Servicios', 'Gasto - Combustibles', 'Gasto - Combustibles', 'Gasto - Combustibles',
        'Gasto - Seguros', 'Gasto - Representación', 'Gasto - Comisiones', 'Gasto - Software',
        'Activo Fijo - Equipos de Imagen', 'Activo Fijo - Equipos de Imagen', 'Activo Fijo - Equipos de Imagen',
        'Activo Fijo - Equipos de Imagen', 'Activo Fijo - Equipos de Imagen',
        'Activo Fijo - Electrodomésticos', 'Activo Fijo - Electrodomésticos',
        'Gasto - Enseres Menores', 'Gasto - Enseres Menores',
        'Gasto - Servicios Informáticos', 'Gasto - Servicios Informáticos',
        'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación',
        'Gasto - Viáticos', 'Gasto - Viáticos',
        'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación',
        # Nuevos: Hogar / Muebles (4)
        'Activo Fijo - Muebles y Enseres', 'Activo Fijo - Muebles y Enseres',
        'Activo Fijo - Muebles y Enseres', 'Activo Fijo - Muebles y Enseres',
        # Nuevos: Equipos de Computación (8)
        'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación',
        'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación',
        'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación',
        'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación',
        # Nuevos: Comidas y Víveres (8)
        'Gasto - Alimentación Personal', 'Gasto - Alimentación Personal',
        'Gasto - Alimentación Personal', 'Gasto - Alimentación Personal',
        'Gasto - Alimentación Personal', 'Gasto - Alimentación Personal',
        'Gasto - Alimentación Personal', 'Gasto - Alimentación Personal',
        # Nuevos: Productos para el hogar / Limpieza (6)
        'Gasto - Limpieza y Aseo', 'Gasto - Limpieza y Aseo',
        'Gasto - Limpieza y Aseo', 'Gasto - Limpieza y Aseo',
        'Gasto - Limpieza y Aseo', 'Gasto - Limpieza y Aseo',
        # Nuevos: Electrodomésticos (6)
        'Activo Fijo - Electrodomésticos', 'Activo Fijo - Electrodomésticos',
        'Activo Fijo - Electrodomésticos', 'Activo Fijo - Electrodomésticos',
        'Activo Fijo - Electrodomésticos', 'Activo Fijo - Electrodomésticos',
        # Nuevos: Enseres menores (4)
        'Gasto - Enseres Menores', 'Gasto - Enseres Menores',
        'Gasto - Enseres Menores', 'Gasto - Enseres Menores',
        # Nuevos: Útiles de Oficina / Ventas Adicionales (4)
        'Ingreso - Ventas', 'Ingreso - Ventas',
        'Gasto - Útiles de Oficina', 'Gasto - Útiles de Oficina'
    ]
}

# Cargar dataset de entrenamiento desde el archivo Excel proporcionado.
# Si falla la lectura (por ejemplo, si el archivo no existe o está corrupto),
# se usa como respaldo el dataset embebido en la variable `data`.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_DATASET = os.path.join(BASE_DIR, "dataset_entrenamiento.xlsx")

try:
    df_entrenamiento = pd.read_excel(EXCEL_DATASET)
    df_entrenamiento.dropna(subset=['descripcion', 'cuenta_sugerida'], inplace=True)
except Exception:
    df_entrenamiento = pd.DataFrame(data)

X_train, X_test, y_train, y_test = train_test_split(
    df_entrenamiento['descripcion'],
    df_entrenamiento['cuenta_sugerida'],
    test_size=0.2,
    random_state=42
)

# Palabras sin valor para ignorar ("ruido")
stop_words_es = ['de', 'para', 'el', 'la', 'los', 'las', 'un', 'una', 'en', 'por', 'con', 'a', 'al', 'del', 'y', 'o']

modelo_ia = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words=stop_words_es)),
    ('clf', MultinomialNB(alpha=0.2))
])

# ENTRENAR CON EL 100% PARA NO "OLVIDAR" PALABRAS DEL DATASET
modelo_ia.fit(df_entrenamiento['descripcion'], df_entrenamiento['cuenta_sugerida'])

def predecir_cuenta(descripcion):
    probas = modelo_ia.predict_proba([descripcion])[0]
    clase_idx = np.argmax(probas)
    cuenta = modelo_ia.classes_[clase_idx]
    confianza = probas[clase_idx] * 100
    return cuenta, confianza

# =============================================================================
# FUNCIONES CONTABLES
# =============================================================================
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

# =============================================================================
# INTERFAZ GRÁFICA (Tkinter)
# =============================================================================
class CalculadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Contable Inteligente - Bolivia")
        self.root.geometry("800x600")
        self.root.resizable(True, True)  # Ventana redimensionable
        self.root.configure(bg="#f4f4f9")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', padding=[15, 5], font=('Arial', 11, 'bold'))
        style.configure('TLabel', background="#f4f4f9", font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=5)
        style.configure('TRadiobutton', background="#f4f4f9", font=('Arial', 10))

        # Notebook (Pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Tabs
        self.tab_registro = ttk.Frame(self.notebook, padding=20)
        self.tab_visor = ttk.Frame(self.notebook, padding=20)
        self.tab_metricas = ttk.Frame(self.notebook, padding=20)

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
        
        self.text_log = tk.Text(frame_log, height=15, state='disabled', font=('Courier New', 10), bg="#1e1e1e", fg="#00ff00")
        self.text_log.pack(expand=True, fill="both")
        
        # Mensaje de bienvenida
        mensaje_bienvenida = "=== SIMULADOR CONTABLE INTELIGENTE ===\n" \
                             "Normativa: Ley 843 (Bolivia)\n" \
                             "IVA: 13% | IT: 3%\n\n" \
                             "Nota: La clasificación de cuentas depende 100% del dataset.\n" \
                             "Para que nuevos ítems se clasifiquen correctamente, deben\n" \
                             "ser agregados al modelo de entrenamiento.\n\n"
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
        
        y_pred_test = modelo_ia.predict(X_test)
        acc = accuracy_score(y_test, y_pred_test)
        
        info_text = (
            f"🎯  IA Entrenada: Naive Bayes (MultinomialNB)\n\n"
            f"📊  Total de muestras en el dataset (Conocimiento): {len(df_entrenamiento)}\n"
            f"🗂️  Cuentas contables únicas clasificadas: {len(df_entrenamiento['cuenta_sugerida'].unique())}\n\n"
            f"🧪  Muestras separadas para validación de examen: {len(X_test)}\n"
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
        
        y_pred_test = modelo_ia.predict(X_test)
        acc = accuracy_score(y_test, y_pred_test)
        
        plt.figure(figsize=(8, 5))
        bars = plt.bar(['Precisión del Modelo IA'], [acc], color='#4ECDC4', edgecolor='black')
        plt.ylim(0, 1.1)
        plt.ylabel('Rendimiento (0 a 1)')
        plt.title('Rendimiento de Simulación: Clasificación Contable', fontsize=14, pad=15)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Añadir porcentaje sobre la barra
        plt.text(0, acc + 0.03, f"{acc * 100:.2f}%", ha='center', fontweight='bold', fontsize=14, color='#292f36')
        
        # Etiqueta inferior con contexto de los datos
        plt.figtext(0.1, 0.01, f"Muestras de entrenamiento: {len(df_entrenamiento)}  |  Total Cuentas: {len(df_entrenamiento['cuenta_sugerida'].unique())}", 
                    ha="left", fontsize=9, bbox={"facecolor":"orange", "alpha":0.2, "pad":5})
                    
        plt.tight_layout(rect=[0, 0.05, 1, 1])
        plt.show()

if __name__ == "__main__":
    y_pred_test = modelo_ia.predict(X_test)
    acc = accuracy_score(y_test, y_pred_test)
    print(f"Modelo cargado. Precisión en pruebas: {acc*100:.2f}%")
    
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()