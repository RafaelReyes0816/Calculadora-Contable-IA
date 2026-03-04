import pandas as pd
from calculadora_contable import df_entrenamiento, predecir_cuenta, modelo_ia, X_train, y_train, X_test, y_test
from sklearn.metrics import accuracy_score

print("In X_train?", 'Compra de comedor de madera' in X_train.values)
print("In X_test?", 'Compra de comedor de madera' in X_test.values)

# Retrain on all
modelo_ia.fit(df_entrenamiento['descripcion'], df_entrenamiento['cuenta_sugerida'])
print("Prediction after full fit:", predecir_cuenta('Comedor de madera'))

