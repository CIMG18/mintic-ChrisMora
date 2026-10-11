# FUNCION 1:
def euclidean_distance(point1, point2):
    import numpy as np
    p1 = np.array(point1, dtype=float)
    p2 = np.array(point2, dtype=float)

    if len(p1) != len(p2):
        raise ValueError("Los puntos deben tener la misma dimensión")

    diferencias = p1 - p2
    suma = np.sum(diferencias ** 2)
    return suma ** 0.5
# FUNCION 2:
def create_kmeans(data, n_clusters=8, max_iter=1000, tol=0.0001, randomstate=None):
    import numpy as np
    datos = np.array(data, dtype=float)
    n_filas = datos.shape[0]

    if isinstance(n_clusters, int) == False or n_clusters < 1:
        raise ValueError("n_clusters debe ser un entero positivo")
    if n_clusters > n_filas:
        raise ValueError("n_clusters no puede ser mayor al número de puntos")

    if randomstate != None:
        np.random.seed(randomstate)

    # elegimos k puntos al azar (sin repetir) como centroides iniciales
    indices_random = np.random.permutation(n_filas)
    indices_iniciales = indices_random[:n_clusters]
    centroides = datos[indices_iniciales].copy()

    kmeans = {
        'data': datos,
        'n_clusters': n_clusters,
        'max_iter': max_iter,
        'tol': tol,
        'centroids': centroides,
        'labels': None,
        'n_iter': 0,
        'converged': False
    }
    return kmeans
