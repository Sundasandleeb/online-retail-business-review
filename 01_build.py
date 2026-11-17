import pandas as pd

sheets = pd.read_excel("online_retail_II.xlsx", sheet_name=None)

for name, t in sheets.items():
    print(name, t.shape, t["InvoiceDate"].min(), t["InvoiceDate"].max())

df = pd.concat(sheets.values(), ignore_index=True)
print(df.shape)
print("Exact duplicate rows:", df.duplicated().sum())
print(df.isna().sum())

df = df.drop_duplicates()
print(df.shape)

df.to_csv("online_retail_II.csv", index=False)