def impute_missing(data, strategy='mean', columns=None):
    df = data.copy()
    
    if columns == None:
        cols_to_use = df.columns
    else:
        cols_to_use = columns

    for col in cols_to_use:
        no_nan = df[col].dropna()  # quita los NaN de esa columna

        if strategy == 'mean':
            suma = 0
            for v in no_nan:
                suma += v
            valor = suma / len(no_nan)

        elif strategy == 'median':
            valores_ordenados = no_nan.sort_values().values
            n = len(valores_ordenados)
            if n % 2 == 0:
                # Si es par, la mediana es el promedio de los dos valores centrales
                valor = (valores_ordenados[n//2 - 1] + valores_ordenados[n//2]) / 2
            else:
                valor = valores_ordenados[n//2]

        elif strategy == 'mode':
            conteo = no_nan.value_counts()  # cuenta cuántas veces aparece cada valor
            valor = conteo.index[0]  # el más frecuente queda primero

        else:
            print("Estrategia no válida:", strategy)
            valor = None

        df[col] = df[col].fillna(valor)

    return df
def plot_missing(data):
    import matplotlib.pyplot as plt
    
    nulos = data.isnull().sum() # We use the attribute 'isnull' to find the missing values in the dataset and then we use the attribute 'sum' to sum the missing values by column
    nulos = nulos[nulos > 0] # We focus on the columns that have missinf values
    nulos.sort_values(inplace=True) # It works to sort the values in order to have a better visualization of the data
    
    plt.figure(figsize=(15,6))
    nulos.plot.bar()
    plt.title('Valores nulos por columna')
    plt.ylabel('Número de valores nulos')
    plt.xlabel('Columnas')
    plt.show()
def detect_outliers(data, method='iqr', threshold=1.5):
    import numpy as np
    import pandas as pd
    
    df = data.copy()
    resultado = pd.DataFrame(index=df.index)

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]) == False or df[col].dtype == bool:
            # si la columna no es numérica, o es booleana, no aplicamos detección
            resultado[col] = False
            continue

        no_nan = df[col].dropna()

        if method == 'iqr':
            q1 = np.percentile(no_nan, 25)
            q3 = np.percentile(no_nan, 75)
            iqr = q3 - q1
            limite_inferior = q1 - threshold * iqr
            limite_superior = q3 + threshold * iqr

            es_outlier = (df[col] < limite_inferior) | (df[col] > limite_superior)

        elif method == 'zscore':
            # calculamos la media
            suma = 0
            for v in no_nan:
                suma = suma + v
            media = suma / len(no_nan)

            # calculamos la desviación estándar
            suma_cuadrados = 0
            for v in no_nan:
                suma_cuadrados = suma_cuadrados + (v - media) ** 2
            desviacion = (suma_cuadrados / len(no_nan)) ** 0.5

            z_scores = (df[col] - media) / desviacion
            es_outlier = z_scores.abs() > threshold

        else:
            print("Método no válido:", method)
            es_outlier = pd.Series(False, index=df.index)

        resultado[col] = es_outlier

    return resultado
def handle_outliers(data, method='iqr', action='trim', threshold=1.5):
    df = data.copy()

    for col in df.columns:
        # esta condición evita que se apliquen métodos de outliers a columnas no numéricas o booleanas usando la función proporcionada en clase
        if pd.api.types.is_numeric_dtype(df[col]) == False or df[col].dtype == bool: 
            continue

        no_nan = df[col].dropna()

        # Bloque de código recuperado de la función detect_outliers para calcular los límites de outliers
        if method == 'iqr':
            q1 = np.percentile(no_nan, 25)
            q3 = np.percentile(no_nan, 75)
            iqr = q3 - q1
            limite_inferior = q1 - threshold * iqr
            limite_superior = q3 + threshold * iqr

        # Bloque de código recuperado de la función detect_outliers para calcular los límites de outliers
        elif method == 'zscore':
            suma = 0
            for v in no_nan:
                suma += v
            media = suma / len(no_nan)

            suma_cuadrados = 0
            for v in no_nan:
                suma_cuadrados += (v - media) ** 2
            desviacion = (suma_cuadrados / len(no_nan)) ** 0.5

            limite_inferior = media - threshold * desviacion
            limite_superior = media + threshold * desviacion

        else:
            print("Método no válido:", method)
            continue

        if action == 'trim':
            # se eliminan las filas donde el valor esté fuera de los límites
            df = df[(df[col] >= limite_inferior) & (df[col] <= limite_superior) | df[col].isna()]

        elif action == 'cap':
            # recortamos los valores a los límites, sin eliminar filas
            df.loc[df[col] < limite_inferior, col] = limite_inferior
            df.loc[df[col] > limite_superior, col] = limite_superior

        else:
            print("Acción no válida:", action)

    return df