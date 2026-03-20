def limpiar_datos(df):
    df = df.dropna()
    df = df[df['Quantity'] > 0]
    return df