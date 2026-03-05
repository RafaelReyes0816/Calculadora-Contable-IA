import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

EXCEL_DATASET = "dataset_entrenamiento.xlsx"

print("=" * 60)
print("   INICIANDO ENTRENAMIENTO DE IA CONTABLE")
print("=" * 60)

if not os.path.exists(EXCEL_DATASET):
    print(f"\nERROR: No se encontró el archivo '{EXCEL_DATASET}'.")
    print("Por favor, asegúrate de colocar tus datos en el excel antes de entrenar.")
    exit(1)

try:
    print(f"\nLeyendo '{EXCEL_DATASET}'...")
    df = pd.read_excel(EXCEL_DATASET)
    df.dropna(subset=['descripcion', 'cuenta_sugerida'], inplace=True)
    # Convertir a texto por si hay numeros sueltos en el excel
    df['descripcion'] = df['descripcion'].astype(str)
    df['cuenta_sugerida'] = df['cuenta_sugerida'].astype(str)
    print(f"✓ Dataset cargado correctamente: {len(df)} filas válidas.")
except Exception as e:
    print(f"\nERROR CRÍTICO al leer el archivo Excel:")
    print(str(e))
    print("\n¿Tienes el archivo abierto? Ciérralo e intenta de nuevo.")
    exit(1)

# Separar validación para métricas
X_train, X_test, y_train, y_test = train_test_split(
    df['descripcion'],
    df['cuenta_sugerida'],
    test_size=0.2,
    random_state=42
)

# Configurar Pipeline IA
stop_words_es = ['de', 'para', 'el', 'la', 'los', 'las', 'un', 'una', 'en', 'por', 'con', 'a', 'al', 'del', 'y', 'o']
modelo_ia = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words=stop_words_es, ngram_range=(1, 2))),
    ('clf', MultinomialNB(alpha=0.2))
])

print("\nEntrenando conocimiento con el 100% de la base de datos...")
modelo_ia.fit(df['descripcion'], df['cuenta_sugerida'])

# Calcular score en las pruebas (20% invisible)
y_pred_test = modelo_ia.predict(X_test)
acc = accuracy_score(y_test, y_pred_test)

# Guardar modelo y métricas en archivos estáticos compilados
joblib.dump(modelo_ia, 'modelo_ia.pkl')
joblib.dump({
    'total_filas': len(df),
    'cuentas_unicas': len(df['cuenta_sugerida'].unique()),
    'acc': acc,
    'muestras_test': len(X_test)
}, 'metricas_ia.pkl')

print("\n" + "=" * 60)
print(" ✓ ¡ENTRENAMIENTO EXITOSO!")
print("=" * 60)
print(f" Precisión de exactitud: {acc * 100:.2f}%")
print(f" Cuentas únicas aprendidas: {len(df['cuenta_sugerida'].unique())}")
print("-" * 60)
print(" ✓ El archivo 'modelo_ia.pkl' ha sido generado o actualizado.")
print(" ✓ Ya puedes correr 'calculadora_contable.py' para trabajar.")
print("=" * 60)
