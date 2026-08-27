import matplotlib.pyplot as plt

def plot_missing(data):
    nulos = data.isnull().sum() # We use the attribute 'isnull' to find the missing values in the dataset and then we use the attribute 'sum' to sum the missing values by column
    nulos = nulos[nulos > 0] # We focus on the columns that have missinf values
    nulos.sort_values(inplace=True) # It works to sort the values in order to have a better visualization of the data
    
    plt.figure(figsize=(15,6))
    nulos.plot.bar()
    plt.title('Valores nulos por columna')
    plt.ylabel('Número de valores nulos')
    plt.xlabel('Columnas')
    plt.show()
