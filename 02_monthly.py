import pandas as pd    #getting the tools i need for this project
import matplotlib.pyplot as plt
                       #getting the data
df = pd.read_csv("online_retail_II.csv", parse_dates=["InvoiceDate"])
                      #treat Invoice date column as date, all others are treated as text by default in python
df["Revenue"] = df["Quantity"] * df["Price"]  #creating a new useful column for analysis
df["Month"] = df["InvoiceDate"].dt.to_period("M") #month column to group sales by month
df["is_cancel"] = df["Invoice"].astype(str).str.startswith("C")

# removing two orders that were canceled right after being placed
df = df[df["Quantity"].abs() != 80995]
pair = df["Invoice"].astype(str).isin(["541431", "C541433"])
df = df[pair == False]
print(df.shape)

# removing non-product entries (postage, fees, adjustments)
non_product = ["POST", "DOT", "C2", "M", "D", "S", "BANK CHARGES", "ADJUST", "AMAZONFEE"]
df = df[df["StockCode"].astype(str).isin(non_product) == False]
print(df.shape)
# calculating monthly sales & returns
sales = df[df["is_cancel"] == False].groupby("Month")["Revenue"].sum()
returns = df[df["is_cancel"] == True].groupby("Month")["Revenue"].sum()
# creating new table with 3 columns
table = pd.DataFrame({"sales": sales, "returns": returns})
table["net"] = table["sales"] + table["returns"]  #net= sales - returns (returns are negative)
print(table)

#Charts
months = table.index.astype(str).tolist()  #row labels: getting list of months name with the last month renamed
months[-1] = "2011-12 (9 days only)"

plt.figure(figsize=(11, 5))  #blank chart with this size
plt.plot(months, table["sales"], label="Sales") # draw first line , first x-axis , second y-axis
plt.plot(months, table["net"], label="Net (after returns)") #draw second line in same chart
plt.xticks(rotation=90)  #turn the month names sideways so they don’t overlap.
plt.title("Monthly revenue (GBP). Dec 2011 has only 9 days")
plt.legend()  #shows which line is which
plt.tight_layout()
plt.savefig("monthly_revenue.png")
plt.show()