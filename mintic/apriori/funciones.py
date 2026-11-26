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

