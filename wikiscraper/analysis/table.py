import pandas as pd


def save_table_csv(df, phrase):
    filename = phrase.replace(" ", "_") + ".csv"
    df.to_csv(filename, index=False)


def value_freqs(df):
    flat = pd.Series(df.values.ravel()).dropna()
    flat = flat[flat.astype(str).str.strip() != ""]
    vc = flat.value_counts()
    return vc.reset_index().rename(columns={"index": "value", 0: "count"})
