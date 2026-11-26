def load_transactions(path):
    transacciones = []

    with open(path, 'r', encoding='utf-8-sig') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea == "":
                continue

            items = set()
            for item in linea.split(','):
                item = item.strip()
                if item != "":
                    items.add(item)

            if len(items) > 0:
                transacciones.append(items)

    return transacciones

def support(transactions, itemset):
    if len(transactions) == 0:
        raise ValueError("La lista de transacciones está vacía")

    items = set(itemset)
    contador = 0
    for t in transactions:
        if items.issubset(t):
            contador = contador + 1

    return contador / len(transactions)

# NOTA: Se usó ayuda de IA para la función apriori, pero se hizo revisión y corrección de errores. Se agregaron validaciones y se mejoró la legibilidad del código.
def apriori(transactions, min_support=0.05, max_len=None, verbose=False):
    import pandas as pd
    
    if len(transactions) == 0:
        raise ValueError("La lista de transacciones está vacía")
    if min_support <= 0 or min_support > 1:
        raise ValueError("min_support debe ser mayor que 0 y menor o igual a 1")

    n = len(transactions)
    todos_los_itemsets = []
    todos_los_soportes = []

    conteo = {}
    for t in transactions:
        for item in t:
            if item in conteo:
                conteo[item] = conteo[item] + 1
            else:
                conteo[item] = 1

    frecuentes_previos = []
    for item in conteo:
        sop = conteo[item] / n
        if sop >= min_support:
            itemset = frozenset([item])
            frecuentes_previos.append(itemset)
            todos_los_itemsets.append(itemset)
            todos_los_soportes.append(sop)

    if verbose:
        print("k=1:", len(conteo), "candidatos,", len(frecuentes_previos), "frecuentes")

    # ---- niveles k>=2 ----
    k = 2
    while len(frecuentes_previos) > 0:
        if max_len != None and k > max_len:
            break

        set_previos = set(frecuentes_previos)

        # 1) generar candidatos uniendo
        candidatos = []
        vistos = set()
        for i in range(len(frecuentes_previos)):
            for j in range(i + 1, len(frecuentes_previos)):
                union = frecuentes_previos[i] | frecuentes_previos[j]
                if len(union) == k and union not in vistos:
                    vistos.add(union)

                    # 2) poda
                    sobrevive = True
                    for item in union:
                        subconjunto = union - frozenset([item])
                        if subconjunto not in set_previos:
                            sobrevive = False
                            break

                    if sobrevive:
                        candidatos.append(union)

        # 3) contar el soporte solo de los candidatos que sobrevivieron
        frecuentes_nuevos = []
        for cand in candidatos:
            contador = 0
            for t in transactions:
                if cand.issubset(t):
                    contador = contador + 1
            sop = contador / n
            if sop >= min_support:
                frecuentes_nuevos.append(cand)
                todos_los_itemsets.append(cand)
                todos_los_soportes.append(sop)

        if verbose:
            print("k=" + str(k) + ":", len(candidatos), "candidatos,", len(frecuentes_nuevos), "frecuentes")

        frecuentes_previos = frecuentes_nuevos
        k = k + 1

    resultado = pd.DataFrame({'itemsets': todos_los_itemsets, 'support': todos_los_soportes})
    resultado = resultado.sort_values('support', ascending=False).reset_index(drop=True)
    return resultado

