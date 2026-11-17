import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("online_retail_II.csv", parse_dates=["InvoiceDate"])

df["Revenue"] = df["Quantity"] * df["Price"]
df["Month"] = df["InvoiceDate"].dt.to_period("M")
df["is_cancel"] = df["Invoice"].astype(str).str.startswith("C")

# remove two orders that were cancelled right after being placed
df = df[df["Quantity"].abs() != 80995]
pair = df["Invoice"].astype(str).isin(["541431", "C541433"])
df = df[pair == False]
print(df.shape)

sales = df[df["is_cancel"] == False].groupby("Month")["Revenue"].sum()
returns = df[df["is_cancel"] == True].groupby("Month")["Revenue"].sum()

table = pd.DataFrame({"sales": sales, "returns": returns})
table["net"] = table["sales"] + table["returns"]
print(table)

months = table.index.astype(str).tolist()
months[-1] = "2011-12 (9 days only)"

plt.figure(figsize=(11, 5))
plt.plot(months, table["sales"], label="Sales")
plt.plot(months, table["net"], label="Net (after returns)")
plt.xticks(rotation=90)
plt.title("Monthly revenue (GBP). Dec 2011 has only 9 days")
plt.legend()
plt.tight_layout()
plt.savefig("monthly_revenue.png")
plt.show()