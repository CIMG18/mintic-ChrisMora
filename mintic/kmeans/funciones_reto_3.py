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