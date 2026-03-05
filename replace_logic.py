import re

with open('calculadora_contable.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Borrar todo el bloque desde 'data = {' hasta 'modelo_ia.fit(...)'
# Pero conservar la funcion predecir_cuenta
# Hay un comentario "# ============================================================================="
# justo antes de "DATASET Y ENTRENAMIENTO DEL MODELO IA"
# Podemos reemplazar desde "data = {" hasta "def predecir_cuenta"

new_imports = """import joblib
import os
import sys

# =============================================================================
# CARGA DEL MODELO IA PRE-ENTRENADO
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(BASE_DIR, 'modelo_ia.pkl')
METRICS_FILE = os.path.join(BASE_DIR, 'metricas_ia.pkl')

if not os.path.exists(MODEL_FILE) or not os.path.exists(METRICS_FILE):
    import tkinter.messagebox as messagebox
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('Error', 'No se encontró el modelo de la Inteligencia Artificial.\nPor favor, ejecute primero el archivo "entrenador_ia.py" para que el programa pueda estudiar el Excel.')
    sys.exit(1)

# Cargar el cerebro entrenado
modelo_ia = joblib.load(MODEL_FILE)
metricas_ia = joblib.load(METRICS_FILE)

def predecir_cuenta"""

code = re.sub(r'data = \{.*?def predecir_cuenta', new_imports, code, flags=re.DOTALL)

with open('calculadora_contable.py', 'w', encoding='utf-8') as f:
    f.write(code)

