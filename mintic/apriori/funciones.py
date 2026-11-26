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