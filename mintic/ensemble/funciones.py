# FUNCIÓN 1:
def bootstrap_sample(X, y, random_state=42):
    import numpy as np
    n_filas = X.shape[0]

    if random_state != None:
        np.random.seed(random_state)

    indices_elegidos = []
    for i in range(n_filas):
        indice_random = np.random.randint(0, n_filas)
        indices_elegidos.append(indice_random)

    X_sample = X[indices_elegidos]
    y_sample = y[indices_elegidos]

    return X_sample, y_sample

# FUNCIÓN 2:
def build_id3_tree(X, y, columnas_disponibles=None):
    import numpy as np

    def calcular_entropia(y_datos):
        valores, conteos = np.unique(y_datos, return_counts=True)
        total = len(y_datos)
        
        entropia = 0
        for i in range(len(valores)):
            p = conteos[i] / total
            entropia = entropia - p * np.log2(p)
        
        return entropia

    def calcular_ganancia(X_datos, y_datos, indice_columna):
        entropia_padre = calcular_entropia(y_datos)
        
        columna = X_datos[:, indice_columna]
        valores_unicos = np.unique(columna)
        total = len(y_datos)
        
        entropia_ponderada = 0
        for valor in valores_unicos:
            mascara = columna == valor
            y_subconjunto = y_datos[mascara]
            peso = len(y_subconjunto) / total
            entropia_ponderada = entropia_ponderada + peso * calcular_entropia(y_subconjunto)
        
        ganancia = entropia_padre - entropia_ponderada
        return ganancia

    # --- lógica principal de build_id3_tree, igual que antes ---
    if columnas_disponibles == None:
        columnas_disponibles = list(range(X.shape[1]))

    valores_clase = np.unique(y)

    if len(valores_clase) == 1:
        return valores_clase[0]

    if len(columnas_disponibles) == 0:
        clases, conteos = np.unique(y, return_counts=True)
        clase_mayoritaria = clases[np.argmax(conteos)]
        return clase_mayoritaria

    mejor_ganancia = -1
    mejor_columna = None
    for col in columnas_disponibles:
        ganancia = calcular_ganancia(X, y, col)
        if ganancia > mejor_ganancia:
            mejor_ganancia = ganancia
            mejor_columna = col

    arbol = {mejor_columna: {}}

    columnas_restantes = []
    for col in columnas_disponibles:
        if col != mejor_columna:
            columnas_restantes.append(col)

    valores_de_columna = np.unique(X[:, mejor_columna])
    for valor in valores_de_columna:
        mascara = X[:, mejor_columna] == valor
        X_subconjunto = X[mascara]
        y_subconjunto = y[mascara]

        if len(y_subconjunto) == 0:
            clases, conteos = np.unique(y, return_counts=True)
            arbol[mejor_columna][valor] = clases[np.argmax(conteos)]
        else:
            subarbol = build_id3_tree(X_subconjunto, y_subconjunto, columnas_restantes)
            arbol[mejor_columna][valor] = subarbol

    return arbol

def build_random_forest(X, y, n_trees=10, random_state=42):
    lista_de_arboles = []

    for i in range(n_trees):
        if random_state != None:
            semilla_arbol = random_state + i
        else:
            semilla_arbol = None

        X_sample, y_sample = bootstrap_sample(X, y, random_state=semilla_arbol)
        arbol = build_id3_tree(X_sample, y_sample)
        lista_de_arboles.append(arbol)

    return lista_de_arboles