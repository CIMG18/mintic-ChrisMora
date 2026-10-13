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
# FUNCION 3:
def kmeans_fit(kmeans, verbose=True):

    def asignar_clusters(datos, centroides):
        etiquetas = []
        for i in range(len(datos)):
            mejor_cluster = 0
            mejor_distancia = euclidean_distance(datos[i], centroides[0])
            for c in range(1, len(centroides)):
                d = euclidean_distance(datos[i], centroides[c])
                if d < mejor_distancia:
                    mejor_distancia = d
                    mejor_cluster = c
            etiquetas.append(mejor_cluster)
        return np.array(etiquetas)

    datos = kmeans['data']
    centroides = kmeans['centroids']
    k = kmeans['n_clusters']

    for iteracion in range(1, kmeans['max_iter'] + 1):
        etiquetas = asignar_clusters(datos, centroides)

        nuevos_centroides = centroides.copy()
        for c in range(k):
            puntos_del_cluster = datos[etiquetas == c]
            if len(puntos_del_cluster) > 0:
                nuevos_centroides[c] = np.mean(puntos_del_cluster, axis=0)
            # si el cluster quedó vacío, dejamos su centroide donde estaba

        # qué tanto se movieron los centroides en esta iteración
        cambio_maximo = 0
        for c in range(k):
            d = euclidean_distance(centroides[c], nuevos_centroides[c])
            if d > cambio_maximo:
                cambio_maximo = d

        centroides = nuevos_centroides
        kmeans['n_iter'] = iteracion

        if verbose:
            print("Iteración", iteracion, "- cambio máximo de centroides:", cambio_maximo)

        if cambio_maximo <= kmeans['tol']:
            kmeans['converged'] = True
            break

    if verbose:
        if kmeans['converged']:
            print("Convergió en", kmeans['n_iter'], "iteraciones")
        else:
            print("Se llegó al máximo de iteraciones sin converger")

    kmeans['centroids'] = centroides
    kmeans['labels'] = asignar_clusters(datos, centroides)
    return kmeans
# FUNCION 4:
def inertia(kmeans):
    if kmeans['labels'] is None:
        raise ValueError("Primero hay que ejecutar kmeans_fit")

    total = 0
    for i in range(len(kmeans['data'])):
        centroide = kmeans['centroids'][kmeans['labels'][i]]
        d = euclidean_distance(kmeans['data'][i], centroide)
        total = total + d ** 2
    return total
# FUNCION 5:
def elbow(data, min=2, max=8, max_iter=1000, tol=0.001, randomstate=None):
    valores_k = []
    inercias = []

    for k in range(min, max + 1):
        modelo = create_kmeans(data, n_clusters=k, max_iter=max_iter, tol=tol, randomstate=randomstate)
        modelo = kmeans_fit(modelo, verbose=False)
        valores_k.append(k)
        inercias.append(inertia(modelo))
        print("k =", k, "- inercia:", inercias[-1])

    plt.figure(figsize=(8, 5))
    plt.plot(valores_k, inercias, marker='o')
    plt.xlabel("Número de clusters (k)")
    plt.ylabel("Inercia")
    plt.title("Método del codo")
    plt.xticks(valores_k)
    plt.grid(True)
    plt.show()