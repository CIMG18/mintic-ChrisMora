# Carga de datos

`sample_dataset.csv` es un dataset sintético para pruebas rápidas. Para los retos del curso, se recomienda usar datasets reales del [UCI Machine Learning Repository](https://archive.ics.uci.edu/).

## Cargar datos remotos sin descargarlos a disco

`pandas.read_csv()` acepta una URL directamente, por lo que no es necesario descargar el archivo manualmente:

```python
import pandas as pd

url = "https://archive.ics.uci.edu/static/public/53/iris.zip"  # ejemplo, ajustar a la URL real del dataset
df = pd.read_csv(url)
```

Si el dataset no está en un CSV simple (por ejemplo, viene sin encabezados o en un `.data`), especifica los parámetros correspondientes:

```python
columnas = ["feat_1", "feat_2", "feat_3", "target"]
df = pd.read_csv(url, header=None, names=columnas)
```

Busca el dataset en UCI, copia el enlace directo al archivo de datos (no la página HTML del dataset) y pásalo como `url` a `pd.read_csv()`.
