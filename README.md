# 🤖📊 Simulador Contable Inteligente

_Asistente local impulsado por Inteligencia Artificial para la clasificación automatizada de asientos y hechos contables._

---

## ⚙️ Guía de Instalación y Ejecución

Para correr este proyecto en cualquier computadora local que tenga Python instalado, sigue estos pasos:

1. **Clonar el repositorio o descargar la carpeta:**
   Asegúrate de tener todos los archivos del proyecto juntos en una misma carpeta (`calculadora_contable.py`, `entrenador_ia.py`, y `dataset_entrenamiento.xlsx`).

2. **Crear y activar un entorno virtual (VENV):**  
   Este paso es crucial para aislar el proyecto y evitar conflictos de librerías en tu equipo. Abre una terminal (como PowerShell o CMD) dentro de la carpeta del proyecto y ejecuta:

   **🟦 Para usuarios de Windows (Recomendado):**

   ```powershell
   # 1. Crear el entorno virtual
   python -m venv venv

   # 2. Activar el entorno virtual
   # (Nota: si te da error de permisos, ejecuta tu editor de código o PowerShell como administrador)
   .\venv\Scripts\Activate
   ```

   **🟧 Para usuarios de Linux / Mac:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar Dependencias Requeridas:**

   Este repositorio cuenta con un archivo estandarizado con las versiones compatibles que necesita la Inteligencia Artificial. Instálalas corriendo (asegúrate de que en tu terminal se vea un `(venv)` a la izquierda antes de ejecutar esto):

   ```cmd
   pip install -r requirements.txt
   ```

4. **Ejecución de la Aplicación (Usuario Final):**
   Una vez instalado todo, para abrir la interfaz gráfica principal con la IA congelada y lista para clasificar asientos, solo debes ejecutar:

   ```cmd
   python calculadora_contable.py
   ```

5. **Re-entrenamiento de la IA (Modo Desarrollador):**
   Si agregaste nuevas filas de conocimiento al archivo Excel (`dataset_entrenamiento.xlsx`), debes compilar temporalmente un nuevo cerebro antes de usar el programa. Hazlo ejecutando:
   ```cmd
   python entrenador_ia.py
   ```
   _Esto compilará y generará un nuevo archivo protegido (`modelo_ia.pkl`), tras lo cual podrás volver al paso 4 normal._

---

## ✍️ Manual de Usuario (Guía de Especificidad de NLP)

Esta Inteligencia Artificial está diseñada utilizando **Procesamiento de Lenguaje Natural (NLP)** con una comprensión de contexto (`N-Grams`). Por ende, para que la máquina entregue resultados sumamente precisos, los usuarios deben escribir siguiendo un "Patrón de Acción + Objeto".

Si el modelo detecta que la descripción está fuera de su límite de confianza (menor a 40%), se negará a clasificarlo aleatoriamente y arrojará el cartel: `Desconocido - Requiere Revisión Humana`.

**❌ Nivel Uno: Excesivamente Genérico / Suelto (NO recomendado)**
Escribir palabras solitarias, ambiguas o sueltas reducirá drásticamente la certeza matemática.

- _"Cuaderno"_ -> (Malo)
- _"Papa"_ -> (Malo)
- _"Luz"_ -> (Malo)

**✅ Nivel Dos: Específico Contextualizado (El Patrón de Oro)**
Este es el formato recomendado para obtener un modelo infalible. Usa un verbo o sustantivo de operación seguido del artículo. La IA unificará el bloque para comprender que hablas financieramente.

- _"Compra de cuadernos para el despacho"_ -> (Gasto - Útiles de Oficina)
- _"Recibo por pago de luz de este mes"_ -> (Gasto - Servicios Básicos)
- _"Compra de papas para almuerzo de personal"_ -> (Gasto - Alimentación Personal)

---

## 🏗️ Descripción Técnica (La Arquitectura)

### 1️⃣ ¿Qué paradigma de IA elegimos y por qué?

Para este problema contable elegimos el algoritmo **Naive Bayes Multinomial (MultinomialNB)** acompañado técnica de Procesamiento de Lenguaje Natural basada en **TF-IDF vectorial con Bigramas (`ngram_range=(1,2)`)**.

**Justificación:** ¿Por qué no usamos redes neuronales profundas (CNN/RNN) ni clustering (K-Means)?

- Un **K-Means** (Aprendizaje No Supervisado) intentaría agrupar las transacciones a ciegas sin saber cómo llamarlas, y la ciencia contable ya tiene un plan de cuentas estrictamente definido del que no podemos salirnos. Necesitamos Aprendizaje Supervisado.
- Una **Red Neuronal Profunda** requiere millones de datos y horas de poder de GPU para entrenar, siendo un "matamoscas para matar hormigas".
- Por su parte, la probabilidad del teorema de **Naive Bayes** es el rey indiscutible de la clasificación de textos en el mundo ligero. Es ultrarrápido computacionalmente, entrena en milisegundos y nos permite asignar probabilidades matemáticas exactas de certeza a cada palabra ingresada frente a nuestro de Plan de Cuentas estático.

### 2️⃣ ¿Qué herramientas y librerías se usaron?

Toda la lógica base se probó en entornos de exploración interactiva y fue madurada en el sistema de producción final utilizando:

- **Scikit-Learn:** El framework principal de Machine Learning encargado del Vectorizador (Traducción de texto humano a vectores matemáticos TF-IDF), el modelo `Pipeline` de flujo, y las métricas de `Accuracy_Score`.
- **Pandas & Numpy:** Motor de ingeniería y limpieza masiva de datos contables tabulares (Excel/DataFrames).
- **Joblib:** Para el congelamiento estático del conocimiento (serialización del cerebro `.pkl`), desacoplando el pesado entrenamiento de la veloz aplicación final interactiva.
- **Tkinter & Matplotlib:** Implementación nativa de la Interfaz Gráfica interactiva de la Calculadora y renderización del informe del rendimiento estadístico visual exportable.

### 3️⃣ ¿De dónde se obtuvieron los datos para entrenar a la máquina?

El cuerpo de conocimiento (`dataset_entrenamiento.xlsx`) fue creado partiendo de un set empírico base validado por la experticia humana de los desarrolladores.

Con el fin de lograr robustez en el porcentaje de entendimiento de lenguaje natural ruidoso, se inyectaron más de **6,700 registros** financieros sintéticos y de uso común. El dataset final fue sometido a una curación por _Moda Estadística_ para resolver contradicciones de clasificación y eliminar multiplicidad (esquirlas contables), garantizando que las 860 cuentas sugeridas únicas cuenten con un nivel de repetición equilibrado para sostener un análisis matemático de rigor probabilístico.
