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


def calcular_entropia(y):
    import numpy as np
    valores, conteos = np.unique(y, return_counts=True)
    total = len(y)
    
    entropia = 0
    for i in range(len(valores)):
        p = conteos[i] / total
        entropia = entropia - p * np.log2(p)
    
    return entropia


def calcular_ganancia(X, y, indice_columna):
    import numpy as np
    entropia_padre = calcular_entropia(y)
    
    columna = X[:, indice_columna]
    valores_unicos = np.unique(columna)
    total = len(y)
    
    entropia_ponderada = 0
    for valor in valores_unicos:
        mascara = columna == valor
        y_subconjunto = y[mascara]
        peso = len(y_subconjunto) / total
        entropia_ponderada = entropia_ponderada + peso * calcular_entropia(y_subconjunto)
    
    ganancia = entropia_padre - entropia_ponderada
    return ganancia