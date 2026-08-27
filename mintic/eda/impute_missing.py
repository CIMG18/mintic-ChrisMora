def impute_missing(data, strategy='mean', columns= None):
    df = data.copy()
    if columns == None:
        columns = df.columns
    
    for data in columns: # This for loop determines the strategy to fill the mising data
        if strategy == 'mean':
            value = df[data].mean()
        elif strategy == 'median':
            value = df[data].median()
        elif strategy == 'mode':
            value = df[data].mode()
        else:
            print("There has been a problem")
        
        df[data] = df[data].fillna(value) # Once we´ve obtained strategy we fill the missing values using a pandas attribute called 'fillna'
        return df