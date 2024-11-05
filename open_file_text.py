import pandas as pd

df = pd.read_csv('/Users/michalkoperski/Library/Mobile Documents/com~apple~CloudDocs/db.csv')

print(df)
print(len(df))

df.loc[len(df) + 1] = ['1970-01-01', "Krzysztof", "Kononowicz", 'mleczarz', "1980-02-04", "Sikal"]

print(df)

df.to_csv('/Users/michalkoperski/Library/Mobile Documents/com~apple~CloudDocs/db.csv')